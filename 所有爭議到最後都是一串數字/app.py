import streamlit as st
import os

# --- 設定路徑 (絕對路徑法) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
ARTICLE_FOLDER = os.path.join(current_dir, "articles")
AI_DATA_FOLDER = os.path.join(current_dir, "ai_data")

st.set_page_config(page_title="所有爭議到最後都是一串數字", layout="wide", page_icon="📚")

# --- 側邊欄 ---
st.sidebar.title("📚 目錄")

# 1. 讀取並顯示章節列表
files = sorted([f for f in os.listdir(ARTICLE_FOLDER) if f.endswith(".txt")])
if not files:
    st.error("找不到文章檔")
    st.stop()
selected_filename = st.sidebar.radio("章節", files, label_visibility="collapsed")

st.sidebar.markdown("---")

# 2. 顯示全書劇情提要 (使用 Markdown 解決換行與編號問題)
with st.sidebar.expander("🧐 全書劇情提要", expanded=True):
    global_context_path = os.path.join(AI_DATA_FOLDER, "global_context.txt")
    if os.path.exists(global_context_path):
        with open(global_context_path, "r", encoding="utf-8") as f:
            # 這裡改用 markdown，Streamlit 會自動幫您縮排和換行
            st.markdown(f.read())
    else:
        st.caption("尚無資料")

# 3. 顯示全書時間軸 (新功能)
with st.sidebar.expander("📅 事件時間簡表", expanded=False):
    st.caption("AI 自動整理的時間線")
    # 讀取所有章節的 timeline 檔案並合併顯示
    all_timelines = ""
    for f in files:
        timeline_path = os.path.join(AI_DATA_FOLDER, f.replace(".txt", "_timeline.txt"))
        if os.path.exists(timeline_path):
            with open(timeline_path, "r", encoding="utf-8") as t:
                # 只保留表格內容，去除可能的標題重複
                lines = t.readlines()
                for line in lines:
                    if "|" in line and "---" not in line and "時間" not in line:
                         all_timelines += line
    
    if all_timelines:
        # 手動加上表頭
        table_md = "| 時間 | 事件 |\n|---|---|\n" + all_timelines
        st.markdown(table_md)
    else:
        st.caption("尚無時間軸資料")


# --- 主畫面 ---
analysis_path = os.path.join(AI_DATA_FOLDER, selected_filename.replace(".txt", "_analysis.txt"))
article_path = os.path.join(ARTICLE_FOLDER, selected_filename)

with open(article_path, "r", encoding="utf-8") as f:
    article_content = f.read()
# 🔥 修改重點在這裡：加入總標題 🔥
st.title("所有爭議到最後都是一串數字") 
st.subheader(f"第 {selected_filename.replace('.txt', '')} 章") # 這裡會顯示「第 01 章」

st.markdown("---") # 加一條分隔線更美觀

col1, col2 = st.columns([3, 1.2])
with col1:
    st.markdown("### 📖 故事內文")
    with st.container(border=True):
        st.markdown(article_content)

with col2:
    st.markdown("### 🤖 本章摘要")
    if os.path.exists(analysis_path):
        with open(analysis_path, "r", encoding="utf-8") as f:
            st.success(f.read())
    else:
        st.info("請執行 AI 腳本生成摘要")

    # 這裡也可以顯示單章的時間軸
    timeline_path = os.path.join(AI_DATA_FOLDER, selected_filename.replace(".txt", "_timeline.txt"))
    if os.path.exists(timeline_path):
        st.markdown("#### ⏳ 本章時間點")
        with open(timeline_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())

st.markdown("---")
st.caption("Designed with Python & Gemini")

