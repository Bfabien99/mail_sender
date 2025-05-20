from fastapi import APIRouter, Request
from app.core.database import DBSession
from app.schemas.mail_schema import MailCreate, MailUpdate
from app.controllers import mail_controller
from fastapi.responses import JSONResponse
from app.core.limiter import limiter

router = APIRouter(prefix="/mails")

@router.get("/")
async def get_mails(request: Request, db: DBSession):
    return mail_controller.read_mails(db)

@router.post("/")
async def save_mail(request: Request, item: MailCreate, db: DBSession):
    return mail_controller.create_mail(item, db)

@router.get("/{id}")
async def get_single_mail(request: Request, id: int, db: DBSession):
    return mail_controller.read_mail(db, id)

@router.put("/{id}")
async def update_put_mail(request: Request, id: int, item: MailCreate, db: DBSession):
    return mail_controller.update_mail(id, item, db)

@router.patch("/{id}")
async def update_patch_mail(request: Request, id: int, item: MailUpdate, db: DBSession):
    return mail_controller.update_mail(id, item, db)

@router.post("/send")
@limiter.limit("5/minutes")
async def send_mail(request: Request, id: int, db: DBSession):
    try:
        if mail_controller.sent_pending_mail(id, db):
            return JSONResponse(content={"message": "Mail sent"}, status_code=200)
    except Exception as e:
        print(e.__dict__)
        return JSONResponse(content={"error": str(e)}, status_code=500)