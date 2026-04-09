# ResumeEnhancer API & Code Reference

This document provides a comprehensive reference for the programmatic interfaces, CLI commands, and internal utility functions of ResumeEnhancer.

## 1. Command Line Interface (CLI)

The CLI provides a robust way to integrate ResumeEnhancer into bash scripts or CI/CD pipelines.

### `optimize` Command

The core command to analyze a resume against a job description.

```bash
python -m resumeenhancer optimize [RESUME_PATH] [JD_PATH] [OPTIONS]
```

**Arguments:**
- `RESUME_PATH` (string, required): Path to the candidate's resume (PDF, DOCX, TXT).
- `JD_PATH` (string, required): Path to the target job description (PDF, DOCX, TXT).

**Options:**
- `--output`, `-o` (string): Specify the path where the generated markdown report will be saved. Default is stdout.
- `--score-only` (flag): If passed, the AI will only return an ATS compatibility score (0-100) instead of a full rewrite report. Useful for batch processing.
- `--prompt-profile` (string): Select a specific prompting style. Options: `default`, `strictly_technical`, `executive_summary`.
- `--api-key` (string): Pass the Groq API key directly instead of using the `GROQ_API_KEY` environment variable.

## 2. Python API

You can import ResumeEnhancer modules directly into your own Python scripts.

### Module: `resumeenhancer.utils.ai_service`

#### Class `AIService`
Handles all communication with the Groq API.

**Constructor:**
```python
AIService(api_key: str = None)
```
- `api_key` (str, optional): The Groq API key. If not provided, it falls back to `os.environ.get("GROQ_API_KEY")`. Raises `ValueError` if no key is found.

**Methods:**

```python
def analyze_resume(self, resume_content: str, job_description: str, model: str = "llama3-8b-8192", temperature: float = 0.7, max_tokens: int = 2048) -> str
```
Analyzes the provided texts and returns optimization suggestions.
- **Parameters:**
  - `resume_content` (str): The raw text extracted from the CV.
  - `job_description` (str): The raw text extracted from the JD.
  - `model` (str): The Groq model to use. Recommended: `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`.
  - `temperature` (float): Controls the creativity of the AI (0.0 to 1.0).
  - `max_tokens` (int): The maximum length of the generated response.
- **Returns:** `str` - A Markdown-formatted string containing the analysis report.
- **Raises:** `APIError` if the Groq API rejects the request or times out.

### Module: `resumeenhancer.parsers.file_handler`

#### Function `extract_text_from_file`

```python
def extract_text_from_file(file_path: str) -> str
```
Automatically detects the file type via its extension and routes it to the appropriate parser.
- **Parameters:**
  - `file_path` (str): Absolute or relative path to the document.
- **Returns:** `str` - The extracted raw text.
- **Raises:** 
  - `FileNotFoundError` if the file does not exist.
  - `ValueError` if the file extension is unsupported.

### Module: `resumeenhancer.utils.logger`

#### Function `setup_logger`

```python
def setup_logger(level: int = logging.INFO) -> logging.Logger
```
Initializes and returns the standard application logger.
- **Parameters:**
  - `level` (int): The standard `logging` level (e.g., `logging.DEBUG`, `logging.INFO`).
- **Returns:** `logging.Logger` instance configured to output to both console and `resumeenhancer.log`.

## 3. Web Dashboard (Streamlit)
The web dashboard is invoked by running:
```bash
streamlit run app.py
```
It does not expose an external API, but internally it utilizes `st.file_uploader` for ingestion and `tempfile.NamedTemporaryFile` for bridging the file gap between the web UI and the local `extract_text_from_file` utility.
