from fastapi import FastAPI

from routes.user import user_router
from routes.account import account_router

app = FastAPI()

app.include_router(user_router, tags=["user"])
app.include_router(account_router, prefix="/accounts", tags=["account"])


@app.get('/')
def home():
    return {"message": "welcome to UserMoney"}
