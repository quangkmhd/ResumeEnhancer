"""
Setup script for ResumeEnhancer package.
"""
from setuptools import setup, find_packages
import os

# Đọc nội dung file README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Đọc requirements từ file requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

# Lấy phiên bản từ file __init__.py
about = {}
with open(os.path.join("resumeenhancer", "__init__.py"), "r", encoding="utf-8") as fh:
    exec(fh.read(), about)

setup(
    name="resumeenhancer",
    version=about["__version__"],
    author=about["__author__"],
    description="Công cụ tối ưu hóa Resume dựa trên AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resumeenhancer",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "resumeenhancer": ["config_default.toml"],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "resumeenhancer=resumeenhancer.main:app",
        ],
    },
) 