# ResumeEnhancer

ResumeEnhancer là một công cụ dòng lệnh (CLI) sử dụng AI để tối ưu hóa hồ sơ (resume) dựa trên mô tả công việc (job description). Công cụ này phân tích nội dung resume và so sánh với mô tả công việc để đề xuất cải tiến, làm nổi bật các kỹ năng, kinh nghiệm, và chứng chỉ phù hợp mà không thêm thông tin giả mạo.

## Tính năng chính

- **Phân tích thông minh**: Sử dụng Groq API với mô hình ngôn ngữ lớn (LLM) để phân tích resume và job description
- **Hỗ trợ nhiều định dạng**: Đọc được các file PDF, TXT, DOCX
- **Tùy chỉnh linh hoạt**: Cấu hình thông qua file TOML hoặc tham số dòng lệnh
- **Tối ưu hóa mục tiêu**: Đề xuất cải tiến để phù hợp với yêu cầu công việc cụ thể

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

```bash
python -m resumeenhancer --resume path/to/resume.pdf --job-description path/to/jd.txt
```

### Tham số

- `--resume`: Đường dẫn tới file resume (PDF, DOCX, TXT)
- `--job-description`: Đường dẫn tới file mô tả công việc hoặc văn bản mô tả
- `--output`: Đường dẫn lưu kết quả (mặc định: enhanced_resume.txt)
- `--config`: Đường dẫn tới file cấu hình TOML (tùy chọn)
- `--api-key`: Groq API key (có thể cấu hình trong file .env hoặc config.toml)
- `--model`: Tên mô hình LLM (mặc định: llama3-8b-8192)
- `--temperature`: Độ sáng tạo của AI (mặc định: 0.7)
- `--max-tokens`: Số token tối đa cho kết quả (mặc định: 2048)

## Yêu cầu hệ thống

- Python 3.8+
- Groq API key 