# 🚀 UI-Based-RAG

<div align="center">

<!-- TODO: Add project logo (e.g., an icon representing RAG or chat) -->

[![GitHub stars](https://img.shields.io/github/stars/ambrose-kutti/UI-Based-RAG?style=for-the-badge)](https://github.com/ambrose-kutti/UI-Based-RAG/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ambrose-kutti/UI-Based-RAG?style=for-the-badge)](https://github.com/ambrose-kutti/UI-Based-RAG/network)
[![GitHub issues](https://img.shields.io/github/issues/ambrose-kutti/UI-Based-RAG?style=for-the-badge)](https://github.com/ambrose-kutti/UI-Based-RAG/issues)
[![GitHub license](https://img.shields.io/badge/license-Unlicensed-blue.svg?style=for-the-badge)](LICENSE) <!-- Using Unlicensed as no LICENSE file was detected -->

**An intuitive web application for document-based Q&A using Retrieval-Augmented Generation (RAG).**

<!-- TODO: Add live demo link if available -->
<!-- [Live Demo](https://demo-link.com) -->

</div>

## 📖 Overview

UI-Based-RAG is an integrated and user-friendly system designed to facilitate natural language querying over your private documents. Users can upload text (`.txt`) and PDF (`.pdf`) documents via a simple web interface. The backend then intelligently processes these documents by chunking them, generating embeddings, and storing them in a vector database. This prepared knowledge base is then utilized by a chatbot, powered by Retrieval-Augmented Generation (RAG), to provide accurate and contextually relevant answers to user queries, significantly enhancing the effectiveness and relevance of the conversational AI.

## ✨ Features

-   **Interactive Chatbot Interface**: Engage with an intuitive chat interface for seamless Q&A.
-   **Document Upload**: Easily upload multiple `.txt` and `.pdf` files directly through the web UI.
-   **RAG-powered Q&A**: Leverage Retrieval-Augmented Generation to get precise answers grounded in your uploaded documents.
-   **Intelligent Document Processing**: Backend handles automatic document parsing, chunking, and embedding generation.
-   **Vector Store Integration**: Utilizes ChromaDB for efficient storage and retrieval of document embeddings.
-   **Local Deployment**: Designed for straightforward setup and operation on a local machine.
-   **Clear Separation**: Frontend (HTML/JS/CSS) and Backend (Python FastAPI) are separated for modular development.

## 🖥️ Screenshots

<!-- TODO: Add actual screenshots of the UI, including document upload and chat interaction -->
<!-- ![Upload Interface](path-to-upload-screenshot.png) -->
<!-- ![Chat Interface](path-to-chat-screenshot.png) -->

## 🛠️ Tech Stack

**Frontend:**

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Backend:**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-FF4500?style=for-the-badge&logo=uvicorn&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-24C78E?style=for-the-badge&logo=langchain&logoColor=white)
![PyPDF2](https://img.shields.io/badge/PyPDF2-D9000D?style=for-the-badge&logo=pypdf&logoColor=white)
![Unstructured](https://img.shields.io/badge/Unstructured-EE8735?style=for-the-badge&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BPHBhdGggZD0iTTcuNTEwMyAyNC4wMDAxdjAuMDA1aDE3LjY2NjR2LTEwLjYxNjhjMC0xLjU1OTUtMS40MDQ1LTMuMDMyMi0yLjk0MTMtMy41ODcyLS41NTU0LS4yMTMtMS41MjcxLS40MTgyLTIuMTc4Ny0uNjU3LTQuMjM2My0xLjU2MS04LjUwNTctMi44MjY1LTkuMzcxNi02LjI3NzUtLjEyOTktLjQ2MjMtLjI5NzMtMS4xMDItLjI5NzMtMi4zMjI0VjBoLTE2LjQ1MjJ2MjQuMDAwMWg3LjQxNDR6IiBmaWxsPSIjRUU4NzM1Ii8%2BPC9zdmc%2B&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-FFD700?style=for-the-badge&logo=python&logoColor=white)

**Vector Database:**

![ChromaDB](https://img.shields.io/badge/ChromaDB-006A6A?style=for-the-badge&logo=chroma&logoColor=white)

**LLM & Embeddings:**

![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) <!-- Assumed based on common RAG setups -->
![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-008080?style=for-the-badge&logo=huggingface&logoColor=white)
![Tiktoken](https://img.shields.io/badge/Tiktoken-000000?style=for-the-badge&logo=python&logoColor=white)

## 🚀 Quick Start

Follow these steps to get the UI-Based-RAG application up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:
-   **Python 3.8+**: The backend is built with Python.
-   **pip**: Python package installer (usually comes with Python).

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/ambrose-kutti/UI-Based-RAG.git
    cd UI-Based-RAG
    ```

2.  **Install backend dependencies**
    Navigate to the project root directory and install all required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment setup**
    The application requires an OpenAI API key for accessing LLM models (or similar for other providers).
    Create a `.env` file in the project root directory by copying the example:
    ```bash
    cp .env.example .env
    ```
    Then, open the `.env` file and add your API key:
    ```ini
    OPENAI_API_KEY="your_openai_api_key_here"
    # Other potential environment variables if you use different models or local options
    # CHROMA_PERSIST_DIRECTORY="./chroma_db"
    ```
    *Note: A `.env.example` file was not found, so this is a best practice assumption. Please create one if it doesn't exist.*

### Run the Application

The application consists of two parts: a Python backend (API) and a static HTML/JS/CSS frontend.

1.  **Start the Backend Server**
    Open your terminal, navigate to the project root, and run the FastAPI application using Uvicorn:
    ```bash
    uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
    ```
    This will start the backend server, typically accessible at `http://localhost:8000`. The `--reload` flag is optional but useful for development.

2.  **Open the Frontend in your browser**
    Locate the `frontend.html` file in the project root directory. You can open it directly in your web browser by double-clicking it or by navigating to its path (e.g., `file:///path/to/UI-Based-RAG/frontend.html`).

    Once the frontend loads, it will automatically connect to the running backend.

## 📁 Project Structure

```
UI-Based-RAG/
├── README.md           # This documentation file
├── backend.py          # Python backend logic (FastAPI application, RAG pipeline)
├── frontend.html       # Static HTML file for the user interface
├── requirements.txt    # List of Python dependencies for the backend
├── script.js           # JavaScript logic for frontend interactivity and API calls
└── style.css           # CSS file for styling the frontend
```

## ⚙️ Configuration

### Environment Variables

The application uses environment variables for sensitive information like API keys.



| Variable                  | Description                                            | Default         | Required |



|-----------------           |--------------------------------------------------------     |-----------------|----------|



| `OPENAI_API_KEY`           | Your API key for accessing OpenAI models (GPT, embeddings)| `(None)`        | Yes      |


| `CHROMA_PERSIST_DIRECTORY` | Directory to persist ChromaDB embeddings. If not set, ChromaDB might operate in-memory| `./chroma_db` (recommended) | No   
|

### ChromaDB Persistence

By default, ChromaDB can run in an ephemeral in-memory mode. For persistent storage of your document embeddings, it is highly recommended to configure a directory. This ensures that your uploaded documents and their embeddings are not lost when the backend server restarts. This is typically configured internally within `backend.py` or via an environment variable like `CHROMA_PERSIST_DIRECTORY`.

## 📚 API Reference

The backend provides a simple set of API endpoints for document processing and chatbot interaction.

### `/upload` - Document Upload

Uploads a document (TXT or PDF) for processing and embedding.

-   **URL**: `/upload`
-   **Method**: `POST`
-   **Request Body**: `multipart/form-data` with a file field named `file`.
-   **Response**: JSON object indicating success or failure.

**Example (Internal JavaScript call from `script.js`):**
```javascript
// This is handled by the frontend script.js when you upload a file.
// Example pseudocode:
/*
fetch('/upload', {
    method: 'POST',
    body: formData // formData contains the uploaded file
})
.then(response => response.json())
.then(data => console.log(data));
*/
```

### `/chat` - Chatbot Interaction

Sends a user query to the RAG chatbot and receives a contextually relevant response.

-   **URL**: `/chat`
-   **Method**: `POST`
-   **Request Body**: JSON object with a `query` field.
    ```json
    {
      "query": "What is Retrieval-Augmented Generation?"
    }
    ```
-   **Response**: JSON object containing the `answer` from the chatbot.

**Example (Internal JavaScript call from `script.js`):**
```javascript
// This is handled by the frontend script.js when you submit a chat message.
// Example pseudocode:
/*
fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: 'Your question here' })
})
.then(response => response.json())
.then(data => console.log(data.answer));
*/
```

## 🤝 Contributing

We welcome contributions! If you're interested in improving this project, please consider the following:

-   **Reporting Issues**: If you find any bugs or have suggestions, please open an issue on GitHub.
-   **Feature Enhancements**: Feel free to propose and implement new features (e.g., support for more document types, improved UI, advanced RAG techniques).
-   **Documentation**: Improve clarity or add more details to the documentation.

### Development Setup for Contributors

1.  Follow the [Quick Start](#🚀-quick-start) instructions to get the project running locally.
2.  Make your changes to `backend.py`, `frontend.html`, `script.js`, or `style.css`.
3.  Test your changes thoroughly by restarting the backend and refreshing the frontend.

## 📄 License

This project is currently **Unlicensed**. Users are advised to clarify licensing terms with the author for any redistribution or commercial use.

## 🙏 Acknowledgments

-   Built using **FastAPI** for a fast and efficient Python backend.
-   **LangChain** for orchestrating the RAG pipeline.
-   **ChromaDB** for efficient vector storage.
-   **OpenAI** for providing powerful language models and embeddings (if used).
-   Thanks to the open-source community for the invaluable libraries that made this project possible.

## 📞 Support & Contact

-   🐛 Issues: [GitHub Issues](https://github.com/ambrose-kutti/UI-Based-RAG/issues)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [ambrose-kutti](https://github.com/ambrose-kutti)

</div>
```

