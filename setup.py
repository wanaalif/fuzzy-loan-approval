"""
Setup script for Fuzzy Logic Loan Approval System

This allows the package to be installed with: pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fuzzy-loan-approval",
    version="1.0.0",
    author="Le Yong Xiang and Team",
    author_email="your.email@example.com",
    description="A fuzzy logic controller for automated loan approval decisions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fuzzy-loan-approval",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "fuzzy-loan-demo=examples.demo:main",
        ],
    },
    include_package_data=True,
    keywords="fuzzy-logic loan-approval artificial-intelligence decision-making",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fuzzy-loan-approval/issues",
        "Source": "https://github.com/yourusername/fuzzy-loan-approval",
        "Documentation": "https://github.com/yourusername/fuzzy-loan-approval/blob/main/README.md",
    },
)
