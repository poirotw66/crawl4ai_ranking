import pandas as pd

def compare_csv(file1, file2):
    # 讀取 CSV 檔案
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # 確保只包含 '類別' 和 '數量' 欄位
    df1 = df1[['類別', '數量']]
    df2 = df2[['類別', '數量']]
    
    # 以 '類別' 作為索引，方便比較
    df1.set_index('類別', inplace=True)
    df2.set_index('類別', inplace=True)
    
    # 合併兩個 DataFrame
    merged = df1.join(df2, lsuffix='_df1', rsuffix='_df2')
    
    # 計算數值變化
    merged['數量變化'] = merged['數量_df2'] - merged['數量_df1']
    
    # 過濾出有變化的類別
    changed = merged[merged['數量變化'] != 0].reset_index()
    # changed.rename(columns={'數量_df1': 'df1_原本的數值', '數量_df2': 'df2_原本的數值'}, inplace=True)
    
    return changed

# 測試函數
file1 = './20250210_toolify_categories.csv'  # 第一個 CSV 檔案
file2 = './20250213_toolify_categories.csv'  # 第二個 CSV 檔案

changes = compare_csv(file1, file2)
print(changes)