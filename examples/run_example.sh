#!/bin/bash
echo "=== ResumeEnhancer - Ví dụ chạy ==="

# Đặt API key của bạn ở đây hoặc qua biến môi trường
export GROQ_API_KEY="your_groq_api_key_here"

echo "Đang chạy ResumeEnhancer với file resume và mô tả công việc mẫu..."
python -m resumeenhancer optimize \
  sample_resume.txt \
  sample_job_description.txt \
  --output enhanced_resume.txt \
  --config config.toml

echo ""
echo "Quá trình hoàn tất. Kết quả được lưu trong file enhanced_resume.txt"
echo "" 