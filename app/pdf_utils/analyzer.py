import re

def extract_file(pdf_file):
    from .extractor import extract_text_from_pdf, extract_signature_data
    from .processor import preprocess
    
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
