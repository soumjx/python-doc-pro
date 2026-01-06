# generate_test_data.py
import os
from docx import Document
from pathlib import Path

def create_sample_docx():
    # Ensure input directory exists
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)
    
    file_path = input_dir / "financial_report.docx"
    
    doc = Document()
    
    # 1. Add Heading and Text (For HTML/PDF/MD)
    doc.add_heading('Q4 Financial Performance', 0)
    doc.add_paragraph('This report summarizes the financial performance for Q4 2024.')
    
    doc.add_heading('Executive Summary', level=1)
    doc.add_paragraph(
        'Revenue exceeded expectations by 15%, primarily driven by '
        'strong adoption in the enterprise sector.', style='Intense Quote'
    )

    # 2. Add Data Table (For CSV/Tableau)
    doc.add_heading('Revenue Data Table', level=1)
    doc.add_paragraph('The following table outlines revenue per region:')
    
    # Create a table with 4 columns
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    
    # Add Header Row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Region'
    hdr_cells[1].text = 'Product'
    hdr_cells[2].text = 'Revenue'
    hdr_cells[3].text = 'Growth (%)'
    
    # Add Data Rows
    data = [
        ('North America', 'Software', '50000', '12.5'),
        ('Europe', 'Software', '32000', '8.2'),
        ('Asia Pacific', 'Hardware', '45000', '15.0'),
        ('North America', 'Services', '12000', '5.5'),
    ]
    
    for region, product, revenue, growth in data:
        row_cells = table.add_row().cells
        row_cells[0].text = region
        row_cells[1].text = product
        row_cells[2].text = revenue
        row_cells[3].text = growth

    # Save the file
    doc.save(file_path)
    print(f"✅ Success! Created sample file at: {file_path}")

if __name__ == "__main__":
    create_sample_docx()