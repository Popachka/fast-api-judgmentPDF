import io
import PyPDF2
import re

def extract_text_from_pdf(pdf_file):
    text_per_page = {}
    pdfReader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
    for pagenum, page in enumerate(pdfReader.pages):
        page_text = page.extract_text()
        text_per_page[f'Page_{pagenum}'] = page_text
    return text_per_page

def extract_signature_data(text):
    data = {}
    center_match = re.search(r'Удостоверяющий центр\s+(.*)', text)
    if center_match:
        data['certifying_center'] = center_match.group(1).strip()
    date_match = re.search(r'Дата\s+([^\n]+)', text)
    if date_match:
        data['date'] = date_match.group(1).strip()
    recipient_match = re.search(r'Кому выдана\s+(.*)', text)
    if recipient_match:
        data['recipient'] = recipient_match.group(1).strip()
    return data
