from fastapi import FastAPI, Depends, UploadFile, HTTPException, File
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from datetime import datetime
from app.models.pdf_file import PDFFiles
from app.config import get_db_url
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.pdf_utils.base import extract_file
from typing import List
app = FastAPI()
origins = [
    "http://localhost:3000",
    'http://judgmentfiles.online/'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Монтируем папку для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/", response_class=HTMLResponse)
async def get_upload_form():
    with open("static/upload-form.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/upload-pdf/")
async def upload_pdf(files:  List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    response_data = []
    print('-------------', files)
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Invalid file type")

        try:
            contents = await file.read()
            info, security_data = extract_file(contents)

            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            certifying_center = security_data.get(
                'certifying_center', 'Не указано')
            date = security_data.get('date', 'Не указано')
            recipient = security_data.get('recipient', 'Не указано')

            file_data = {'data': [], 'file_name': '', 'file_size': ''}

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
                file_data['data'].append({
                    'filename': file.filename,
                    'timestamp': timestamp,
                    'certifying_center': certifying_center,
                    'date': date,
                    'recipient': recipient,
                    'amount': '0 руб',
                    "status": info
                })
            else:
                for money, status in info:
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

                file_data['data'].extend([{
                    'filename': file.filename,
                    'timestamp': timestamp,
                    'certifying_center': certifying_center,
                    'date': date,
                    'recipient': recipient,
                    'amount': money,
                    "status": status
                } for money, status in info])
            file_data['file_name'] = file.filename
            file_data['file_size'] = file.size
            response_data.append(file_data)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred while processing the PDF file: {str(e)}")
        print('--------------', response_data)
    return {'files': response_data}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
