"""
Module đọc và phân tích file PDF.
"""
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
from loguru import logger


def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Trích xuất nội dung văn bản từ file PDF.
    
    Args:
        pdf_path: Đường dẫn tới file PDF.
    
    Returns:
        Nội dung văn bản của file PDF hoặc None nếu xảy ra lỗi.
    """
    try:
        logger.info(f"Đang đọc file PDF: {pdf_path}")
        
        # Kiểm tra file có tồn tại không
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            logger.error(f"File không tồn tại: {pdf_path}")
            return None
        
        # Đọc nội dung PDF
        reader = PdfReader(pdf_path)
        text = ""
        
        # Trích xuất văn bản từ mỗi trang
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
        
        if not text.strip():
            logger.warning(f"Không trích xuất được văn bản từ file PDF: {pdf_path}")
            return None
        
        logger.debug(f"Đã trích xuất thành công {len(text)} ký tự từ file PDF")
        return text
        
    except Exception as e:
        logger.error(f"Lỗi khi đọc file PDF {pdf_path}: {str(e)}")
        return None 