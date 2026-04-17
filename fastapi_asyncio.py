import asyncio
import httpx
from datetime import datetime


async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        print("Request fetch url!")
        response = await client.get(url)
        print("Response fetch url!")
        return response.status_code, response.text[:50]

async def main():
    urls = [
        "https://echo.getpostman.com/delay/1",
        "https://echo.getpostman.com/delay/2",
        "https://echo.getpostman.com/delay/3"
    ]

    results = await asyncio.gather(*(fetch_url(url) for url in urls))

    for status_code, text in results:
        print(f"Status code: {status_code}, text: {text}")

if __name__ == "__main__":
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)
