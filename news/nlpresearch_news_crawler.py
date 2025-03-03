import asyncio
from crawl4ai import *
import os

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
                url=f"https://nlp.elvissaravia.com/archive?sort=new",
            )
        url = "nlpresearch"
        markdown = result.markdown
        create_directory_if_not_exists(f'./{url}')
        with open(f'./{url}/{url}_news.md', 'w', encoding='utf-8-sig') as md_file:
            md_file.write(markdown)
        print(f"Markdown 檔案已成功儲存為 {url}_news.md")

if __name__ == "__main__":
    asyncio.run(main())