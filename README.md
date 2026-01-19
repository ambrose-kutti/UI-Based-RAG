# UI-Based RAG Chatbot 🧠💬
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-orange.svg)](../../issues)

A **Retrieval-Augmented Generation (RAG)** system with a simple **web UI**.  
Upload `.txt` or `.pdf` files, and chat with an AI assistant that retrieves context from your documents to generate accurate, grounded answers.

---

## ✨ Features
- 📂 Upload documents directly via the UI
- 📝 Supports `.txt` and `.pdf` formats
- 🔎 Automatic chunking + embeddings
- 🗄️ Vector storage with **ChromaDB**
- 🤖 Chatbot powered by RAG pipeline
- 🛠️ Modular design for easy extension

---
## 🚀 Usage
  1. Create a **templates folder** and paster the `html file` and create a **static folder** and paste your `css` and `js file`
  2. Start the backend
     Start the backend
       `uvicorn app1:app --reload --port 8000`
     This launches the server.
   
  3. Open the UI
     
       `Open portal.html in the browser.`
     
       `Upload .txt or .pdf files.`
     
       `Start chatting with the RAG assistant`.
---

## 📊 Example Workflow
  1. Upload a PDF research paper.

  2. Backend chunks + embeds content into ChromaDB.

  3. Chatbot retrieves relevant passages and generates context‑aware answers.

---
## 🧭 Future Enchancements are welcomed

  1. Add support for multiple formats documents
  2. Enhance UI with chat history
  3. Dockerize for deployment
  4. Multi‑user authentication
---

## 📦 Installation
Clone the repo and install dependencies:

```bash
git clone https://github.com/ambrose-kutti/UI-Based-RAG.git
cd UI-Based-RAG
pip install -r requirements.txt
# for running the app.py file
uvicorn app:app --reload --port 8000   (replace ur first app with your file name)



