# ResumeEnhancer - Giao diện Streamlit

ResumeEnhancer hiện đã có giao diện người dùng sử dụng Streamlit, giúp việc tối ưu hóa CV dễ dàng hơn thông qua trình duyệt web.

## Cài đặt

Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt ResumeEnhancer:

```bash
# Đi đến thư mục ResumeEnhancer
cd ResumeEnhancer

# Cài đặt gói
pip install -e .

# Cài đặt Streamlit nếu chưa có
pip install streamlit
```

## Chạy ứng dụng Streamlit

Để khởi động giao diện web Streamlit cho ResumeEnhancer:

```bash
# Đi đến thư mục ResumeEnhancer
cd ResumeEnhancer

# Chạy ứng dụng Streamlit
streamlit run app.py
```

Sau khi chạy lệnh trên, trình duyệt web sẽ tự động mở và hiển thị giao diện của ResumeEnhancer.

## Tính năng của giao diện Streamlit

Giao diện Streamlit của ResumeEnhancer cung cấp các tính năng sau:

1. **Tải lên file CV** - Hỗ trợ các định dạng PDF, DOCX, và TXT
2. **Tải lên mô tả công việc** hoặc nhập trực tiếp nội dung
3. **Tùy chọn nâng cao** - Điều chỉnh mô hình AI, độ sáng tạo và số token
4. **Hiển thị kết quả** - Xem và tải xuống kết quả phân tích

## Cấu hình API

Bạn sẽ cần một Groq API key để sử dụng ResumeEnhancer. Có hai cách để cung cấp API key:

1. Nhập trực tiếp vào trường API key trong giao diện
2. Đặt biến môi trường `GROQ_API_KEY` trước khi chạy ứng dụng:

```bash
# Windows (PowerShell)
$env:GROQ_API_KEY="your_groq_api_key_here"

# Linux/Mac
export GROQ_API_KEY="your_groq_api_key_here"
```

## Hướng dẫn sử dụng

1. Nhập Groq API key của bạn
2. Tải lên file CV (PDF, DOCX, TXT)
3. Tải lên file mô tả công việc hoặc nhập trực tiếp
4. Điều chỉnh tùy chọn nâng cao (tùy chọn)
5. Nhấn "Phân tích và tối ưu CV"
6. Xem kết quả và tải xuống nếu cần

## Xử lý lỗi

Nếu gặp lỗi khi chạy ứng dụng Streamlit, hãy kiểm tra:

- API key Groq có hợp lệ không
- Định dạng file CV và mô tả công việc có được hỗ trợ không
- Kết nối internet có ổn định không

## Tùy chỉnh

Bạn có thể tùy chỉnh giao diện Streamlit bằng cách chỉnh sửa file `app.py` và CSS trong thư mục `resumeenhancer/static/`. 