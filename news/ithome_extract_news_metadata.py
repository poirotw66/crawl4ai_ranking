import markdown
import re
def extract_news_info(content):
    """提取新聞資訊的簡單方法"""
    lines = content.strip().split('\n')
    # 標題行通常是第二行，包含在方括號中
    if len(lines) < 4:
        return None
    title_line = lines[1]
    title = title_line.split('[')[1].split(']')[0]
    
    # 網址在標題行的第二個括號內
    url = title_line.split('(')[1].split(')')[0]
    # 修正網址格式
    url = url.replace("</news/", "news/").replace(">", "")
    
    # 摘要是第三行
    summary = lines[2]
    
    # 日期是第四行
    date = lines[3]
    
    # 標籤在第一行，用 | 分隔
    tags_line = lines[0]
    tags_parts = tags_line.split(' | ')
    tags = []
    for part in tags_parts:
        if '[' in part and ']' in part:
            tag = part.split('[')[1].split(']')[0]
            tags.append(tag)
    
    return {
        "標題": title,
        "網址": url,
        "摘要": summary,
        "日期": date,
        "標籤": tags
    }

def format_output(news_info):
    """將提取的資訊格式化為要求的輸出格式"""
    result = f"""標題: {news_info["標題"]}
網址: {news_info["網址"]}
摘要: {news_info["摘要"]}
日期: {news_info["日期"]}
標籤：{", ".join(news_info["標籤"])}"""
    
    return result

def split_news_content(content):
    # 使用 split 方法來分割字串
    news_blocks = content.split("[新聞](https://www.ithome.com.tw/</tags/")

    # 移除第一個空元素（因為開頭沒有 [新聞]）
    # if news_blocks[0].strip() == "":
    news_blocks.pop(0)
    # 再加上 "[新聞](" 到每個區塊的開頭
    news_blocks = ["[新聞](" + block for block in news_blocks]

    return news_blocks



# 示範使用
if __name__ == "__main__":
    # 這裡放入你提供的內容
    content = """
[新聞](https://www.ithome.com.tw/</tags/%E6%96%B0%E8%81%9E>) | [刪預算](https://www.ithome.com.tw/</tags/%E5%88%AA%E9%A0%90%E7%AE%97>) | [數位發展部](https://www.ithome.com.tw/</tags/%E6%95%B8%E4%BD%8D%E7%99%BC%E5%B1%95%E9%83%A8>) | [數位部](https://www.ithome.com.tw/</tags/%E6%95%B8%E4%BD%8D%E9%83%A8>) | [黃彥男](https://www.ithome.com.tw/</tags/%E9%BB%83%E5%BD%A5%E7%94%B7>)
[預算刪減危機衝擊，數發部面臨政策落地與產業創新的雙重考驗](https://www.ithome.com.tw/</news/167596>)
立法院刪除數發部四成預算並凍結近二成預算，數發部長黃彥男坦言，數位發展部預算的縮減對臺灣數位政策的推動造成重大挑戰，可能影響數位基礎建設、技術研發、跨部門協作、法規修訂、AI產業發展、數位憑證行動化、國際合作以及數位防詐策略的實施。 
2025-02-27 
[![](https://s4.itho.me/sites/default/files/styles/picture_size_small/public/field/image/0227-amazon-alexa-960.jpg?itok=RY2aA1mP)](https://www.ithome.com.tw/</news/167595>)
[新聞](https://www.ithome.com.tw/</tags/%E6%96%B0%E8%81%9E>) | [Alexa Plus](https://www.ithome.com.tw/</tags/alexa-plus>) | [Amazon](https://www.ithome.com.tw/</tags/amazon>)
[Amazon公布付費AI助理Alexa Plus，整合Echo成智慧家庭中樞](https://www.ithome.com.tw/news/167595)
透過與Apple Music、Spotify、Uber Eats等第三方服務合作，Amazon將新一代智慧助理Alexa Plus打造成智慧家庭控制中樞，能根據用戶指令執行更多元任務 
2025-02-27 
"""
    markdown_file_path = "./ithome/ithome_news_0.md"
    # 讀取Markdown內容
    with open(markdown_file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    news_index = split_news_content(content)
    # 提取資訊 
    for i in news_index:
        
        news_info = extract_news_info(i)
        # 格式化並輸出結果
        if news_info is None:
            continue
        formatted_result = format_output(news_info)
        print(formatted_result)
        print("="*40)