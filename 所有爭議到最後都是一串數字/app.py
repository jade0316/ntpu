import streamlit as st
import os

# --- 1. 基本設定 ---
st.set_page_config(page_title="我的連載小說", layout="wide", page_icon="📚")

# 設定資料夾路徑
ARTICLE_FOLDER = "articles"
AI_DATA_FOLDER = "ai_data"

# 確保資料夾存在，避免報錯
if not os.path.exists(ARTICLE_FOLDER):
    os.makedirs(ARTICLE_FOLDER)
if not os.path.exists(AI_DATA_FOLDER):
    os.makedirs(AI_DATA_FOLDER)

# --- 2. 側邊欄：自動讀取章節列表 ---
st.sidebar.title("📚 目錄")

# 讀取 articles 資料夾內的所有 txt 檔案，並排序
# (建議檔名用數字開頭，如 01_開頭.txt，排序才會正確)
files = sorted([f for f in os.listdir(ARTICLE_FOLDER) if f.endswith(".txt")])

if not files:
    st.error(f"⚠️ 找不到文章！請將 .txt 檔放入 '{ARTICLE_FOLDER}' 資料夾中。")
    st.stop()

# 讓使用者選擇章節
selected_filename = st.sidebar.radio("請選擇章節：", files)

# --- 3. 側邊欄：全書劇情脈絡 (AI) ---
st.sidebar.markdown("---")
st.sidebar.header("🧐 全書劇情提要")
global_context_path = os.path.join(AI_DATA_FOLDER, "global_context.txt")

if os.path.exists(global_context_path):
    with open(global_context_path, "r", encoding="utf-8") as f:
        st.sidebar.info(f.read())
else:
    st.sidebar.warning("尚無劇情大綱 (請先執行 AI 腳本)")

# --- 4. 主畫面：顯示內文與單篇分析 ---
# 找出對應的 AI 分析檔案路徑 (假設檔名規則是 ch1.txt -> ch1_analysis.txt)
analysis_filename = selected_filename.replace(".txt", "_analysis.txt")
analysis_path = os.path.join(AI_DATA_FOLDER, analysis_filename)
article_path = os.path.join(ARTICLE_FOLDER, selected_filename)

# 讀取文章內容
with open(article_path, "r", encoding="utf-8") as f:
    article_content = f.read()

# 標題 (去除 .txt 副檔名)
st.title(selected_filename.replace(".txt", ""))

# 使用兩欄佈局：左邊寬 (內文)，右邊窄 (本章導讀)
col1, col2 = st.columns([3, 1.2])

with col1:
    st.markdown("### 📖 故事內文")
    # 使用 container 來增加一點邊距美感
    with st.container(border=True):
        st.markdown(article_content) # 如果文章是 Markdown 格式會自動渲染，純文字也沒問題

with col2:
    st.markdown("### 🤖 本章 AI 導讀")
    if os.path.exists(analysis_path):
        with open(analysis_path, "r", encoding="utf-8") as f:
            st.success(f.read())
    else:
        st.caption("尚未生成本章分析 (請執行 AI 腳本)")

# --- 5. 頁尾 ---
st.markdown("---")
st.caption("Designed with Python & Gemini | 僅供好友閱讀")