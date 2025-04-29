"""
Module quản lý cấu hình cho ResumeEnhancer.
"""
import os
import tomli
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Tải biến môi trường từ file .env nếu có
load_dotenv()

# Đường dẫn tới thư mục gốc của ứng dụng
ROOT_DIR = Path(__file__).parent.parent

# Đường dẫn tới file cấu hình mặc định
DEFAULT_CONFIG_PATH = ROOT_DIR / "config_default.toml"

# Các vị trí cấu hình có thể có theo thứ tự ưu tiên (cao đến thấp)
CONFIG_PATHS = [
    Path("./config.toml"),  # Thư mục hiện tại
    Path.home() / ".config" / "resumeenhancer" / "config.toml",  # Thư mục người dùng
    DEFAULT_CONFIG_PATH,  # Cấu hình mặc định trong package
]


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Tải cấu hình từ file TOML.
    
    Args:
        config_path: Đường dẫn tới file cấu hình. Nếu None, sẽ tìm trong các vị trí mặc định.
    
    Returns:
        Dict chứa cấu hình.
    
    Raises:
        FileNotFoundError: Nếu không tìm thấy file cấu hình nào.
    """
    # Nếu người dùng chỉ định đường dẫn cụ thể
    if config_path:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Không tìm thấy file cấu hình: {config_path}")
        
        with open(config_file, "rb") as f:
            return tomli.load(f)
    
    # Tìm file cấu hình đầu tiên tồn tại
    for path in CONFIG_PATHS:
        if path.exists():
            with open(path, "rb") as f:
                return tomli.load(f)
    
    # Nếu không tìm thấy file cấu hình nào, báo lỗi
    raise FileNotFoundError(
        f"Không tìm thấy file cấu hình nào. Đã thử các đường dẫn: {', '.join(str(p) for p in CONFIG_PATHS)}"
    )


def get_api_key() -> str:
    """
    Lấy Groq API key từ biến môi trường hoặc file cấu hình.
    
    Returns:
        API key dưới dạng string.
        
    Raises:
        ValueError: Nếu không tìm thấy API key.
    """
    # Ưu tiên lấy từ biến môi trường
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        # Thử tìm trong file cấu hình
        try:
            config = load_config()
            api_key = config.get("api", {}).get("api_key")
        except FileNotFoundError:
            pass
    
    if not api_key:
        raise ValueError(
            "Không tìm thấy Groq API key. Vui lòng đặt biến môi trường GROQ_API_KEY "
            "hoặc thêm vào file cấu hình."
        )
    
    return api_key 