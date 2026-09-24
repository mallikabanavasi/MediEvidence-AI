import pymupdf
import pytesseract
from PIL import Image


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text.strip()


def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """
    Extract text from a scanned PDF using Tesseract OCR.
    """

    document = pymupdf.open(pdf_path)

    extracted_text = ""

    for page in document:
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples,
        )

        text = pytesseract.image_to_string(image)

        extracted_text += text + "\n"

    document.close()

    return extracted_text.strip()


def extract_text_from_pdf_with_ocr(pdf_path: str) -> str:
    """
    Extract text from a PDF.
    Use normal PDF text extraction first.
    If very little text is found, use OCR.
    """

    document = pymupdf.open(pdf_path)

    normal_text = ""

    for page in document:
        normal_text += page.get_text()

    document.close()

    normal_text = normal_text.strip()

    if len(normal_text) >= 50:
        return normal_text

    return extract_text_from_scanned_pdf(pdf_path)