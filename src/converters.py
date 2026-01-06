import logging
from pathlib import Path
from typing import List, Optional

import mammoth
from xhtml2pdf import pisa
import pandas as pd
from docx import Document
from markdownify import markdownify as md

# Configure Logger
logger = logging.getLogger(__name__)

class DocxConverter:
    """
    A professional wrapper to convert DOCX files to HTML, MD, PDF, and CSV.
    """

    # Basic CSS for PDF to make it look professional
    PDF_CSS = """
    <style>
        body { font-family: Helvetica, sans-serif; font-size: 12px; line-height: 1.5; }
        h1 { color: #2E4053; border-bottom: 1px solid #ccc; }
        h2 { color: #2E4053; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
    """

    def __init__(self, input_path: str, output_dir: str):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.filename = self.input_path.stem

        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_html_content(self) -> str:
        """Helper to get raw HTML from Mammoth."""
        with open(self.input_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            if result.messages:
                for msg in result.messages:
                    logger.debug(f"Mammoth message: {msg}")
            return result.value

    def convert_to_html(self) -> Path:
        """Converts DOCX to standalone HTML."""
        try:
            output_file = self.output_dir / f"{self.filename}.html"
            logger.info(f"Converting to HTML: {output_file}")

            raw_html = self._get_html_content()
            # Wrap in semantic HTML5 structure with Bootstrap CDN for instant styling
            full_html = (
                f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
                f"<title>{self.filename}</title>"
                f"<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>"
                f"</head><body class='container mt-5'>{raw_html}</body></html>"
            )
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_html)
            
            return output_file
        except Exception as e:
            logger.error(f"Failed to convert HTML: {e}")
            raise

    def convert_to_markdown(self) -> Path:
        """Converts DOCX to Markdown."""
        try:
            output_file = self.output_dir / f"{self.filename}.md"
            logger.info(f"Converting to Markdown: {output_file}")

            raw_html = self._get_html_content()
            markdown_text = md(raw_html, heading_style="ATX")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_text)
            
            return output_file
        except Exception as e:
            logger.error(f"Failed to convert Markdown: {e}")
            raise

    def convert_to_csv(self) -> List[Path]:
        """
        Extracts tables to CSVs. 
        Uses Pandas to handle duplicate headers and whitespace cleaning.
        """
        generated_files = []
        try:
            logger.info("Extracting tables to CSV...")
            doc = Document(self.input_path)
            
            if not doc.tables:
                logger.warning("No tables found in document.")
                return []

            for i, table in enumerate(doc.tables):
                # Extract all data as a list of lists first
                table_data = []
                for row in table.rows:
                    # Strip whitespace from cells
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)

                if not table_data:
                    continue

                # Create DataFrame
                # We assume the first row is the header. 
                # If header is empty, pandas handles it automatically if we don't specify columns immediately
                df = pd.DataFrame(table_data)

                # Promote first row to header if it looks like a header
                if len(df) > 1:
                    new_header = df.iloc[0] # Grab the first row for the header
                    df = df[1:] # Take the data less the header row
                    df.columns = new_header # Set the header row as the df header

                # Basic Data Cleaning for Tableau compatibility
                df = df.replace(r'^\s*$', pd.NA, regex=True) # Replace empty strings with NA
                df = df.dropna(how='all') # Drop rows that are completely empty
                
                # Handle duplicate columns by appending a suffix
                df = df.loc[:, ~df.columns.duplicated()].copy() 

                csv_filename = self.output_dir / f"{self.filename}_table_{i+1}.csv"
                df.to_csv(csv_filename, index=False)
                generated_files.append(csv_filename)
                logger.info(f"Saved table {i+1} to {csv_filename}")
            
            return generated_files

        except Exception as e:
            logger.error(f"Failed to extract CSV: {e}")
            raise

    def convert_to_pdf(self) -> Path:
        """Converts DOCX to PDF with CSS styling."""
        try:
            output_file = self.output_dir / f"{self.filename}.pdf"
            logger.info(f"Converting to PDF: {output_file}")

            raw_html = self._get_html_content()
            
            # Inject CSS for better PDF rendering
            full_html = f"<html><head>{self.PDF_CSS}</head><body>{raw_html}</body></html>"
            
            with open(output_file, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)
                
            if pisa_status.err:
                raise RuntimeError(f"PDF generation error: {pisa_status.err}")
            
            return output_file

        except Exception as e:
            logger.error(f"Failed to convert PDF: {e}")
            raise

    def process_all(self):
        """Runs all conversions pipeline."""
        self.convert_to_html()
        self.convert_to_markdown()
        self.convert_to_csv()
        self.convert_to_pdf()