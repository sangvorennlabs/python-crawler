from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
import logging

from utils.pupperteer import PupperteerModule

semaphore = asyncio.Semaphore(10)

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/crawl")
async def submit(payload: dict):
    url = payload.get("url")
    # print(f"Received URL: {url}")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    try:
        web_content = await PupperteerModule.crawl_one_url(url)
        return web_content
    except Exception as e:
        logging.error(f"Error crawling URL {url}: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)