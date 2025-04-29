"""
Module tích hợp Groq API để phân tích resume.
"""
import time
from typing import Dict, Any, Optional
from groq import Groq
from loguru import logger

from .config import load_config, get_api_key


class AIService:
    """
    Lớp cung cấp dịch vụ AI sử dụng Groq API.
    """
    
    def __init__(self, api_key: Optional[str] = None, config_path: Optional[str] = None):
        """
        Khởi tạo dịch vụ AI.
        
        Args:
            api_key: Groq API key. Nếu None, sẽ tự động lấy từ biến môi trường hoặc file cấu hình.
            config_path: Đường dẫn tới file cấu hình. Nếu None, sẽ tìm trong các vị trí mặc định.
        """
        # Tải cấu hình
        self.config = load_config(config_path)
        self.api_config = self.config.get("api", {})
        
        # Lấy API key
        self.api_key = api_key or get_api_key()
        
        # Khởi tạo client Groq
        self.client = Groq(api_key=self.api_key)
        
        # Các giá trị mặc định
        self.model = self.api_config.get("model", "llama3-8b-8192")
        self.temperature = float(self.api_config.get("temperature", 0.7))
        self.max_tokens = int(self.api_config.get("max_tokens", 2048))
        self.timeout = int(self.api_config.get("timeout", 30))
        
        logger.info(f"Đã khởi tạo dịch vụ AI với model: {self.model}")
    
    def analyze_resume(
        self, 
        resume_content: str, 
        job_description: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """
        Phân tích resume dựa trên mô tả công việc.
        
        Args:
            resume_content: Nội dung của resume.
            job_description: Mô tả công việc.
            model: Tên model AI muốn sử dụng (ghi đè cấu hình).
            temperature: Nhiệt độ AI (ghi đè cấu hình).
            max_tokens: Số token tối đa cho kết quả (ghi đè cấu hình).
        
        Returns:
            Các đề xuất cải tiến cho resume hoặc None nếu có lỗi.
        """
        try:
            # Sử dụng các giá trị được truyền vào hoặc giá trị mặc định
            model = model or self.model
            temperature = temperature if temperature is not None else self.temperature
            max_tokens = max_tokens or self.max_tokens
            
            # Đọc hệ thống prompt từ cấu hình
            system_message = self.config.get("prompts", {}).get("system_message", "")
            
            # Tạo nội dung cho user message
            user_message = f"""
# Resume hiện tại
{resume_content}

# Mô tả công việc (JD)
{job_description}

Hãy phân tích và đề xuất cách tối ưu resume để phù hợp với mô tả công việc này.
"""
            
            logger.info(f"Đang gửi yêu cầu đến Groq API với model {model}")
            start_time = time.time()
            
            # Gọi API với timeout
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.timeout
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"Nhận được phản hồi từ Groq API sau {elapsed_time:.2f} giây")
            
            # Trích xuất nội dung
            result = response.choices[0].message.content
            
            if not result:
                logger.warning("API trả về kết quả rỗng")
                return None
            
            return result
            
        except Exception as e:
            logger.error(f"Lỗi khi gọi Groq API: {str(e)}")
            return None 