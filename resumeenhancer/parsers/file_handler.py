"""
Module xử lý file, tự động chọn parser phù hợp dựa vào định dạng.
"""
import os
from pathlib import Path
from typing import Optional
from loguru import logger

from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from .text_parser import extract_text_from_txt


def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Trích xuất nội dung văn bản từ file với định dạng bất kỳ (PDF, DOCX, TXT).
    
    Args:
        file_path: Đường dẫn tới file cần đọc.
    
    Returns:
        Nội dung văn bản của file hoặc None nếu không thể đọc.
    """
    # Kiểm tra file có tồn tại không
    if not os.path.exists(file_path):
        logger.error(f"File không tồn tại: {file_path}")
        return None
    
    # Lấy phần mở rộng của file
    file_extension = Path(file_path).suffix.lower()
    
    # Chọn parser phù hợp dựa vào phần mở rộng
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    elif file_extension in ['.txt', '.md', '.rst']:
        return extract_text_from_txt(file_path)
    else:
        # Thử đọc như file văn bản thông thường
        logger.warning(f"Định dạng file không được hỗ trợ chính thức: {file_extension}. Thử đọc như file văn bản.")
        return extract_text_from_txt(file_path)


def save_text_to_file(text: str, output_path: str) -> bool:
    """
    Lưu nội dung văn bản vào file.
    
    Args:
        text: Nội dung cần lưu.
        output_path: Đường dẫn tới file đầu ra.
    
    Returns:
        True nếu lưu thành công, False nếu có lỗi.
    """
    try:
        # Tạo thư mục chứa file đầu ra nếu chưa tồn tại
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Ghi nội dung vào file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        logger.info(f"Đã lưu kết quả vào file: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Lỗi khi lưu file {output_path}: {str(e)}")
        return False 