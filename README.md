# 💬 UI-Based RAG Chatbot

<div align="center">

<img width="200" height="200" alt="Copilot_20260316_110345" src="https://github.com/user-attachments/assets/06efbaa2-ff78-4d34-b7f0-eb4b3a2dd6a1" /> <!-- TODO: Add project logo -->

[![GitHub stars](https://img.shields.io/github/stars/ambrose-kutti/UI-Based-RAG?style=for-the-badge)](https://github.com/ambrose-kutti/UI-Based-RAG/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ambrose-kutti/UI-Based-RAG?style=for-the-badge)](https://github.com/ambrose-kutti/UI-Based-RAG/network)
[![GitHub issues](https://img.shields.io/github/issues/ambrose-kutti/UI-Based-RAG?style=for-the-badge)](https://github.com/ambrose-kutti/UI-Based-RAG/issues)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE) <!-- Assumed MIT, add LICENSE file if not present -->

**An intuitive web application for document-driven Retrieval Augmented Generation (RAG) using Ollama and ChromaDB.**


</div>

## 📖 Overview

This project provides a user-friendly, integrated system for building and interacting with a Retrieval Augmented Generation (RAG) chatbot. Users can upload their own `.txt` or `.pdf` documents via a simple web interface. The backend then processes these documents by chunking them, generating embeddings using Ollama, and storing them in a persistent ChromaDB vector store. Subsequently, users can engage in a chat session where the chatbot leverages the uploaded document context to provide accurate and relevant responses, powered by a local Large Language Model (LLM) also served by Ollama.

The system is designed for ease of use, making advanced RAG capabilities accessible without complex setup, ideal for personal knowledge base Q&A, research assistance, or exploring RAG technology.

## ✨ Features

-   **Intuitive Web Interface**: A clean and simple HTML/CSS/JS frontend for easy interaction.
-   **Document Upload**: Seamlessly upload `.txt` and `.pdf` files directly through the UI.
-   **Automated Document Processing**: Backend handles chunking, embedding generation, and vector storage for uploaded documents.
-   **Contextual Chatbot**: Engage in conversations with a chatbot that retrieves information directly from your uploaded documents.
-   **Retrieval Augmented Generation (RAG)**: Leverages advanced RAG techniques to provide accurate and contextually relevant answers.
-   **Local LLM Integration**: Powered by Ollama, enabling the use of local open-source LLMs (e.g., Llama2) and embedding models (e.g., Nomic Embed Text) for privacy and offline capability.
-   **Persistent Vector Store**: Uses ChromaDB to store document embeddings, allowing for efficient retrieval and persistent knowledge.
-   **Chat History**: Displays ongoing chat conversation for a better user experience.

## 🖥️ Screenshots

[Screenshot 1]

<img width="500" height="500" alt="Screenshot 2026-03-14 124409" src="https://github.com/user-attachments/assets/9798835d-cea0-45f9-8103-427170017d54" />

[Screenshot 2]

<img width="500" height="500" alt="Screenshot 2026-03-14 145319" src="https://github.com/user-attachments/assets/bc218438-8585-4e56-9421-eb5a37888671" />

[Screenshot 2]

<img width="500" height="500" alt="Screenshot 2026-03-14 145349" src="https://github.com/user-attachments/assets/5e3d6333-154e-4466-ad7b-c6c3eed5532c" />



## 🛠️ Tech Stack

**Frontend:**
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

**Backend:**
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-FF6200?style=for-the-badge&logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-lightgreen?style=for-the-badge&logo=dotenv&logoColor=white)](https://github.com/theskumar/python-dotenv)

**AI/ML & RAG:**
[![LangChain](https://img.shields.io/badge/LangChain-26A74C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai/)
[![pypdf](https://img.shields.io/badge/pypdf-lightgrey?style=for-the-badge)](https://pypdf.readthedocs.io/)
[![tiktoken](https://img.shields.io/badge/tiktoken-lightgrey?style=for-the-badge)](https://github.com/openai/tiktoken)

**Vector Database:**
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0062FF?style=for-the-badge&logo=chroma&logoColor=white)](https://www.trychroma.com/)

## 🚀 Quick Start

Follow these steps to get the UI-Based RAG Chatbot up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.9+**
-   **Ollama**: Install Ollama from [ollama.ai](https://ollama.ai/). This will serve your local LLM and embedding models.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/ambrose-kutti/UI-Based-RAG.git
    cd UI-Based-RAG
    ```

2.  **Set up a Python virtual environment** (recommended)
    ```bash
    python -m venv .venv
    # On Windows:
    # .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Ollama models**
    Once Ollama is installed and running, download the required models:
    ```bash
    ollama pull llama2
    ollama pull nomic-embed-text
    ```

5.  **Environment setup** (Optional but recommended for customization)
    Create a `.env` file in the project root based on the example below.
    ```bash
    cp .env.example .env
    ```
    Configure your environment variables:

    ```ini
    # .env
    # Optional: If Ollama is running on a different URL/port than default
    # OLLAMA_BASE_URL=http://localhost:11434

    # Optional: If you prefer to use OpenAI for embeddings/chat (not default in app.py)
    # OPENAI_API_KEY=your_openai_api_key_here
    ```

6.  **Start the backend server**
    ```bash
    uvicorn app:app --reload
    ```
    The backend will start on `http://127.0.0.1:8000`.

7.  **Open your browser**
    Visit `http://127.0.0.1:8000` to access the UI-Based RAG Chatbot application.

## 📁 Project Structure

```
UI-Based-RAG/
├── .gitignore          # Specifies intentionally untracked files to ignore
├── app.py              # Main FastAPI backend application, handles API endpoints
├── frontend.html       # Single-page HTML frontend for the application
├── requirements.txt    # Lists Python dependencies for the backend
├── static/             # Directory for static assets
      └── script.js
      └── style.css
└── .env.example        # Example environment variables for configuration
```

## ⚙️ Configuration

### Environment Variables
The application can be configured using environment variables. These can be set directly in your shell or, more conveniently, in a `.env` file in the project root.

| Variable          | Description                                                                                                   | Default                   | Required |
|-------------------|---------------------------------------------------------------------------------------------------------------|---------------------------|----------|
| `OLLAMA_BASE_URL` | Specifies the base URL for the Ollama server. Useful if Ollama is not running on the default `localhost:11434`. | `http://localhost:11434`  | No       |
| `OPENAI_API_KEY`  | Your OpenAI API key. While the application defaults to Ollama, this can be used to switch to OpenAI services. | `None` (uses Ollama)      | No       |

### ChromaDB Persistence
ChromaDB data (embeddings) is persisted locally in a directory named `chroma_db` within the project root. This directory will be created automatically upon the first document upload. You can delete this directory to reset the vector database.

## 🔧 Development

### Backend (Python/FastAPI)
The backend is built with FastAPI and Uvicorn. The `app.py` file contains all the core logic, including API routes for document upload and chat interaction.

### Frontend (HTML/CSS/JS)
The frontend is a single `frontend.html` file, which uses vanilla JavaScript for dynamic interactions and Fetch API calls to the backend. Styling is primarily inline or within `<style>` tags.

### Available Scripts
To run the development server:
```bash
uvicorn app:app --reload
```
The `--reload` flag enables auto-reloading of the server on code changes, which is useful during development.

## 📚 API Reference

The backend exposes the following API endpoints:

### Serve Frontend
-   **GET `/`**
    -   **Description:** Serves the `frontend.html` file, which is the main user interface for the application.
    -   **Returns:** HTML content.

### Document Upload
-   **POST `/uploadfile`**
    -   **Description:** Handles the upload of `.txt` or `.pdf` documents. Processes the document by splitting it into chunks, generating embeddings using Ollama, and storing them in ChromaDB.
    -   **Request Body:** `file` (multipart/form-data) - The document file to upload.
    -   **Returns:** `JSON` object with a success message and the number of chunks processed.
    -   **Example Response:**
        ```json
        {"message": "File processed successfully", "chunks": 50}
        ```

### Chat Interaction
-   **POST `/chat`**
    -   **Description:** Processes a user's chat message. Retrieves relevant document chunks from ChromaDB based on the message, augments the prompt, and generates a response using the Ollama LLM.
    -   **Request Body:** `JSON` object with `message` field.
        ```json
        {"message": "What is the main topic of the uploaded documents?"}
        ```
    -   **Returns:** `JSON` object with the chatbot's `response`.
    -   **Example Response:**
        ```json
        {"response": "Based on the documents, the main topic is..."}
        ```

## 🤝 Contributing

We welcome contributions to improve this RAG chatbot! If you have suggestions or want to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a Pull Request.

Please ensure your code adheres to good practices and includes appropriate comments.

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details. <!-- TODO: Create a LICENSE file in the repository root if not present -->

## 🙏 Acknowledgments

-   **LangChain**: For providing an excellent framework for building LLM applications.
-   **Ollama**: For enabling easy local LLM and embedding model deployment.
-   **ChromaDB**: For the efficient and user-friendly vector database.
-   **FastAPI**: For the modern, fast (high-performance) web framework.
-   **pypdf**: For robust PDF document processing.

## 📞 Support & Contact

-   📧 Email: [contact@example.com] <!-- TODO: Add a relevant contact email -->
-   🐛 Issues: [GitHub Issues](https://github.com/ambrose-kutti/UI-Based-RAG/issues)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [ambrose-kutti](https://github.com/ambrose-kutti) in 2024

</div>
