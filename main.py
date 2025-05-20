from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
import uvicorn
from app.routes import mail_route
from app.core.database import Base, engine

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(mail_route.router)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(engine)

@app.get('/')
async def root():
    return {"message": "Kaboré the ant"}

@app.get('/limit')
@limiter.limit("2/minute")
async def limit_page(request: Request):
    return {"message": "You can only access this page 2 times per minute"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
