from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from fastapi.responses import HTMLResponse, JSONResponse
import uuid
import time
import os
from datetime import datetime
import re
from typing import List, Dict
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor  # ADDED FOR MULTI-UPLOAD

# Request schema for chat
class ChatRequest(BaseModel):
    query: str

class DocumentUpdate(BaseModel):
    content: str

# Ollama settings - DISABLED by default
OLLAMA_ENABLED = False  # Set to True ONLY if you have Ollama working properly
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB with proper persistence
chroma_dir = "./chroma_store"
os.makedirs(chroma_dir, exist_ok=True)

# In-memory storage for UI document management (separate from ChromaDB)
ui_documents = []  # Stores documents for UI CRUD operations

# Session-level in-memory storage (for current run/session)
# `current_session_id` identifies the active session; `session_documents`
# holds documents uploaded during this session only.
current_session_id = str(uuid.uuid4())
session_documents: List[Dict] = []

# Load UI documents from file if exists
def load_ui_documents():
    global ui_documents
    try:
        if os.path.exists("ui_documents.json"):
            with open("ui_documents.json", "r") as f:
                ui_documents = json.load(f)
                print(f"Loaded {len(ui_documents)} UI documents from storage")
    except Exception as e:
        print(f"Error loading UI documents: {e}")
        ui_documents = []

def save_ui_documents():
    try:
        with open("ui_documents.json", "w") as f:
            json.dump(ui_documents, f)
    except Exception as e:
        print(f"Error saving UI documents: {e}")

# Initialize ChromaDB collection for embeddings
try:
    client = chromadb.PersistentClient(path=chroma_dir)
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    )
    print(f"ChromaDB initialized. Documents in collection: {collection.count()}")
except Exception as e:
    print(f"ChromaDB initialization error: {e}")
    collection = None
    
load_ui_documents()    # Load UI documents on startup
executor = ThreadPoolExecutor(max_workers=4)    # Thread pool for parallel processing - ADDED FOR MULTI-UPLOAD

