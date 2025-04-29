"""
Module chính của ứng dụng ResumeEnhancer.
"""
import os
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pydantic import BaseModel

from resumeenhancer.utils.logger import setup_logger
from resumeenhancer.utils.config import load_config
from resumeenhancer.utils.ai_service import AIService
from resumeenhancer.parsers.file_handler import extract_text_from_file, save_text_to_file

# Thiết lập logger
logger = setup_logger()

# Khởi tạo ứng dụng Typer
app = typer.Typer(
    name="resumeenhancer",
    help="Công cụ tối ưu hóa Resume dựa trên AI",
    add_completion=False,
)

# Khởi tạo console từ rich
console = Console()


class EnhanceOptions(BaseModel):
    """Model Pydantic cho các tùy chọn tối ưu hóa resume."""
    resume_path: str
    job_description_path: str
    output_path: Optional[str] = None
    config_path: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


def enhance_resume(options: EnhanceOptions) -> None:
    """
    Tối ưu hóa resume dựa trên mô tả công việc.
    
    Args:
        options: Các tùy chọn cho quá trình tối ưu hóa.
    """
    try:
        # Tải cấu hình
        config = load_config(options.config_path)
        
        # Lấy đường dẫn output mặc định nếu không được chỉ định
        if not options.output_path:
            output_filename = config.get("output", {}).get("default_filename", "enhanced_resume.txt")
            options.output_path = output_filename
        
        # Đọc nội dung resume
        console.print("[bold blue]Đang đọc file resume...[/bold blue]")
        resume_content = extract_text_from_file(options.resume_path)
        if not resume_content:
            console.print("[bold red]Lỗi: Không thể đọc file resume.[/bold red]")
            return
        
        # Đọc nội dung mô tả công việc
        console.print("[bold blue]Đang đọc file mô tả công việc...[/bold blue]")
        job_description = extract_text_from_file(options.job_description_path)
        if not job_description:
            console.print("[bold red]Lỗi: Không thể đọc file mô tả công việc.[/bold red]")
            return
        
        # Khởi tạo dịch vụ AI
        console.print("[bold blue]Đang kết nối tới dịch vụ AI...[/bold blue]")
        ai_service = AIService(api_key=options.api_key, config_path=options.config_path)
        
        # Phân tích resume
        with console.status("[bold green]Đang phân tích resume và tạo đề xuất...[/bold green]", spinner="dots"):
            result = ai_service.analyze_resume(
                resume_content=resume_content,
                job_description=job_description,
                model=options.model,
                temperature=options.temperature,
                max_tokens=options.max_tokens
            )
        
        if not result:
            console.print("[bold red]Lỗi: Không thể tạo đề xuất tối ưu hóa.[/bold red]")
            return
        
        # Hiển thị kết quả
        console.print("\n[bold green]Kết quả tối ưu hóa:[/bold green]")
        console.print(Panel(Markdown(result), title="Đề xuất tối ưu hóa Resume", expand=False))
        
        # Lưu kết quả vào file
        if save_text_to_file(result, options.output_path):
            console.print(f"[bold green]Đã lưu kết quả vào file: {options.output_path}[/bold green]")
        else:
            console.print(f"[bold red]Lỗi: Không thể lưu kết quả vào file {options.output_path}[/bold red]")
        
    except Exception as e:
        logger.exception(f"Lỗi không xác định khi tối ưu hóa resume: {str(e)}")
        console.print(f"[bold red]Lỗi: {str(e)}[/bold red]")


@app.command()
def optimize(
    resume: str = typer.Argument(..., help="Đường dẫn tới file resume (PDF, DOCX, TXT)"),
    job_description: str = typer.Argument(..., help="Đường dẫn tới file mô tả công việc (PDF, DOCX, TXT)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Đường dẫn file đầu ra (mặc định: enhanced_resume.txt)"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Đường dẫn tới file cấu hình TOML"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="Groq API key"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Tên model LLM (mặc định: llama3-8b-8192)"),
    temperature: Optional[float] = typer.Option(None, "--temperature", "-t", help="Độ sáng tạo của AI (0-1, mặc định: 0.7)"),
    max_tokens: Optional[int] = typer.Option(None, "--max-tokens", help="Số token tối đa cho kết quả (mặc định: 2048)"),
) -> None:
    """
    Tối ưu hóa resume dựa trên mô tả công việc (job description).
    """
    # In banner
    console.print(Panel.fit(
        "[bold blue]ResumeEnhancer[/bold blue] - [italic]Công cụ tối ưu hóa Resume dựa trên AI[/italic]",
        border_style="green"
    ))
    
    # Tạo options từ tham số dòng lệnh
    options = EnhanceOptions(
        resume_path=resume,
        job_description_path=job_description,
        output_path=output,
        config_path=config,
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Tối ưu hóa resume
    enhance_resume(options)


@app.command()
def version() -> None:
    """Hiển thị phiên bản của ResumeEnhancer."""
    from resumeenhancer import __version__
    console.print(f"[bold]ResumeEnhancer[/bold] v{__version__}")


if __name__ == "__main__":
    app() 