from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class PDFFiles(Base):
    __tablename__ = 'pdf_files'  # Укажите имя таблицы в базе данных

    id = Column(Integer, primary_key=True)
    filename = Column(String(120), nullable=False)
    timestamp = Column(String(120), nullable=False)
    certifying_center = Column(String(120), nullable=False)
    date = Column(String(120), nullable=False)
    recipient = Column(String(120), nullable=False)
    moneys = Column(Text, nullable=False)
    status = Column(String(120), nullable=False)

    def __str__(self):
        return (f"ID: {self.id}, Filename: {self.filename}, "
                f"Timestamp: {self.timestamp}, Certifying Center: {self.certifying_center}, "
                f"Date: {self.date}, Recipient: {self.recipient}, "
                f"Moneys: {self.moneys}, Status: {self.status}")

    def __repr__(self):
        return str(self)