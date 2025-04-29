# ResumeEnhancer

ResumeEnhancer là công cụ tối ưu hóa CV dựa trên AI, giúp phân tích và cải thiện CV của bạn để phù hợp hơn với mô tả công việc (JD) cụ thể. Công cụ sử dụng Groq API để phân tích nội dung và đề xuất những thay đổi, giúp tăng cơ hội được tuyển dụng.

## Cách hoạt động

ResumeEnhancer hoạt động theo quy trình sau:

1. **Đọc tệp đầu vào**: Hỗ trợ đọc CV và JD từ nhiều định dạng (PDF, DOCX, TXT)
2. **Phân tích nội dung**: Trích xuất văn bản từ các tệp đầu vào
3. **Gửi đến Groq API**: Sử dụng mô hình ngôn ngữ lớn (LLM) để phân tích sự phù hợp
4. **Tạo đề xuất cải tiến**: Nhấn mạnh các kỹ năng, kinh nghiệm phù hợp với JD
5. **Xuất kết quả**: Hiển thị và lưu các đề xuất cải tiến

## Cài đặt

### Từ mã nguồn
```bash
# Clone repository
git clone <repository-url>
cd ResumeEnhancer

# Cài đặt gói
pip install -e .
```

### Yêu cầu
- Python 3.8+
- Groq API key (đăng ký tại https://console.groq.com/)

## Sử dụng

### Dòng lệnh (CLI)
```bash
# Sử dụng trực tiếp với Groq API key
python -m resumeenhancer optimize path/to/resume.pdf path/to/jd.pdf --api-key your_groq_api_key

# Hoặc đặt API key qua biến môi trường
export GROQ_API_KEY="your_groq_api_key"  # Linux/Mac
$env:GROQ_API_KEY="your_groq_api_key"    # Windows PowerShell
python -m resumeenhancer optimize path/to/resume.pdf path/to/jd.pdf
```

### Giao diện Streamlit
```bash
# Chạy giao diện web
streamlit run app.py
```

## Tính năng chính

- **Đa dạng định dạng đầu vào**: Hỗ trợ PDF, DOCX, và TXT cho cả CV và mô tả công việc
- **Phân tích thông minh**: So sánh CV với JD và đề xuất cải tiến
- **Tùy chỉnh AI**: Điều chỉnh model, temperature, max tokens
- **Cấu hình linh hoạt**: Sử dụng file cấu hình TOML hoặc tham số dòng lệnh
- **Giao diện web**: Sử dụng Streamlit để tạo giao diện thân thiện

## Cấu trúc dự án

```
ResumeEnhancer/
├── resumeenhancer/          # Gói Python chính
│   ├── __init__.py          # Khởi tạo gói
│   ├── __main__.py          # Entry point
│   ├── main.py              # Xử lý luồng chính
│   ├── config_default.toml  # Cấu hình mặc định
│   ├── parsers/             # Bộ xử lý định dạng file
│   │   ├── pdf_parser.py    # Xử lý PDF
│   │   ├── docx_parser.py   # Xử lý DOCX
│   │   ├── text_parser.py   # Xử lý file văn bản
│   │   └── file_handler.py  # Tự động chọn parser
│   ├── utils/               # Các tiện ích
│   │   ├── ai_service.py    # Tích hợp Groq API
│   │   ├── config.py        # Quản lý cấu hình
│   │   └── logger.py        # Quản lý log
│   └── static/              # Assets cho UI
│       └── styles.css       # CSS cho Streamlit
├── app.py                   # Ứng dụng Streamlit
├── setup.py                 # Setup script
└── requirements.txt         # Dependencies
```

## Luồng xử lý dữ liệu

1. **Đầu vào**:
   - CV (PDF/DOCX/TXT)
   - Mô tả công việc (PDF/DOCX/TXT hoặc văn bản)
   - Groq API key và cấu hình

2. **Xử lý**:
   - `parsers`: Trích xuất văn bản từ các file đầu vào
   - `ai_service`: Gửi dữ liệu đến Groq API và nhận kết quả
   - `main`: Điều phối luồng xử lý

3. **Đầu ra**:
   - Kết quả phân tích và đề xuất
   - Lưu kết quả vào file

## Tích hợp AI

ResumeEnhancer sử dụng Groq API với các mô hình:
- llama3-8b-8192 (mặc định, tốc độ nhanh)
- llama3-70b-8192 (chất lượng cao) 
- mixtral-8x7b-32768 (cân bằng tốc độ và chất lượng)

Prompt hệ thống được thiết kế để phân tích CV và JD, đề xuất cải tiến phù hợp mà không thêm thông tin giả.

## Giao diện đồ họa

Ứng dụng Streamlit cung cấp giao diện trực quan với các tính năng:
- Upload CV và JD hoặc nhập JD trực tiếp
- Tùy chỉnh các tham số AI
- Hiển thị kết quả và tải xuống

## Tùy chỉnh

### Cấu hình qua TOML

```toml
# config.toml
[api]
model = "llama3-70b-8192"
temperature = 0.5
max_tokens = 3000

[output]
default_filename = "custom_output.txt"
```

### Tham số dòng lệnh

```bash
python -m resumeenhancer optimize resume.pdf jd.txt --model llama3-70b-8192 --temperature 0.5 --max-tokens 3000
```

## Xử lý lỗi

ResumeEnhancer bao gồm hệ thống log đầy đủ để ghi lại tiến trình và lỗi. Log được lưu trong file `resumeenhancer.log`.

## Ví dụ

Thư mục `examples` chứa các ví dụ để bắt đầu:
- `sample_resume.txt`: CV mẫu
- `sample_job_description.txt`: Mô tả công việc mẫu
- `config.toml`: Cấu hình mẫu
- `run_example.bat`/`run_example.sh`: Script chạy ví dụ 