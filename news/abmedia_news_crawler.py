import asyncio
from crawl4ai import *
import os

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")

async def main():
    async with AsyncWebCrawler() as crawler:
        # 755
        for number in range(1, 3):
            result = await crawler.arun(
                url=f"https://abmedia.io/category/trend/ai-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/page/{number}",
            )
            # print(result.markdown)
            url = "abmedia"
            markdown = result.markdown
            create_directory_if_not_exists(f'./{url}')
            with open(f'./{url}/{url}_news_{number}.md', 'w', encoding='utf-8-sig') as md_file:
                md_file.write(markdown)
            print(f"Markdown 檔案已成功儲存為 {url}_news_{number}.md")

if __name__ == "__main__":
    asyncio.run(main())