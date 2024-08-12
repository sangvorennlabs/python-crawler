import asyncio
from playwright.async_api import async_playwright
import markdownify
import logging

class PupperteerModule:
    
    @classmethod
    async def crawl_one_url(cls, url):
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

if __name__ == "__main__":
    url = 'https://www.bing.com/ck/a?!&&p=ab833b15f73b52e9JmltdHM9MTcyMzE2MTYwMCZpZ3VpZD0yMjgzNzA3MC1kMTU5LTY2MzEtMGRhNy02MjEyZDA0YjY3MTAmaW5zaWQ9NTIwNQ&ptn=3&ver=2&hsh=3&fclid=22837070-d159-6631-0da7-6212d04b6710&psq=Bu%e1%bb%95i+t%e1%ba%adp+d%c6%b0%e1%bb%a1ng+sinh+%c4%91%e1%bb%8bnh+m%e1%bb%87nh+%e1%bb%9f+c%c3%b4ng+vi%c3%aan+Tao+%c4%90%c3%a0n&u=a1aHR0cHM6Ly92bmV4cHJlc3MubmV0L2J1b2ktdGFwLWR1b25nLXNpbmgtZGluaC1tZW5oLW8tY29uZy12aWVuLXRhby1kYW4tNDc3OTYyMi5odG1s&ntb=1'
    content = asyncio.run(PupperteerModule.crawl_one_url(url))
    print(content)