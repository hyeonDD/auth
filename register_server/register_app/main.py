import logging
import uvicorn
from fastapi import FastAPI

app = FastAPI()


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p',
)


@app.get("/")
async def root():
    logging.warning('WARNING TEST!!')
    logging.info('INFO TEST')
    return {"message": "This is register server!!"}


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
