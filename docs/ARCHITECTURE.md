# Architecture of ResumeEnhancer

## 1. System Overview

ResumeEnhancer is designed as a modular, AI-driven application that takes a candidate's resume and a target job description (JD) and generates actionable, highly targeted suggestions to improve the resume's match rate. The architecture follows a simple but powerful pipeline, dividing responsibilities between text extraction, natural language processing, external API communication, and user interface rendering.

The system is highly scalable, allowing it to be run either as a standalone Command Line Interface (CLI) application or as an interactive web dashboard powered by Streamlit.

## 2. Core Components

### 2.1. User Interface Layer
The application provides two distinct ways for users to interact with the core engine:
- **CLI (Command Line Interface)**: Built for automation, batch processing, and developers. It accepts file paths and flags via `argparse` or `click`, reads the files locally, and outputs the result to the standard output or a Markdown file.
- **Streamlit Web Dashboard (`app.py`)**: A rich, interactive web application that allows users to upload documents (PDF, DOCX, TXT) via a drag-and-drop interface, configure AI parameters (like Temperature and Max Tokens) using sliders and dropdowns, and view the AI's suggestions in real-time.

### 2.2. Document Parsing Engine (`resumeenhancer.parsers`)
Resumes and JDs come in various formats. The parsing engine is responsible for extracting raw text from these formats while attempting to preserve as much semantic structure as possible.
- **PDF Parser**: Utilizes libraries like `PyPDF2` or `pdfplumber` to extract text from PDF documents.
- **Word Document Parser**: Uses `python-docx` to read `.docx` files, extracting paragraphs and bullet points.
- **Plain Text Parser**: Handles raw `.txt` files directly.
The parsed text is normalized and cleaned before being sent to the AI service.

### 2.3. AI Processing Service (`resumeenhancer.utils.ai_service.AIService`)
This is the brain of ResumeEnhancer. Instead of running heavy LLMs locally, the system delegates the intensive inference tasks to the **Groq API**, taking advantage of their ultra-fast LPUs (Language Processing Units).
- The `AIService` constructs a detailed prompt combining the extracted resume text, the JD text, and specific instructional constraints (e.g., "focus on skill gaps", "rewrite bullet points for impact").
- It communicates with the Groq API using the provided `GROQ_API_KEY`.
- It supports multiple models:
  - `llama3-8b-8192`: For blazing-fast, lightweight inference.
  - `llama3-70b-8192`: For deep, highly contextual, and high-quality analysis.
  - `mixtral-8x7b-32768`: For processing extremely long documents due to its massive context window.

### 2.4. Configuration and Logging (`resumeenhancer.utils`)
- **Logger (`logger.py`)**: Provides standardized logging across the application, tracking errors (like API failures or parsing issues) and operational metrics.
- **Config Loader (`config.py`)**: Manages default settings, environment variables (like `GROQ_API_KEY`), and user preferences.

## 3. Data Flow

1. **Input Ingestion**: The user provides a CV and a JD via the CLI or Streamlit UI.
2. **Temporary Storage (Streamlit only)**: Uploaded files are temporarily saved to the disk using Python's `tempfile` module to allow the parsers to read them.
3. **Text Extraction**: The `extract_text_from_file` function reads the files and returns raw string representations.
4. **Prompt Construction**: The `AIService` wraps the extracted text in a predefined system prompt that instructs the LLM on how to analyze the documents.
5. **API Invocation**: An HTTP/WebSocket request is dispatched to the Groq API endpoint.
6. **Response Processing**: The Groq API returns a Markdown-formatted string containing the analysis, skill gaps, and rewritten bullet points.
7. **Output Delivery**: The application displays the Markdown to the user in the Streamlit UI or writes it to a file via the CLI.
8. **Cleanup**: Temporary files are securely deleted.

## 4. Design Decisions and Trade-offs

- **External LLM vs. Local LLM**: By choosing the Groq API over local models (like a local HuggingFace setup), ResumeEnhancer sacrifices offline capability for massive speed gains, lower hardware requirements, and access to state-of-the-art models like Llama 3 70B that cannot run on standard consumer hardware.
- **Streamlit for UI**: Streamlit was chosen for its rapid prototyping capabilities in Python. While it may not offer the granular customization of a React/Next.js frontend, it perfectly aligns with the data-driven, text-heavy nature of the application and allows the entire stack to remain in pure Python.
- **Stateless Architecture**: The application does not use a database. No user data, resumes, or JDs are stored persistently. This was a deliberate decision to ensure maximum user privacy and to simplify deployment.
