"""
Module đọc và phân tích file văn bản thông thường (.txt).
"""
from pathlib import Path
from typing import Optional
from loguru import logger


def extract_text_from_txt(txt_path: str) -> Optional[str]:
    """
    Trích xuất nội dung từ file văn bản thông thường.
    
    Args:
        txt_path: Đường dẫn tới file văn bản.
    
    Returns:
        Nội dung văn bản của file hoặc None nếu xảy ra lỗi.
    """
    try:
        logger.info(f"Đang đọc file văn bản: {txt_path}")
        
        # Kiểm tra file có tồn tại không
        txt_file = Path(txt_path)
        if not txt_file.exists():
            logger.error(f"File không tồn tại: {txt_path}")
            return None
        
        # Thử đọc với các encoding khác nhau
        encodings = ['utf-8', 'windows-1252', 'latin-1']
        text = None
        
        for encoding in encodings:
            try:
                with open(txt_path, 'r', encoding=encoding) as file:
                    text = file.read()
                logger.debug(f"Đã đọc file với encoding {encoding}")
                break
            except UnicodeDecodeError:
                logger.debug(f"Không thể đọc file với encoding {encoding}, thử encoding khác")
                continue
        
        if text is None:
            logger.error(f"Không thể đọc file với bất kỳ encoding nào: {txt_path}")
            return None
        
        if not text.strip():
            logger.warning(f"File văn bản rỗng: {txt_path}")
            return None
        
        logger.debug(f"Đã trích xuất thành công {len(text)} ký tự từ file văn bản")
        return text
        
    except Exception as e:
        logger.error(f"Lỗi khi đọc file văn bản {txt_path}: {str(e)}")
        return None 