def print_banner():
    print("=" * 60)
    print("DOCUMENT PROCESSING BACKEND")
    print("=" * 60)
    print(f"Server started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"ChromaDB directory: {chroma_dir}")
    print(f"UI Documents loaded: {len(ui_documents)}")
    print(f"Embedding model: all-MiniLM-L6-v2")
    print(f"Ollama enabled: {OLLAMA_ENABLED}")
    print("=" * 60)
print_banner()

@app.get("/")
def home():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] GET / - Serving portal.html")
    with open("portal.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

def process_single_file(file: UploadFile, file_index: int, total_files: int):  # ADDED FOR MULTI-UPLOAD
    """Process a single file - can be called in parallel"""
    print(f"\n  [{file_index}/{total_files}] Processing: {file.filename}")
    
    start_time = time.time()
    file_content = file.file.read()        # Read file content
    file.file.seek(0)  # Reset file pointer
    # Extract text
    is_pdf = file.filename.lower().endswith('.pdf')
    text = ""
    
    if is_pdf:
        try:
            with pdfplumber.open(file.file) as pdf:
                num_pages = len(pdf.pages)
                print(f" {file.filename}: {num_pages} pages")
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"--- Page {page_num} ---\n{page_text}\n\n"
        except Exception as e:
            print(f" PDF processing error for {file.filename}: {e}")
            raise
    else:
        try:
            text = file_content.decode("utf-8")
        except UnicodeDecodeError:
            text = file_content.decode("latin-1", errors="ignore")
    
    if not text.strip():
        print(f"Warning: No text extracted from {file.filename}")
        return None
    
    # Create document record
    doc_id = str(uuid.uuid4())
    ui_document = {
        "id": doc_id,
        "filename": file.filename,
        "content": text,
        "uploaded_at": datetime.now().isoformat(),
        "size": len(text),
        "file_type": "pdf" if is_pdf else "text",
        "session_id": current_session_id 
    }
    
    # Store in ChromaDB for chatbot
    if collection and text.strip():
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        print(f"    ✂️ Created {len(chunks)} chunks for embeddings")
        for idx, chunk in enumerate(chunks):
            try:
                chunk_id = f"{doc_id}_chunk_{idx}"
                collection.add(
                    documents=[chunk],
                    ids=[chunk_id],
                    metadatas=[{
                        "source": file.filename,
                        "doc_id": doc_id,
                        "session_id": current_session_id,
                        "chunk": idx,
                        "type": "embedding"
                    }]
                )
            except Exception as e:
                print(f"Error storing chunk {idx}: {e}")
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Processed: {file.filename} ({len(text)} chars, {processing_time:.2f}s)")
    return ui_document

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print("\n" + "=" * 60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📥 SINGLE FILE UPLOAD")
    print(f"File: {file.filename}")
    start_time = time.time()
    
    # Read file content
    content = await file.read()
    is_pdf = file.filename.lower().endswith('.pdf')
    
    # Extract text
    text = ""
    if is_pdf:
        print("Processing PDF file...")
        try:
            import io
            file_stream = io.BytesIO(content)
            with pdfplumber.open(file_stream) as pdf:
                num_pages = len(pdf.pages)
                print(f"PDF has {num_pages} pages")
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"--- Page {page_num} ---\n{page_text}\n\n"
        except Exception as e:
            print(f"PDF processing error: {e}")
            return {"status": "error", "message": f"PDF processing failed: {str(e)}"}
    else:
        print("Processing text file...")
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1", errors="ignore")

    if not text.strip():
        print("ERROR: No text extracted from file!")
        return {"status": "error", "message": "No text extracted from file"}

    print(f"Total text extracted: {len(text)} characters")
    
    # Create document with session ID
    doc_id = str(uuid.uuid4())
    ui_document = {
        "id": doc_id,
        "filename": file.filename,
        "content": text,
        "uploaded_at": datetime.now().isoformat(),
        "size": len(text),
        "file_type": "pdf" if is_pdf else "text",
        "session_id": current_session_id  # ADD THIS
    }
    
    # Store in session documents ONLY (not persistent storage)
    session_documents.append(ui_document)
    print(f"Added to session documents: {file.filename} (Session: {current_session_id})")
    
    # Also store in persistent storage for backup (optional)
    ui_documents.append(ui_document)
    save_ui_documents()
    
    # Store in ChromaDB for chatbot
    if collection and text.strip():
        print("Creating embeddings for chatbot...")
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        print(f"Created {len(chunks)} chunks for embeddings")
        
        for idx, chunk in enumerate(chunks):
            try:
                chunk_id = f"{doc_id}_chunk_{idx}"
                collection.add(
                    documents=[chunk],
                    ids=[chunk_id],
                    metadatas=[{
                        "source": file.filename,
                        "doc_id": doc_id,
                        "session_id": current_session_id,
                        "chunk": idx,
                        "type": "embedding"
                    }]
                )
            except Exception as e:
                print(f"Error storing chunk {idx}: {e}")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print("=" * 60)
    print("UPLOAD COMPLETE")
    print("=" * 60)
    print(f"File: {file.filename}")
    print(f"Time: {processing_time:.2f}s")
    print(f"Text: {len(text)} chars")
    print(f"Added to session: ✓ (Session ID: {current_session_id})")
    print(f"Added to ChromaDB: {len(chunks) if collection else 0} chunks")
    print("=" * 60 + "\n")
    return {
        "status": "success",
        "filename": file.filename,
        "document_id": doc_id,
        "session_id": current_session_id,
        "size": len(text),
        "processing_time": f"{processing_time:.2f}s",
        "message": f"{file.filename} uploaded successfully!\nDocument is now available for viewing and editing."
}


@app.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files at once"""
    print("\n" + "=" * 60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📥 MULTI-FILE UPLOAD STARTED")
    print(f"Session ID: {current_session_id}")
    print(f"Files received: {len(files)}")
    if not files:
        return {"status": "error", "message": "No files selected"}
    start_time = time.time()
    successful_uploads = []
    failed_uploads = []
    print("Starting parallel processing...")
    # Process files in parallel
    loop = asyncio.get_event_loop()
    tasks = []
    for i, file in enumerate(files, 1):
        task = loop.run_in_executor(
            executor, 
            process_single_file, 
            file, i, len(files)
        )
        tasks.append(task)
    results = await asyncio.gather(*tasks, return_exceptions=True)    # Wait for all tasks to complete
    
    # Process results
    for i, result in enumerate(results):
        filename = files[i].filename if i < len(files) else f"File {i+1}"
        
        if isinstance(result, Exception):
            print(f"Failed: {filename} - {str(result)}")
            failed_uploads.append({
                "filename": filename,
                "error": str(result)
            })
        elif result is not None:
            # Add to session documents
            session_documents.append(result)
            # Also add to persistent storage (optional)
            ui_documents.append(result)
            successful_uploads.append(result)
            print(f"Added to session: {result['filename']}")
    
    # Save all documents at once
    if successful_uploads:
        save_ui_documents()
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(files)}")
    print(f"Successful: {len(successful_uploads)}")
    print(f"Failed: {len(failed_uploads)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per file: {total_time/len(files):.2f}s")
    print(f"Session documents count: {len(session_documents)}")
    print(f"Total documents in ChromaDB: {collection.count() if collection else 0}")
    print("=" * 60)
    
    # Prepare response
    response = {
        "status": "success" if successful_uploads else "partial" if failed_uploads else "error",
        "total_files": len(files),
        "successful": len(successful_uploads),
        "failed": len(failed_uploads),
        "processing_time": f"{total_time:.2f}s",
        "session_id": current_session_id,
        "session_documents": len(session_documents),
        "successful_files": [
            {
                "filename": doc["filename"],
                "id": doc["id"],
                "size": doc["size"],
                "preview": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"]
            }
            for doc in successful_uploads
        ],
        "failed_files": failed_uploads
    }
    
    if successful_uploads:
        response["message"] = f"Successfully uploaded {len(successful_uploads)} file(s) to current session"
        if failed_uploads:
            response["message"] += f", {len(failed_uploads)} failed"
    else:
        response["message"] = "No files were uploaded successfully"
    
    return response

# Get all UI documents (not chunks) - SESSION DOCUMENTS ONLY
@app.get("/ui-documents")
async def get_ui_documents():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📋 GET /ui-documents")
    print(f"Session ID: {current_session_id}")
    print(f"Session documents count: {len(session_documents)}")
    print(f"All documents in storage: {len(ui_documents)}")
    
    # Debug: Show all session document filenames
    if session_documents:
        print("Session documents:")
        for i, doc in enumerate(session_documents):
            print(f"  {i+1}. {doc['filename']} (ID: {doc['id'][:8]})")
    
    # Return ONLY session documents
    documents_info = []
    for doc in session_documents:
        documents_info.append({
            "id": doc["id"],
            "filename": doc["filename"],
            "uploaded_at": doc["uploaded_at"],
            "size": doc["size"],
            "session_id": doc.get("session_id", current_session_id),
            "preview": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"]
        })
    return {
        "status": "success",
        "count": len(documents_info),
        "session_id": current_session_id,
        "total_in_chromadb": collection.count() if collection else 0,
        "documents": documents_info
    }
    
# Get specific UI document content - ADD THIS ENDPOINT
@app.get("/ui-documents/{doc_id}")
async def get_ui_document(doc_id: str):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📖 GET /ui-documents/{doc_id}")
    print(f"Looking for document ID: {doc_id}")
    
    # Search in session documents first
    for doc in session_documents:
        if doc["id"] == doc_id:
            print(f"Found in session: {doc['filename']}")
            return {
                "status": "success",
                "document": {
                    "id": doc["id"],
                    "filename": doc["filename"],
                    "content": doc["content"],
                    "uploaded_at": doc["uploaded_at"],
                    "size": doc["size"],
                    "file_type": doc.get("file_type", "text"),
                    "session_id": doc.get("session_id", current_session_id)
                }
            }
    
    # If not found in session, check persistent storage
    print(f"Document ID {doc_id} not found in session documents")
    for doc in ui_documents:
        if doc["id"] == doc_id:
            print(f"Found in persistent storage: {doc['filename']}")
            return {
                "status": "success",
                "document": {
                    "id": doc["id"],
                    "filename": doc["filename"],
                    "content": doc["content"],
                    "uploaded_at": doc["uploaded_at"],
                    "size": doc["size"],
                    "file_type": doc.get("file_type", "text"),
                    "session_id": doc.get("session_id", current_session_id)
                }
            }
    
    print(f"Document ID {doc_id} not found anywhere")
    return {"status": "error", "message": "Document not found"}
    
# Update UI document content    # Get specific UI document content  
@app.put("/ui-documents/{doc_id}")
async def update_ui_document(doc_id: str, update: DocumentUpdate):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✏️ PUT /ui-documents/{doc_id}")
    print(f"Looking for document ID: {doc_id}")
    
    # Search in session documents
    doc_found = False
    for doc in session_documents:
        if doc["id"] == doc_id:
            print(f"Found in session: {doc['filename']}")
            print(f"Old content length: {len(doc['content'])} chars")
            print(f"New content length: {len(update.content)} chars")
            
            # Update session document
            doc["content"] = update.content
            doc["size"] = len(update.content)
            doc_found = True
            
            # Also update in persistent storage
            for persistent_doc in ui_documents:
                if persistent_doc["id"] == doc_id:
                    persistent_doc["content"] = update.content
                    persistent_doc["size"] = len(update.content)
            
            
            save_ui_documents()    # Save to file
            
            # Update ChromaDB embeddings
            if collection:
                # Remove old embeddings
                try:
                    results = collection.get(where={"doc_id": doc_id})
                    if results and results["ids"]:
                        collection.delete(ids=results["ids"])
                        print(f"Removed {len(results['ids'])} old embeddings")
                except Exception as e:
                    print(f"Error removing old embeddings: {e}")
                
                # Add new embeddings
                chunk_size = 1000
                chunks = [update.content[i:i+chunk_size] for i in range(0, len(update.content), chunk_size)]
                print(f"Creating {len(chunks)} new chunks for updated document")
                for idx, chunk in enumerate(chunks):
                    try:
                        chunk_id = f"{doc_id}_chunk_{idx}_updated"
                        collection.add(
                            documents=[chunk],
                            ids=[chunk_id],
                            metadatas=[{
                                "source": doc["filename"],
                                "doc_id": doc_id,
                                "session_id": current_session_id,
                                "chunk": idx,
                                "type": "embedding",
                                "updated": True,
                                "update_time": datetime.now().isoformat()
                            }]
                        )
                    except Exception as e:
                        print(f"Error storing updated chunk {idx}: {e}")
            
            print(f"Document '{doc['filename']}' updated successfully")
            return {"status": "success", "message": "Document updated successfully"}
    
    if not doc_found:
        print(f"Document ID {doc_id} not found in session documents")
        # Try to find in persistent storage
        for doc in ui_documents:
            if doc["id"] == doc_id:
                print(f"Found in persistent storage but not in session: {doc['filename']}")
                return {"status": "error", "message": "Document found but not in current session. Please re-upload it."}
    return {"status": "error", "message": "Document not found"}

# Delete UI document
@app.delete("/ui-documents/{doc_id}")
async def delete_ui_document(doc_id: str):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🗑️ DELETE /ui-documents/{doc_id}")
    print(f"Looking for document ID: {doc_id} in session")
    
    # Remove from session documents
    for i, doc in enumerate(session_documents):
        if doc["id"] == doc_id:
            print(f"Found in session: {doc['filename']}")
            deleted_doc = session_documents.pop(i)    # Remove from session documents
            # Also remove from persistent storage
            for j, persistent_doc in enumerate(ui_documents):
                if persistent_doc["id"] == doc_id:
                    ui_documents.pop(j)
                    break
            save_ui_documents()    # Save changes to file
            if collection:    # Remove from ChromaDB
                try:
                    results = collection.get(where={"doc_id": doc_id})
                    if results and results["ids"]:
                        collection.delete(ids=results["ids"])
                        print(f"Removed {len(results['ids'])} embeddings from ChromaDB")
                except Exception as e:
                    print(f"Error removing embeddings: {e}")
            print(f"Document '{deleted_doc['filename']}' deleted from session")
            print(f"Session documents count after deletion: {len(session_documents)}")
            return {
                "status": "success", 
                "message": f"Document '{deleted_doc['filename']}' deleted successfully",
                "session_documents_count": len(session_documents)
            }
    print(f"Document ID {doc_id} not found in session")
    
    # Also check if it exists in persistent storage (for cleanup)
    for doc in ui_documents:
        if doc["id"] == doc_id:
            print(f"Document exists in persistent storage but not in session: {doc['filename']}")
    return {"status": "error", "message": "Document not found in current session"}

# Enhanced Chat endpoint WITHOUT Ollama (simple RAG)
@app.post("/chat")
async def chat(req: ChatRequest):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 💬 CHAT QUERY")
    print(f"Query: '{req.query}'")
    
    if not collection or collection.count() == 0:
        print("No documents in ChromaDB for chat")
        return {
            "answer": "I don't have any documents to search through. Please upload some documents first using the Upload Document section."
        }
    
    try:
        # Get relevant document chunks
        results = collection.query(
            query_texts=[req.query],
            n_results=3,
            include=["documents", "distances", "metadatas"]
        )
        print(f"Retrieved {len(results['documents'][0])} relevant chunks")
        print(results)
        if not results["documents"] or not results["documents"][0]:
            print("No relevant information found")
            return {
                "answer": "I couldn't find specific information about that in the uploaded documents. "
                            "Try asking about something that might be in your documents, or upload more relevant files."
            }
        context_chunks = results["documents"][0]    # Extract context from results
        metadatas = results["metadatas"][0]
        print(f"Found {len(context_chunks)} relevant sections")
        
        if "procedure" in req.query.lower() or "step" in req.query.lower() or "how" in req.query.lower():    # Create a focused answer
            answer = f"Here's what I found about '{req.query}':\n\n"    # For procedural questions
            for i, (chunk, metadata) in enumerate(zip(context_chunks[:2], metadatas[:2]), 1):
                source = metadata.get('source', 'a document')
                answer += f"**From {source}:**\n"
                lines = chunk.split('\n')    # Extract procedural content
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['step', 'procedure', 'method', 'how to', 'instructions']):
                        answer += f"- {line.strip()}\n"
                if i < len(context_chunks[:2]):
                    answer += "\n"
        
        else:
            # For general questions
            answer = "Based on the uploaded documents:\n\n"
            for i, (chunk, metadata) in enumerate(zip(context_chunks[:2], metadatas[:2]), 1):
                source = metadata.get('source', 'a document')
                answer += f"**Information from {source}:**\n"
                
                # Take the most relevant part of the chunk
                sentences = chunk.split('. ')
                relevant_sentences = []
                query_lower = req.query.lower()
                
                for sentence in sentences:
                    if len(sentence.split()) > 3:    # Avoid very short sentences
                        if any(word in sentence.lower() for word in query_lower.split()):
                            relevant_sentences.append(sentence.strip() + '.')
                        elif len(relevant_sentences) < 2:    # Take first few sentences
                            relevant_sentences.append(sentence.strip() + '.')
                answer += " ".join(relevant_sentences[:3]) + "\n\n"
        answer += "\n*This information comes from your uploaded documents. For more details, you can view the full documents in the See Documents section.*"
        print(f"Generated answer ({len(answer)} chars)")
        return {"answer": answer}
        
    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "answer": "Sorry, I encountered an error while searching through the documents. "
                        "Please try again or rephrase your question."
        }

# Health check
@app.get("/health")
async def health_check():
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "session_id": current_session_id,
        "session_documents": len(session_documents),
        "total_documents_in_storage": len(ui_documents),
        "chromadb_documents": collection.count() if collection else 0,
        "ollama_enabled": OLLAMA_ENABLED,
        "upload_workers": executor._max_workers
    }
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🩺 Health check")
    return status

#Get current session info
@app.get("/session-info")
async def get_session_info():
    return {
        "status": "success",
        "session_id": current_session_id,
        "session_started": datetime.now().isoformat(),
        "documents_in_session": len(session_documents),
        "total_documents_in_chromadb": collection.count() if collection else 0
    }
    
# Clear all data (for testing)
@app.post("/clear-all")
async def clear_all_data():
    global ui_documents
    try:
        # Clear UI documents
        ui_documents = []
        save_ui_documents()
        
        # Clear ChromaDB
        if collection:
            client.delete_collection(name="documents")
            print("Cleared all data")
        
        return {"status": "success", "message": "All data cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# Debug function to check session state
@app.get("/debug-session")
async def debug_session():
    return {
        "session_id": current_session_id,
        "session_documents_count": len(session_documents),
        "session_documents": [
            {
                "id": doc["id"][:8],
                "filename": doc["filename"],
                "size": doc["size"]
            }
            for doc in session_documents
        ],
        "all_documents_count": len(ui_documents),
        "chromadb_count": collection.count() if collection else 0
    }

# for running the app.py file
# uvicorn backend:app --reload --port 8000
