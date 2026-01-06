import argparse
import logging
import sys
from pathlib import Path
from src.converters import DocxConverter

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("Main")

def validate_file(path: str) -> str:
    if not Path(path).is_file():
        raise argparse.ArgumentTypeError(f"File not found: {path}")
    if not path.endswith('.docx'):
        raise argparse.ArgumentTypeError(f"File must be a .docx extension: {path}")
    return path

def main():
    parser = argparse.ArgumentParser(description="Industry Standard DOCX Converter")
    parser.add_argument("--input", "-i", type=validate_file, required=True, help="Input .docx path")
    parser.add_argument("--output", "-o", type=str, default="./output", help="Output directory")

    args = parser.parse_args()

    try:
        logger.info(f"Processing file: {args.input}")
        converter = DocxConverter(args.input, args.output)
        converter.process_all()
        logger.info("Conversion Pipeline Completed Successfully.")
        
    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()