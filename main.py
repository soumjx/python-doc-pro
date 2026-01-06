import argparse
import logging
import sys
from src.converters import DocxConverter

# Setup Logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    parser = argparse.ArgumentParser(description="Convert DOCX files to HTML, MD, PDF, and CSV.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to input .docx file")
    parser.add_argument("--output", "-o", type=str, default="./output", help="Directory for output files")

    args = parser.parse_args()

    try:
        logging.info("Starting Conversion Process...")
        converter = DocxConverter(args.input, args.output)
        converter.process_all()
        logging.info("All tasks completed successfully.")
        
    except Exception as e:
        logging.error(f"Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()