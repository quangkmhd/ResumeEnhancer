"""
Module quản lý log cho ResumeEnhancer.
"""
import os
import sys
from pathlib import Path
from loguru import logger

from .config import load_config


def setup_logger():
    """
    Thiết lập logger với các cấu hình từ file cấu hình.
    """
    try:
        # Tải cấu hình
        config = load_config()
        log_config = config.get("output", {})
        
        # Lấy tên file log và level từ cấu hình
        log_file = log_config.get("log_file", "resumeenhancer.log")
        log_level = log_config.get("log_level", "INFO")
        
        # Tạo thư mục chứa file log nếu chưa tồn tại
        log_path = Path(log_file)
        log_dir = log_path.parent
        if not log_path.is_absolute():
            # Nếu đường dẫn là tương đối, lưu trong thư mục hiện tại
            log_dir = Path.cwd() / log_dir
            log_path = Path.cwd() / log_path
        
        os.makedirs(log_dir, exist_ok=True)
        
        # Xóa tất cả các handler mặc định
        logger.remove()
        
        # Thêm handler xuất ra console
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level,
            colorize=True
        )
        
        # Thêm handler xuất ra file
        logger.add(
            str(log_path),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation="10 MB",
            compression="zip",
            enqueue=True
        )
        
        logger.info(f"Đã thiết lập logger với level {log_level}, lưu vào {log_path}")
        
    except Exception as e:
        # Nếu có lỗi, thiết lập logger với cấu hình mặc định
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        logger.add("resumeenhancer.log", level="INFO", rotation="10 MB")
        logger.warning(f"Lỗi khi thiết lập logger: {e}. Sử dụng cấu hình mặc định.")
    
    return logger 