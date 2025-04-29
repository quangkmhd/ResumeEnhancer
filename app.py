"""
Ứng dụng Streamlit cho ResumeEnhancer.
"""
import os
import streamlit as st
import tempfile
import base64
from pathlib import Path
from resumeenhancer.utils.logger import setup_logger
from resumeenhancer.utils.config import load_config
from resumeenhancer.utils.ai_service import AIService
from resumeenhancer.parsers.file_handler import extract_text_from_file

# Thiết lập logger
logger = setup_logger()

# Đường dẫn tới file CSS
STATIC_DIR = Path(__file__).parent / "resumeenhancer" / "static"
CSS_FILE = STATIC_DIR / "styles.css"

def load_css():
    """Tải file CSS từ static directory."""
    try:
        # Sử dụng đường dẫn tương đối vì app.py nằm ở thư mục gốc của dự án
        css_file = Path("resumeenhancer/static/styles.css")
        if css_file.exists():
            with open(css_file, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            logger.warning(f"Không tìm thấy file CSS: {css_file}")
    except Exception as e:
        logger.error(f"Lỗi khi tải file CSS: {str(e)}")

# Tiêu đề ứng dụng
st.set_page_config(
    page_title="ResumeEnhancer - Tối ưu hóa CV với AI",
    page_icon="📝",
    layout="wide"
)

# Tải CSS
load_css()

def main():
    """Hàm chính của ứng dụng Streamlit."""
    
    # Tiêu đề và giới thiệu
    st.title("📝 ResumeEnhancer")
    st.subheader("Công cụ tối ưu hóa CV dựa trên AI")
    
    st.markdown("""
    ResumeEnhancer sử dụng AI để phân tích CV của bạn và so sánh với mô tả công việc.
    Công cụ sẽ đề xuất cách cải thiện CV để phù hợp hơn với vị trí ứng tuyển.
    """)
    
    # Tạo tabs
    tab1, tab2, tab3 = st.tabs(["Tối ưu CV", "Cài đặt", "Hướng dẫn"])
    
    with tab1:
        st.header("Tối ưu CV của bạn")
        
        # Input cho API key
        api_key = st.text_input("Groq API Key", type="password", placeholder="Nhập Groq API key của bạn")
        if not api_key:
            api_key = os.environ.get("GROQ_API_KEY", "")
            if api_key:
                st.success("Đã tìm thấy API key từ biến môi trường")
        
        # Tải lên CV
        cv_file = st.file_uploader("Tải lên CV của bạn", type=["pdf", "docx", "txt"])
        
        # Tải lên mô tả công việc
        jd_file = st.file_uploader("Tải lên mô tả công việc", type=["pdf", "docx", "txt"])
        
        # Hoặc nhập trực tiếp JD
        st.markdown("### Hoặc nhập trực tiếp mô tả công việc")
        jd_text = st.text_area("", height=200, placeholder="Dán mô tả công việc ở đây...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Tùy chọn nâng cao
            with st.expander("Tùy chọn nâng cao"):
                model = st.selectbox(
                    "Mô hình AI",
                    options=["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"],
                    index=0
                )
                temperature = st.slider("Độ sáng tạo", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
                max_tokens = st.number_input("Số token tối đa", min_value=500, max_value=4000, value=2048, step=100)
        
        with col2:
            # Nút phân tích
            analyze_button = st.button("Phân tích và tối ưu CV", type="primary", use_container_width=True)
        
        if analyze_button:
            if not api_key:
                st.error("Vui lòng cung cấp Groq API Key.")
                return
            
            if not cv_file:
                st.error("Vui lòng tải lên CV của bạn.")
                return
            
            if not jd_file and not jd_text:
                st.error("Vui lòng tải lên mô tả công việc hoặc nhập trực tiếp.")
                return
            
            # Đặt API key vào biến môi trường
            os.environ["GROQ_API_KEY"] = api_key
            
            # Hiển thị thanh tiến trình
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Lưu file tạm thời
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv_file.name)[1]) as tmp_cv:
                    tmp_cv.write(cv_file.getbuffer())
                    cv_path = tmp_cv.name
                
                # Đọc nội dung CV
                status_text.text("Đang đọc CV...")
                progress_bar.progress(25)
                cv_content = extract_text_from_file(cv_path)
                if not cv_content:
                    st.error("Không thể đọc nội dung CV. Vui lòng kiểm tra lại file.")
                    # Xóa file tạm
                    os.unlink(cv_path)
                    return
                
                # Hiển thị nội dung CV đã trích xuất
                with st.expander("Xem nội dung CV đã trích xuất"):
                    st.text(cv_content)
                
                # Đọc nội dung mô tả công việc
                status_text.text("Đang đọc mô tả công việc...")
                progress_bar.progress(50)
                
                jd_content = ""
                if jd_file:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(jd_file.name)[1]) as tmp_jd:
                        tmp_jd.write(jd_file.getbuffer())
                        jd_path = tmp_jd.name
                    
                    jd_content = extract_text_from_file(jd_path)
                    # Xóa file tạm
                    os.unlink(jd_path)
                else:
                    jd_content = jd_text
                
                if not jd_content:
                    st.error("Không thể đọc nội dung mô tả công việc. Vui lòng kiểm tra lại.")
                    # Xóa file tạm CV
                    os.unlink(cv_path)
                    return
                
                # Hiển thị nội dung JD đã trích xuất
                with st.expander("Xem nội dung mô tả công việc đã trích xuất"):
                    st.text(jd_content)
                
                # Khởi tạo dịch vụ AI
                status_text.text("Đang phân tích CV và tạo đề xuất...")
                progress_bar.progress(75)
                
                ai_service = AIService(api_key=api_key)
                result = ai_service.analyze_resume(
                    resume_content=cv_content,
                    job_description=jd_content,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                progress_bar.progress(100)
                status_text.text("Hoàn thành!")
                
                # Xóa file tạm CV
                os.unlink(cv_path)
                
                if not result:
                    st.error("Không thể tạo đề xuất tối ưu hóa. Vui lòng thử lại.")
                    return
                
                # Hiển thị kết quả
                st.markdown("## Kết quả phân tích")
                st.markdown(result)
                
                # Tùy chọn tải xuống
                st.download_button(
                    label="Tải xuống kết quả",
                    data=result,
                    file_name="enhanced_resume.md",
                    mime="text/markdown"
                )
                
                # Tạo PDF từ kết quả
                st.markdown("---")
                st.markdown("### Xuất kết quả dưới dạng PDF")
                st.markdown(
                    "Bạn có thể sao chép kết quả trên và sử dụng các công cụ trực tuyến để chuyển đổi sang định dạng PDF."
                )
                
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {str(e)}")
                logger.exception(f"Lỗi khi phân tích CV: {str(e)}")
    
    with tab2:
        st.header("Cài đặt")
        
        st.markdown("""
        ### Cài đặt API
        
        Bạn có thể lấy Groq API key từ [trang web của Groq](https://console.groq.com/).
        
        Các mô hình được hỗ trợ:
        - llama3-8b-8192 (mặc định, tốc độ nhanh)
        - llama3-70b-8192 (chất lượng cao)
        - mixtral-8x7b-32768 (cân bằng tốc độ và chất lượng)
        
        ### Tham số AI
        
        - **Độ sáng tạo (Temperature)**: Giá trị cao hơn tạo ra nội dung đa dạng hơn, giá trị thấp hơn tạo ra kết quả nhất quán hơn.
        - **Số token tối đa**: Giới hạn độ dài của phản hồi.
        """)
    
    with tab3:
        st.header("Hướng dẫn sử dụng")
        
        st.markdown("""
        ### Cách sử dụng ResumeEnhancer
        
        1. **Tải lên CV của bạn**: Hỗ trợ các định dạng PDF, DOCX, và TXT.
        2. **Tải lên mô tả công việc**: Bạn có thể tải lên file mô tả công việc hoặc dán nội dung trực tiếp.
        3. **Nhập API key**: Đăng ký tài khoản tại [Groq](https://console.groq.com/) để lấy API key.
        4. **Điều chỉnh tùy chọn nâng cao** (tùy chọn): Bạn có thể điều chỉnh mô hình AI và các tham số khác.
        5. **Nhấn "Phân tích và tối ưu CV"**: Hệ thống sẽ phân tích CV của bạn và đề xuất cách cải thiện.
        6. **Xem kết quả**: Kết quả sẽ được hiển thị và bạn có thể tải xuống để tham khảo.
        
        ### Lưu ý
        
        - ResumeEnhancer chỉ đưa ra đề xuất dựa trên thông tin có sẵn trong CV của bạn.
        - Công cụ không thêm thông tin giả mạo hoặc phóng đại quá mức.
        - Kết quả tốt nhất đạt được khi CV và mô tả công việc chi tiết và cụ thể.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Được phát triển bởi ResumeEnhancer Team | [GitHub](https://github.com/yourusername/resumeenhancer)"
    )

if __name__ == "__main__":
    main() 