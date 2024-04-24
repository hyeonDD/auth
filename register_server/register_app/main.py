import uvicorn
from fastapi import FastAPI

from register_app.api.router import api_router
from register_app.core.config import settings

app = FastAPI(openapi_url=f'{
              settings.PREFIX_URL}/openapi.json', docs_url=f'{settings.PREFIX_URL}/docs')


@app.get(f"{settings.PREFIX_URL}/")
async def root():
    return {"message": "This is register server!!"}


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)


app.include_router(api_router, prefix=settings.PREFIX_URL)

if __name__ == "__main__":
    start()
