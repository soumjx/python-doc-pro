# DOCX Multi-Format Converter

A Python utility to convert Microsoft Word documents (`.docx`) into Markdown, HTML, PDF, and CSV (tables). 

## Features
- **Semantic HTML**: Uses `mammoth` to generate clean HTML.
- **Markdown**: Converts rich text to clean Markdown.
- **Data Extraction**: Extracts embedded tables and saves them as CSVs for data analysis (Tableau ready).
- **PDF Generation**: Generates PDFs via HTML intermediate.

## Prerequisites
1. Python 3.8+

python-docx==1.1.0
mammoth==1.6.0
markdownify==0.11.6
xhtml2pdf==0.2.15
pandas>=2.0.0
openpyxl==3.1.2

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python generate_test_data.py
   python main.py --input input/tables.docx --output output/v1