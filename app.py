import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai

# 1. 頁面配置
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="centered")

# CSS 樣式 (確保置中與深色風格)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .block-container { max-width: 800px !important; margin: auto; }
    .stButton>button { border-radius: 12px; height: 3em; background: #4f46e5; color: white; border: none; width: 100%; font-weight: bold; }
    .info-box { background-color: #0e1117; padding: 15px; border-radius: 12px; border-left: 4px solid #818cf8; margin: 10px 0; color: #cbd5e1; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化 API (防止 404 的強化邏輯)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # 這裡不直接寫死路徑，讓 SDK 自己去匹配
        # 優先嘗試 gemini-1.5-flash，失敗則嘗試 gemini-pro
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # 測試一下模型是否可用
            model.generate_content("test") 
        except:
            model = genai.GenerativeModel('gemini-pro')
            
    except Exception as e:
        st.error(f"API 初始化失敗: {str(e)}")
        model = None
else:
    st.error("❌ 尚未在 Secrets 中設定 GEMINI_API_KEY")
    model = None

translator = GoogleTranslator(source='auto', target='en')

# 3. 初始化存儲空間
if 'sub_en' not in st.session_state: st.session_state.sub_en = ""
if 'env_en' not in st.session_state: st.session_state.env_en = ""

def call_ai(text, part):
    if not model or not text: return ""
    try:
        prompt = f"Expand this {part} into a cinematic English prompt for video generation: {text}. Output ONLY the English text."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # 如果還是 404，給出一個保底的翻譯
        translated = translator.translate(text)
        return f"{translated} (AI 繁忙中，已自動切換至普通翻譯)"

# 4. 主介面
st.title("📽️ T2I2V Studio Pro")

with st.expander("🎥 攝影設定", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("風格", ["National Geographic", "Arri Alexa Cinematic", "Kodak Portra 400"])
        lens = st.selectbox("焦段", ["24mm Wide", "50mm Standard", "85mm Portrait"])
    with col2:
        angle = st.selectbox("角度", ["Eye-level shot", "High angle shot", "Low angle shot"])
        move_map = {"Static": "static", "Pan": "pan", "Zoom": "zoom", "Orbit": "orbit"}
        move_key = st.selectbox("運鏡", list(move_map.keys()))

st.divider()

# 輸入區
u_kw = st.text_area("✍️ 主體動作 (中文)", height=100)
if st.button("✨ 使用 AI 擴充主體"):
    with st.spinner("AI 正在思考細節..."):
        st.session_state.sub_en = call_ai(u_kw, "subject action")

if st.session_state.sub_en:
    st.markdown(f'<div class="info-box"><b>AI 擴充內容：</b><br>{st.session_state.sub_en}</div>', unsafe_allow_html=True)

u_env = st.text_input("🌍 地點環境 (中文)")
if st.button("✨ 使用 AI 擴充環境"):
    with st.spinner("AI 正在設計場景..."):
        st.session_state.env_en = call_ai(u_env, "environment and lighting")

if st.session_state.env_en:
    st.markdown(f'<div class="info-box"><b>AI 擴充內容：</b><br>{st.session_state.env_en}</div>', unsafe_allow_html=True)

# 生成結果
st.divider()
if st.button("🚀 生成最終提示詞組", type="primary"):
    if u_kw:
        final_sub = st.session_state.sub_en if st.session_state.sub_en else translator.translate(u_kw)
        final_env = st.session_state.env_en if st.session_state.env_en else translator.translate(u_env)
        
        t2i = f"RAW photo, {final_env}, {angle}, {lens}, {final_sub}, {style} --ar 16:9"
        i2v = f"Mostly {move_map[move_key]}, {final_sub} continues action, realistic motion."
        
        st.subheader("✅ 生成結果")
        st.code(f"Step 1 (底圖):\n{t2i}")
        st.code(f"Step 2 (影片):\n{i2v}")
    else:
        st.error("請輸入內容")
