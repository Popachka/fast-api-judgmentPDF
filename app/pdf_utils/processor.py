import re

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
