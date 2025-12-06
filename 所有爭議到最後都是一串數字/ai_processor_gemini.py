import os
import google.generativeai as genai

# =================設定區=================
# 1. 請填入您的 Google Gemini API Key
GOOGLE_API_KEY = "AIzaSyDPhB9AtUVhdwHQmrKkEzOpGybkpXJAul0"

# 2. 設定模型 (推薦使用 gemini-1.5-flash，速度快且免費額度高)
MODEL_NAME = "gemini-1.5-flash" 

# 設定輸入與輸出資料夾
INPUT_FOLDER = "articles"       
OUTPUT_FOLDER = "ai_data"       
GLOBAL_CONTEXT_FILE = "ai_data/global_context.txt" 

# 配置 Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
# =======================================

def ensure_folders():
    """確保資料夾存在"""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def read_file(filepath):
    """讀取檔案內容"""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def save_file(filename, content):
    """儲存內容到檔案"""
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已儲存：{filepath}")

def analyze_chapter(chapter_text):
    """
    功能 1: 針對「單一章節」進行重點分析
    """
    prompt = f"""
    你是一位專業的小說編輯。請閱讀以下章節內容，並整理出以下資訊：
    1. 【本章摘要】：用3句話總結這一章發生了什麼事。
    2. 【關鍵角色動態】：這一章主要角色的心境或關係有什麼變化？
    3. 【伏筆與細節】：有沒有特別值得注意的道具、台詞或場景？

    文章內容：
    {chapter_text}
    """
    
    # Gemini 的呼叫方式比 OpenAI 更簡單
    response = model.generate_content(prompt)
    return response.text

def update_global_context(current_context, new_chapter_text):
    """
    功能 2: 結合「舊的劇情大綱」與「新章節」，更新全書脈絡
    """
    prompt = f"""
    以下是這部小說目前的【累積劇情大綱】：
    {current_context}

    以下是【最新一章】的內容：
    {new_chapter_text}

    請任務：
    請將最新一章的劇情進展，整合進累積劇情大綱中。
    請保持大綱的連貫性，讓讀者即使很久沒看，看這份大綱也能馬上回憶起目前故事走到哪裡。
    (請直接輸出新的完整大綱，不要加開場白)
    """

    response = model.generate_content(prompt)
    return response.text

# =================主程式執行區=================
if __name__ == "__main__":
    ensure_folders()
    
    # 指定您現在要處理的章節檔名
    target_filename = "ch1.txt"  
    article_path = os.path.join(INPUT_FOLDER, target_filename)
    
    print(f"🚀 開始處理 (使用 Gemini)：{target_filename} ...")
    
    # 讀取文章
    article_content = read_file(article_path)
    
    if article_content:
        # --- 動作 A: 生成單篇分析 ---
        print("正在生成單篇分析...")
        try:
            chapter_analysis = analyze_chapter(article_content)
            save_file(target_filename.replace(".txt", "_analysis.txt"), chapter_analysis)
            
            # --- 動作 B: 更新全書脈絡 ---
            print("正在更新全書劇情脈絡...")
            old_context = read_file(GLOBAL_CONTEXT_FILE)
            new_context = update_global_context(old_context, article_content)
            
            with open(GLOBAL_CONTEXT_FILE, "w", encoding="utf-8") as f:
                f.write(new_context)
            print(f"✅ 全書脈絡已更新至 {GLOBAL_CONTEXT_FILE}")
            
        except Exception as e:
            print(f"❌ 發生錯誤：{e}")
            print("建議檢查 API Key 是否正確，或是否超出免費額度限制。")
        
    else:
        print(f"❌ 找不到檔案：{article_path}")