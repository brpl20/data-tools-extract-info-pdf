import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def pdf_to_text(pdf_path):
    # Open the pdf file
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    text = ""

    for page_number in range(num_pages):
        # Get a page from the pdf
        page = pdf_document.load_page(page_number)
        # Render page to an image
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Use pytesseract to convert image to text
        page_text = pytesseract.image_to_string(img, lang='por')
        text += page_text

    return text

if __name__ == "__main__":
    pdf_path = "file_.pdf"
    extracted_text = pdf_to_text(pdf_path)
    print(extracted_text)