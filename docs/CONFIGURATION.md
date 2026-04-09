# Configuration Guide for ResumeEnhancer

ResumeEnhancer is designed to be easily configurable via environment variables, CLI arguments, and the Streamlit UI. This document exhaustively lists all available configuration vectors.

## 1. Environment Variables

The most secure way to configure sensitive credentials like API keys is through environment variables.

| Variable Name | Required | Default | Description |
|---------------|----------|---------|-------------|
| `GROQ_API_KEY` | **Yes** | `None` | Your private Groq API key required to authenticate with the inference service. Without this, the application will immediately fail. |
| `STREAMLIT_SERVER_PORT` | No | `8501` | The port on which the Streamlit web dashboard will be exposed. Useful when running in Docker. |
| `LOG_LEVEL` | No | `INFO` | Sets the verbosity of the internal logger. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |

### Setting Environment Variables
**Linux/macOS:**
```bash
export GROQ_API_KEY="gsk_your_real_api_key_here"
```
**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_your_real_api_key_here
```
**Docker:**
```bash
docker run -e GROQ_API_KEY="gsk_..." -p 8501:8501 resumeenhancer
```

## 2. AI Model Hyperparameters

When running via the Streamlit UI or calling the Python API directly, you have access to several AI hyperparameter configurations.

### 2.1. Model Selection (`model`)
The Groq platform supports various open-source models. ResumeEnhancer exposes three primary options:
- **`llama3-8b-8192` (Default)**: Best for extremely fast, general-purpose resume analysis. Very low latency.
- **`llama3-70b-8192`**: Best for deep, nuanced analysis. It writes better, more professional bullet points but might take a fraction of a second longer.
- **`mixtral-8x7b-32768`**: Best when dealing with massive documents. It has a 32k token context window, preventing truncation if you feed it a 10-page CV and a massive JD.

### 2.2. Temperature (`temperature`)
Controls the randomness or "creativity" of the generated text.
- **Range:** `0.0` to `1.0`
- **Default:** `0.7`
- **Recommendation:** 
  - Set to `0.2 - 0.4` if you want strict, highly factual, and rigid professional rewriting.
  - Set to `0.7 - 0.8` (default) for a good balance of professional tone and creative action-verb usage.
  - Avoid `1.0` as it might hallucinate skills you don't actually possess.

### 2.3. Max Tokens (`max_tokens`)
Defines the absolute maximum length of the AI's response.
- **Range:** `500` to `8192` (depending on the model's limit).
- **Default:** `2048`
- **Recommendation:** `2048` is generally enough for a full 2-page markdown report. If you notice the output cutting off mid-sentence, increase this to `4000`.

## 3. Application Configuration (config.py / settings)

Internally, ResumeEnhancer may load a configuration dictionary if extended in the future. Currently, behavior is governed by the parameters passed at runtime.

### File Support Constraints
The `extract_text_from_file` utility is hardcoded to support:
- `.pdf`
- `.docx`
- `.txt`
Attempting to process `.rtf` or `.doc` files will raise a `ValueError`. Ensure your files are converted to one of the supported formats before processing.
