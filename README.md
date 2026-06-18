🤖 AI Assistant

A modern ChatGPT-inspired AI Assistant built with **Flask**, **Google Gemini AI**, and **Retrieval-Augmented Generation (RAG)**. The application supports conversational AI, document-based question answering, user authentication, persistent chat history, and a responsive ChatGPT-like interface.

---

## 🚀 Features

* 💬 ChatGPT-style conversational interface
* 🤖 Google Gemini 2.5 Flash integration
* 📄 Document Question Answering (RAG)
* 📁 Upload PDF, DOCX, and TXT files
* 🔍 Semantic search using FAISS vector database
* 🧠 Context-aware conversations
* 🔐 User Authentication (Login & Signup)
* 👤 User Profiles
* 💾 Persistent chat history
* 📝 Automatic chat title generation
* 🗑️ Delete conversations
* 📱 Responsive modern UI
* 🎨 Markdown rendering
* 💻 Syntax highlighting for code
* ⚡ Fast Flask backend

---

## 🛠 Tech Stack

### Backend

* Python
* Flask
* Flask-Login
* Flask-Migrate
* SQLAlchemy

### AI

* Google Gemini 2.5 Flash
* LangChain
* FAISS
* HuggingFace Embeddings
* Sentence Transformers

### Database

* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2

### Libraries

* Markdown
* Highlight.js
* WTForms
* PyPDF
* Docx2txt

---

## 📂 Project Structure

```text
AI_Chatbot/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│
├── forms/
│
├── models/
│   ├── user.py
│   ├── conversation.py
│   └── message.py
│
├── routes/
│   ├── auth.py
│   ├── api.py
│   ├── chat.py
│   ├── profile.py
│   └── upload.py
│
├── services/
│   ├── gemini_service.py
│   ├── rag_service.py
│   ├── vector_store_service.py
│   ├── document_loader.py
│   ├── markdown_service.py
│   └── conversation_service.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── uploads/
│
└── vectorstore/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Goveshwar/AI_Chatbot.git

cd AI_Chatbot
```

---

### Create Virtual Environment

```bash
python -m venv myenv
```

Activate

#### Windows

```bash
myenv\Scripts\activate
```

#### Linux / macOS

```bash
source myenv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ Run the Application

```bash
python app.py
```

The application will start at

```
http://127.0.0.1:8000
```

---

## 📄 Supported Documents

* PDF
* DOCX
* TXT

Uploaded documents are automatically:

* Loaded
* Split into chunks
* Embedded using HuggingFace
* Stored in a FAISS vector database
* Used for semantic retrieval

---

## 🧠 AI Capabilities

The assistant can:

* Answer general questions
* Generate code
* Debug programs
* Explain concepts
* Summarize documents
* Analyze resumes
* Answer questions from uploaded files
* Maintain conversation context
* Format responses using Markdown

---

## 🔐 Authentication

* User Registration
* Login
* Logout
* Session Management
* Protected Routes

---

## 📸 Screenshots

Add screenshots here.

```
Home Screen

Chat Interface

Document Upload

Profile Page
```

---

## 🚀 Future Improvements

* Voice Chat
* Image Upload Support
* Streaming Responses
* Multiple AI Models
* Dark/Light Theme
* Chat Export
* Conversation Search
* Chat Sharing
* Admin Dashboard
* Docker Deployment

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Goveshwar Teli**

GitHub:
https://github.com/Goveshwar

LinkedIn:
https://www.linkedin.com/in/goveshwar-teli

Email:
guheswarteli@gmail.com
