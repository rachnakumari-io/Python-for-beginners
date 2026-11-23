"""Tests for the PDF to DOCX converter CLI."""

import contextlib
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import pdf2doc


class TestPdf2Doc(unittest.TestCase):
    def test_converts_input_and_closes_converter(self):
        with tempfile.TemporaryDirectory() as directory:
            input_pdf = Path(directory) / "input.pdf"
            input_pdf.touch()
            output_docx = Path(directory) / "output.docx"
            converter = Mock()
            fake_pdf2docx = types.SimpleNamespace(
                Converter=Mock(return_value=converter)
            )

            with patch.dict(sys.modules, {"pdf2docx": fake_pdf2docx}):
                pdf2doc.main([str(input_pdf), str(output_docx)])

            fake_pdf2docx.Converter.assert_called_once_with(str(input_pdf))
            converter.convert.assert_called_once_with(str(output_docx))
            converter.close.assert_called_once_with()

    def test_missing_input_reports_clear_error(self):
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            missing_pdf = Path(directory) / "missing.pdf"
            output_docx = Path(directory) / "output.docx"

            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as exit_error:
                    pdf2doc.main([str(missing_pdf), str(output_docx)])

        self.assertEqual(exit_error.exception.code, 2)
        self.assertIn(
            f"input PDF does not exist: {missing_pdf}", stderr.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
