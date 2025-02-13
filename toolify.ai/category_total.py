import pandas as pd

def calculate_category_sums(csv_file):
    # 讀取 CSV 檔案
    df = pd.read_csv(csv_file)
    
    # 確保 CSV 檔案有正確的欄位
    if "類別" not in df.columns or "數量" not in df.columns:
        raise ValueError("CSV 檔案必須包含 '類別' 和 '數量' 欄位")
    
    # 轉換數量欄位為數值型態
    df["數量"] = pd.to_numeric(df["數量"], errors='coerce').fillna(0)
    
    # 定義大類別及其對應的欄位範圍
    category_ranges = {
        "文字與寫作": (0, 28),
        "影像": (29, 61),
        "影片": (62, 76),
        "代碼&IT": (77, 97),
        "音訊": (98, 113),
        "商業": (114, 125),
        "行銷": (126, 151),
        "AI探測器": (152, 156),
        "聊天機器人": (157, 161),
        "設計與藝術": (162, 171),
        "生活助理": (172, 191),
        "3D": (192, 194),
        "教育": (195, 203),
        "prompt": (204, 204),
        "生產力": (205, 226),
        "Other": (227, 232)
    }
    
    # 統計每個大類別的總和
    result = []
    for category, (start, end) in category_ranges.items():
        total = df.loc[start:end, "數量"].sum()
        result.append([category, total])
    
    # 轉換為 DataFrame
    result_df = pd.DataFrame(result, columns=["大類別", "總和"])
    
    return result_df

# 測試範例 (請自行替換 'your_file.csv' 為實際檔案名稱)
if __name__ == "__main__":
    csv_file = '20250213_toolify_categories.csv'  # 修改為你的 CSV 檔案路徑
    result_df = calculate_category_sums(csv_file)
    print(result_df)
    result_df.to_csv("category_summary.csv", index=False)  # 輸出結果為 CSV
