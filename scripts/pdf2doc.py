##pip install pdf2docx
# Try installing this using pip install pdf2docx --user if you have any issues

"""Convert a PDF file to a Word document."""

import argparse
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a PDF file to DOCX.")
    parser.add_argument("input_pdf", type=Path, help="PDF file to convert")
    parser.add_argument("output_docx", type=Path, help="path for the output DOCX file")
    args = parser.parse_args(argv)

    if not args.input_pdf.is_file():
        parser.error(f"input PDF does not exist: {args.input_pdf}")

    from pdf2docx import Converter

    converter = Converter(str(args.input_pdf))
    try:
        converter.convert(str(args.output_docx))
    finally:
        converter.close()


if __name__ == "__main__":
    main()
