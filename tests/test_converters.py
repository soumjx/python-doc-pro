import pytest
from pathlib import Path
from src.converters import DocxConverter

# Mock data path
TEST_DOC = Path("tests/sample.docx")
OUTPUT_DIR = Path("tests/output")

@pytest.fixture
def converter():
    # Setup: Create a dummy docx if needed or assume one exists
    # For this test to run, you physically need a small sample.docx in tests/
    if not TEST_DOC.exists():
        pytest.skip("Skipping tests: tests/sample.docx not found")
    
    return DocxConverter(str(TEST_DOC), str(OUTPUT_DIR))

def test_initialization(converter):
    assert converter.input_path == TEST_DOC
    assert converter.output_dir == OUTPUT_DIR

def test_html_conversion(converter):
    output = converter.convert_to_html()
    assert output.exists()
    assert output.suffix == ".html"
    assert "<html" in output.read_text(encoding='utf-8')

def test_markdown_conversion(converter):
    output = converter.convert_to_markdown()
    assert output.exists()
    assert output.suffix == ".md"

def test_pdf_conversion(converter):
    output = converter.convert_to_pdf()
    assert output.exists()
    assert output.suffix == ".pdf"
    # Check PDF magic bytes
    with open(output, 'rb') as f:
        header = f.read(4)
        assert header == b'%PDF'

def test_csv_extraction(converter):
    # This might return empty list if sample.docx has no tables
    outputs = converter.convert_to_csv()
    if outputs:
        for file in outputs:
            assert file.suffix == ".csv"
            assert file.exists()