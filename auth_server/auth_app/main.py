import uvicorn
from fastapi import FastAPI

from auth_app.api.router import api_router
from auth_app.core.config import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This is auth server!!"}


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)


app.include_router(api_router, prefix=settings.PREFIX_URL)

if __name__ == "__main__":
    start()
