# DOCX Multi-Format Converter

A Python utility to convert Microsoft Word documents (`.docx`) into Markdown, HTML, PDF, and CSV (tables). 

## Features
- **Semantic HTML**: Uses `mammoth` to generate clean HTML.
- **Markdown**: Converts rich text to clean Markdown.
- **Data Extraction**: Extracts embedded tables and saves them as CSVs for data analysis (Tableau ready).
- **PDF Generation**: Generates PDFs via HTML intermediate.

## Prerequisites
1. Python 3.8+

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate