from fastapi import FastAPI, HTTPException
import uvicorn
import logging
from playwright.async_api import async_playwright
import markdownify

app = FastAPI()

logging.basicConfig(level=logging.INFO)


async def crawl_one_url(url):
    print(f"Fetching URL: {url}")
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            try:
                browser = await browser_type.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.wait_for_timeout(2000)
                content = await page.content()
                await browser.close()
                return markdownify.markdownify(content)
            except Exception as e:
                logging.error(f"Error with browser {browser_type.name}: {e}")
                continue
    raise Exception("All browser types failed")


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/crawl")
async def submit(payload: dict):
    url = payload.get("url")
    print(f"Received URL: {url}")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    try:
        web_content = await crawl_one_url(url)
        return web_content.__repr__()
    except Exception as e:
        logging.error(f"Error crawling URL {url}: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


if __name__ == "__main__":
    uvicorn.run('app:app', host="127.0.0.1", port=8000, reload=True)
