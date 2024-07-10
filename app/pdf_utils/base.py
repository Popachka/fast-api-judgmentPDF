import io
import PyPDF2
import re
import json
def extract_text_from_pdf(pdf_file):
    text_per_page = {}
    pdfReader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
    for pagenum, page in enumerate(pdfReader.pages):
        page_text = page.extract_text()
        text_per_page[f'Page_{pagenum}'] = page_text
    return text_per_page

def remove_alphanumeric_lines(text):
    lines_to_remove = re.findall(r'.*[a-zA-Z].*\d.*|.*\d.*[a-zA-Z].*', text, re.MULTILINE)
    for line in lines_to_remove:
        text = text.replace(line, '')
    return text

def preprocess(text):
    numbers = re.findall(r'\b\d[\d\s,]+\d\b', text)
    for number in numbers:
        cleaned_number = number.replace(' ', '').replace(',', '.')
        text = text.replace(number, cleaned_number)
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\b\d{1,2}[./]\d{1,2}[./]\d{4}\b', '', text)
    text = re.sub(r'№\d+', '', text)
    text = re.sub(r'-\d+', '', text)
    text = re.sub(r'/\d+', '', text)
    text = re.sub(r'\d+(\.\d+)?%', '', text)
    text = re.sub(r'[.,]', '', text)
    text = re.sub(r'стать(?:ей|ями|я|и)?\s+\d+\s*', '', text)
    text = remove_alphanumeric_lines(text)
    text = text.strip()
    lines = text.split('\n')
    filtered_lines = [line for line in lines if not re.match(r'^\d+$', line.strip())]
    text = '\n'.join(filtered_lines)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.strip()
    return text

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

def f(pdf_file):
    text_per_page = extract_text_from_pdf(pdf_file)
    pattern = [
        'РЕШИЛ', 'Р Е Ш И Л','решил','решено', 'р е ш и л',
        'Р     Е     Ш     И     Л', 'О П Р Е Д Е Л И Л', 'ОПРЕДЕЛИЛ',
        'П О С Т А Н О В И Л', 'Р Е Ш И Л', 'о п р е д е л и л',
        'П О С Т А Н О В И Л', 'О П Р Е Д Е Л И Л', 'ре ши л'
    ]
    found_resolved = False
    all_texts = ""
    pages = list(text_per_page.values())
    if not pages:
        return "", {}
    security_data = extract_signature_data(pages[-1])
    for text in pages:
        if not found_resolved:
            for variant in pattern:
                if variant in text:
                    found_resolved = True
                    start_index = text.find(variant)
                    text = text[start_index:]
                    all_texts += text + " "
                    break
        else:
            all_texts += text + " "
    result = preprocess(all_texts)
    return result, security_data

def g(text):
    pattern_rub = r'\b\d+[.,]?\d*(?:\s*руб(?:лей|ль|)|\s*р(?:\.|))\b'
    matches_rub = re.findall(pattern_rub, text)
    return matches_rub

def classify_context(context):
    fee_keywords = ['госпошлина', 'пошлина', 'пошлины']
    context_lower = context.lower()
    if any(keyword in context_lower for keyword in fee_keywords):
        return 'Госпошлина'
    else:
        return 'Задолженность'

def extract_file(pdf_file):
    text, security_data = f(pdf_file)
    if not text:
        return 'Некорректный формат документа', security_data
    moneys = g(text)
    if not moneys:
        return 'Отсутствие задолженностей или формат задолженностей неправильный', security_data
    text = text.strip()
    classified_numbers = []
    for money in moneys:
        number = money[0]
        start_idx = max(0, text.find(number) - 60)
        end_idx = text.find(number) + len(number) + 60
        context = text[start_idx:end_idx]
        classification = classify_context(context)
        classified_numbers.append((money, classification))
    return classified_numbers, security_data