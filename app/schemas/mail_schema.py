from pydantic import BaseModel
from typing import Optional

class MailBase(BaseModel):
    pass

class MailCreate(MailBase):
    subject: str
    body: str
    send_by: str
    send_to: str
    cc: Optional[str] = None
    bcc: Optional[str] = None

class MailUpdate(MailBase):
    subject: Optional[str] = None
    body: Optional[str] = None
    send_by: Optional[str] = None
    send_to: Optional[str] = None
    cc: Optional[str] = None
    bcc: Optional[str] = None