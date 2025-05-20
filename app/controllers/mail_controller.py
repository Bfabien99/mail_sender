from app.schemas.mail_schema import MailCreate
from app.models.mail_model import MailModel
from app.core.database import DBSession
from fastapi import HTTPException
from typing import List, Optional
from app.service.EmailSender import send_email

def create_mail(mail: MailCreate, db: DBSession) -> MailModel:
    """
    Crée un nouveau mail dans la base de données.
    """
    db_mail = MailModel(**mail.dict())
    db.add(db_mail)
    db.commit()
    db.refresh(db_mail)
    return db_mail


def read_mails(db: DBSession) -> List[MailModel]:
    """
    Retourne tous les mails.
    """
    return db.query(MailModel).all()


def read_mail(db: DBSession, mail_id: int) -> Optional[MailModel]:
    """
    Retourne un mail spécifique par son ID.
    """
    return db.query(MailModel).filter(MailModel.id == mail_id).first()


def update_mail(mail_id: int, mail_update: MailCreate, db: DBSession) -> MailModel:
    """
    Met à jour un mail existant.
    """
    db_mail = db.query(MailModel).filter(MailModel.id == mail_id).first()

    if not db_mail:
        raise HTTPException(status_code=404, detail="Mail non trouvé")

    # Mise à jour des champs
    for key, value in mail_update.dict().items():
        setattr(db_mail, key, value)

    db.commit()
    db.refresh(db_mail)
    return db_mail


def delete_mail(mail_id: int, db: DBSession) -> dict:
    """
    Supprime un mail par son ID.
    """
    db_mail = db.query(MailModel).filter(MailModel.id == mail_id).first()

    if not db_mail:
        raise HTTPException(status_code=404, detail="Mail non trouvé")

    db.delete(db_mail)
    db.commit()
    
    return True

def sent_pending_mail(id: int, db: DBSession):
    db_mail = read_mail(db, id)

    if not db_mail:
        raise HTTPException(status_code=404, detail="Mail non trouvé")

    if db_mail.sent :
        raise HTTPException(status_code=400, detail="Mail déjà envoyé")

    send = send_email(db_mail.subject, db_mail.send_by, db_mail.send_to, db_mail.body)
    if send:
        db_mail.sent = True
        db.commit()
        return True