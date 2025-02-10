import asyncio
from crawl4ai import *
import re
import csv
from datetime import datetime

def markdown_to_csv(markdown, csv_file):
    # 使用正則表達式擷取類別與數量
    pattern = re.findall(r"\[\s*([\u4e00-\u9fa5A-Za-z0-9&（）()\s]+?)\s+(\d+)\s*\]", markdown)

    # 寫入CSV檔案
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["類別", "數量"])  # 寫入標題
        writer.writerows(pattern)  # 寫入資料

    print(f"資料已儲存至 {csv_file}")

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.toolify.ai/tw/category?group=text-writing",
        )
        print(result.markdown)
        markdown = result.markdown
        current_date = datetime.now().strftime("%Y%m%d")
        with open(f'./{current_date}_toolify_categories_page.md', 'w', encoding='utf-8-sig') as md_file:
            md_file.write(markdown)
        print(f"Markdown 檔案已成功儲存為 {current_date}_toolify_categories_page.md")
        markdown_to_csv(markdown, f"{current_date}_toolify_categories.csv")

if __name__ == "__main__":
    asyncio.run(main())