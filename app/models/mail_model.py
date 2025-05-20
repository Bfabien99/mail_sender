from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, func, DateTime

class MailModel(Base):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    body = Column(String)
    send_by = Column(String)
    send_to = Column(String)
    cc = Column(String, nullable=True)
    bcc = Column(String, nullable=True)
    date = Column(DateTime, default=func.now())
    sent = Column(Boolean, default=False)
    sent_date = Column(DateTime, nullable=True)

