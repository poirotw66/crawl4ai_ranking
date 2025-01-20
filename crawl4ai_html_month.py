import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import pandas as pd


def save2csv(data_text, file_name):
    # Split by lines and remove trailing whitespace
    lines = [line.rstrip() for line in data_text.split('\n') if line.strip()]
    try:
        # Find the index of the table header row
        table_start_index = lines.index('排名| 每月訪問量| 增長| 增長率| 標籤') + 1
    except ValueError:
        print("Table header row not found, please check the input data format.")
        return
    
    table_data = []
    for line in lines[table_start_index:]: 
        if not line.strip(): 
            print("Detected empty line, ending table reading")
            break
        
        if '增長:' in line or all(c in '-|' for c in line.strip()):
            continue

        try:
            parts = line.split('|')
            if len(parts) > 6: 
                parts[1] = '|'.join(parts[1:len(parts) - 4])  
                parts = parts[:2] + parts[-4:]  
            if len(parts) < 6:
                continue    

            app = parts[1].strip()
            monthly_visits = parts[2].strip()
            growth = parts[3].strip()
            growth_rate = parts[4].strip()
            tags = parts[5].strip()

            table_data.append([app, monthly_visits, growth, growth_rate, tags])
        except Exception as e:
            print(f"Error processing line: {line}, Error: {e}")

    # Clean data
    cleaned_table_data = [[item.strip() for item in row] for row in table_data]

    # Check if the number of columns in the data is consistent
    expected_columns = 5
    cleaned_table_data = [row for row in cleaned_table_data if len(row) == expected_columns]

    # Create DataFrame
    columns = ['工具名稱', '每月訪問量', '增長', '增長率', '標籤']
    df = pd.DataFrame(cleaned_table_data, columns=columns)

    # Remove unnecessary rows (rows containing "增長:")
    df = df[~df['工具名稱'].str.contains('增長', na=False, regex=False)]

    # Add ranking column
    df['排名'] = df.index + 1
    df = df[['排名', '工具名稱', '每月訪問量', '增長', '增長率', '標籤']]

    # Save as CSV file
    df.to_csv(f'./csv/{file_name}.csv', index=False, encoding='utf-8-sig')
    print(len(df.index))
    print(f"CSV file successfully created: {file_name}.csv")


async def main():
    browser_config = BrowserConfig(
        headless=True,
        verbose=True,
    )
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.48, threshold_type="fixed", min_word_threshold=0)
        ),
        # markdown_generator=DefaultMarkdownGenerator(
        #     content_filter=BM25ContentFilter(user_query="WHEN_WE_FOCUS_BASED_ON_A_USER_QUERY", bm25_threshold=1.0)
        # ),
    )
    aipure_ranking_ = ['top-ai-tools-for-text-and-writing', 'top-ai-tools-for-image',
     'top-ai-tools-for-voice-and-language', 'top-ai-tools-for-video',
     'top-ai-tools-for-coding-and-development', 'top-ai-tools-for-productivity-tools',
     'top-ai-tools-for-marketing-and-advertising', 'top-ai-tools-for-education-and-learning',
     'top-ai-tools-for-life-assistant', 'top-ai-tools-for-ai-detection', 'top-ai-tools-for-business',
     'top-ai-tools-for-other', 'top-ai-tools-for-chatbot', 'top-ai-tools-for-prompts'] 
    aipure_ranking = ['top-ai-tools-in-Dec-2024', 'top-ai-tools-in-Nov-2024',
                      'top-ai-tools-in-Oct-2024', 'top-ai-tools-in-Sep-2024',
                      'top-ai-tools-in-Aug-2024', 'top-ai-tools-in-Jul-2024',
                      'top-ai-tools-in-Jun-2024', 'top-ai-tools-in-May-2024']
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in aipure_ranking:
            result = await crawler.arun(
                url=f"https://aipure.ai/tw/rankings/{url}",
                config=run_config
            )
            markdown = result.markdown
            with open(f'./md/{url}.md', 'w', encoding='utf-8-sig') as md_file:
                md_file.write(markdown)
            print(f"Markdown 檔案已成功儲存為 {url}.md")
            save2csv(markdown, url)
            
            
if __name__ == "__main__":
    asyncio.run(main())