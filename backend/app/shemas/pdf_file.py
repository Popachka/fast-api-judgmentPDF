from pydantic import BaseModel

class PDFFileBase(BaseModel):
    filename: str
    timestamp: str
    certifying_center: str
    date: str
    recipient: str
    moneys: str
    status: str

class PDFFileCreate(PDFFileBase):
    pass

class PDFFileResponse(PDFFileBase):
    id: int

    class Config:
        orm_mode = True