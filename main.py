from fastapi import FastAPI, Depends, UploadFile, HTTPException, File
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from datetime import datetime
import PyPDF2
import re
import json
from app.models.pdf_file import PDFFiles
from app.config import get_db_url
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import io



app = FastAPI()

# Монтируем папку для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/", response_class=HTMLResponse)
async def get_upload_form():
    with open("static/upload-form.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


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

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    try:
        contents = await file.read()
        info, security_data = extract_file(contents)
        
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        certifying_center = security_data.get('certifying_center', 'Не указано')
        date = security_data.get('date', 'Не указано')
        recipient = security_data.get('recipient', 'Не указано')

        if 'Некорректный формат документа' in info or 'Отсутствие задолженностей или формат задолженностей неправильный' in info:
            pdf_data = PDFFiles(
                filename=file.filename,
                timestamp=timestamp,
                certifying_center=certifying_center,
                date=date,
                recipient=recipient,
                moneys='0 руб',
                status=info
            )
            db.add(pdf_data)
            await db.commit()
            response_data = {
                'Файл': file.filename,
                'Метки времени': timestamp,
                'Центр сертификации': certifying_center,
                'Дата': date,
                'Получатель': recipient,
                'Рублей': '0 руб',
                "Вид": info
            }
            return response_data
        else:
            data_list = []
            for money, status in info:
                data = {
                    'Файл': file.filename,
                    'Метки времени': timestamp,
                    'Центр сертификации': certifying_center,
                    'Дата': date,
                    'Получатель': recipient,
                    'Рублей': money,
                    "Вид": status
                }
                data_list.append(data)
                pdf_data = PDFFiles(
                    filename=file.filename,
                    timestamp=timestamp,
                    certifying_center=certifying_center,
                    date=date,
                    recipient=recipient,
                    moneys=money,
                    status=status
                )
                db.add(pdf_data)
            await db.commit()
            return data_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the PDF file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)