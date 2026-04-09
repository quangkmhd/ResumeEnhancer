# ResumeEnhancer 🚀

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

Optimize your CV instantly using advanced AI to perfectly match job descriptions. Built for job seekers and career coaches who need to increase interview callback rates by up to 300% with automated, intelligent resume tailoring.

![ResumeEnhancer AI Dashboard Demo](assets/demo.png)

## ✨ Key Features

- **Analyze resumes against JD instantly**: Extract deep contextual meaning from both your CV and the target Job Description in seconds.
- **Generate actionable improvements**: Receive precise, bullet-point recommendations to rewrite your experience for maximum impact.
- **Support multiple file formats**: Parse PDF, DOCX, and TXT files flawlessly without losing formatting context.
- **Leverage blazing-fast Groq API**: Process complex LLM inference tasks in milliseconds using Groq's high-speed infrastructure.
- **Export tailored results**: Save your optimized resume suggestions directly to your local machine for immediate application.
- **Choose your interface**: Work seamlessly via a robust Command Line Interface (CLI) or an intuitive Streamlit web dashboard.
- **Maintain complete privacy**: Your documents are processed securely via API without being stored persistently on external servers.

## 🚀 Quick Start

Get your first resume optimized in under 3 minutes.

1. **Install the package** (ensure Python 3.8+ is installed):
   ```bash
   git clone https://github.com/your-username/ResumeEnhancer.git
   cd ResumeEnhancer
   pip install -e .
   ```

2. **Set your API Key**:
   ```bash
   export GROQ_API_KEY="gsk_your_api_key_here"
   ```

3. **Run the optimization command**:
   ```bash
   python -m resumeenhancer optimize ./my_resume.pdf ./target_jd.txt
   ```

**Expected Output:**
```text
[INFO] Parsing my_resume.pdf... Done.
[INFO] Parsing target_jd.txt... Done.
[INFO] Sending to Groq API for analysis...
==========================================
🎯 OPTIMIZATION RESULTS:
- Skill Gap Detected: Add "Docker" to your Experience section.
- Wording Suggestion: Change "Managed team" to "Led a cross-functional team of 5..."
- Match Score: 78% -> Potential Match Score: 95%
==========================================
[INFO] Report saved to ./optimization_report.md
```
*The tool analyzed both files and generated a markdown report with specific, actionable changes.*

## 📦 Installation

Choose the installation method that fits your workflow.

### Method 1: From Source (Recommended)
Best for developers who want to contribute or use the latest features.
```bash
git clone https://github.com/your-username/ResumeEnhancer.git
cd ResumeEnhancer
pip install -r requirements.txt
pip install -e .
```

### Method 2: Virtual Environment
Best for isolated environments without messing with global Python dependencies.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Method 3: Using pip (Future Release)
```bash
pip install resumeenhancer
```

## 💡 Usage Examples

### Example 1: Basic CLI Optimization
**Scenario:** You have a PDF resume and a PDF job description and want a quick analysis.
```bash
python -m resumeenhancer optimize ./resume.pdf ./job_desc.pdf --output ./result.txt
```
**Output:** Generates `result.txt` containing missing keywords, suggested bullet point rewrites, and an overall ATS compatibility score.

### Example 2: Launching the Web Dashboard
**Scenario:** You prefer a graphical interface to upload files and view changes side-by-side.
```bash
streamlit run app.py
```
**Output:** Starts a local web server at `http://localhost:8501`. You can drag and drop your files into the browser and click "Analyze" to see real-time suggestions.

### Example 3: Batch Processing Multiple JDs
**Scenario:** You are applying to 5 different roles and want to see which JD matches your base resume best.
```bash
for jd in ./jds/*.txt; do
    python -m resumeenhancer optimize ./base_resume.pdf "$jd" --score-only
done
```
**Output:**
```text
JD: software_engineer.txt - Score: 85%
JD: data_scientist.txt - Score: 40%
JD: backend_dev.txt - Score: 92%
```
*This helps you prioritize which jobs to apply for based on your current resume.*

### Example 4: Customizing the LLM Prompt
**Scenario:** You want the AI to focus strictly on technical skills rather than soft skills.
```bash
python -m resumeenhancer optimize ./resume.pdf ./jd.pdf --prompt-profile "strictly_technical"
```
**Output:** The generated report will bypass leadership and communication suggestions, focusing purely on programming languages, frameworks, and architecture patterns.

## 🛠️ Troubleshooting

- **`ValueError: API Key not found`**
  - *Cause:* The `GROQ_API_KEY` environment variable is not set.
  - *Fix:* Run `export GROQ_API_KEY="your_key"` before executing, or pass it via `--api-key`.
- **`PyPDF2.errors.PdfReadError`**
  - *Cause:* The uploaded PDF is encrypted or scanned as an image.
  - *Fix:* Ensure the PDF contains selectable text. Use OCR tools if it's a scanned document.
- **`RateLimitExceeded`**
  - *Cause:* You have sent too many requests to the Groq API in a short time.
  - *Fix:* Wait 60 seconds and try again, or upgrade your Groq API tier.

## 📚 Documentation Links

Dive deeper into ResumeEnhancer's capabilities with our comprehensive guides:

- **[Complete CLI Reference](./docs/CLI_REFERENCE.md)**
  Master the command-line interface to automate your resume optimization. Discover all available flags, batch processing commands, and output formatting options to integrate seamlessly into your workflow.

- **[Supported File Formats](./docs/FORMATS.md)**
  Learn exactly how our parser extracts text from complex documents. This guide covers the data flow for handling PDFs, DOCX, and TXT files, ensuring your formatting context is never lost during LLM inference.

- **[Customizing AI Prompts](./docs/PROMPTS.md)**
  Take full control of the Groq API's output by tailoring the underlying LLM prompts. Uncover exhaustive hyperparameter tuning techniques to adjust the strictness of the analysis, focus on specific technical skills, and maximize your Match Score.

- **[Groq API Setup Guide](https://console.groq.com/docs/quickstart)**
  Get up and running rapidly with our blazing-fast inference backend. Follow step-by-step instructions to obtain your API keys and securely configure your environment for millisecond-level response times.

## 🤝 Contributing

We welcome contributions to make ResumeEnhancer even better!
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Commit your changes: `git commit -m 'Add amazing feature'`.
4. Push to the branch: `git push origin feature/amazing-feature`.
5. Open a Pull Request.

Please read our [Contributing Guide](./CONTRIBUTING.md) for more details on our code of conduct and development process.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 👏 Credits

Special thanks to the [Groq](https://groq.com/) team for providing the blazing-fast inference API that powers this tool's intelligence.
