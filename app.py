import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai

# 1. 頁面配置 (置中)
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="centered")

# 2. 初始化 API (解決 404 模型找不到的問題)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 改用這種寫法來相容不同版本的 API
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
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
        # 這是最穩定的生成呼叫方式
        response = model.generate_content(f"Expand this {part} into a cinematic English prompt: {text}. Return ONLY the English text.")
        return response.text.strip()
    except Exception as e:
        return f"AI 暫時無法回應，原因：{str(e)}"

# 4. 介面與功能
st.title("📽️ T2I2V Studio Pro")

# 攝影參數
with st.expander("🎥 攝影設定", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("風格", ["National Geographic", "Arri Alexa", "Kodak Portra"])
        lens = st.selectbox("焦段", ["24mm Wide", "50mm Standard", "85mm Portrait"])
    with col2:
        angle = st.selectbox("角度", ["Eye-level", "High angle", "Low angle"])
        move_map = {"Static": "static", "Pan": "pan", "Zoom": "zoom", "Orbit": "orbit"}
        move_key = st.selectbox("運鏡", list(move_map.keys()))

st.divider()

# 輸入區
u_kw = st.text_area("✍️ 主體動作 (中文)", height=100)
if st.button("✨ 使用 AI 擴充主體"):
    st.session_state.sub_en = call_ai(u_kw, "subject action")
if st.session_state.sub_en:
    st.info(f"AI 建議內容：{st.session_state.sub_en}")

u_env = st.text_input("🌍 地點環境 (中文)")
if st.button("✨ 使用 AI 擴充環境"):
    st.session_state.env_en = call_ai(u_env, "environment")
if st.session_state.env_en:
    st.info(f"AI 建議內容：{st.session_state.env_en}")

st.divider()

# 生成結果
if st.button("🚀 生成提示詞組", type="primary"):
    if u_kw:
        final_sub = st.session_state.sub_en if st.session_state.sub_en else translator.translate(u_kw)
        final_env = st.session_state.env_en if st.session_state.env_en else translator.translate(u_env)
        
        t2i = f"RAW photo, {final_env}, {angle}, {lens}, {final_sub}, {style} --ar 16:9"
        i2v = f"Mostly {move_map[move_key]}, {final_sub} continues action."
        
        st.subheader("✅ 生成結果")
        st.code(f"Step 1 (底圖):\n{t2i}")
        st.code(f"Step 2 (影片):\n{i2v}")
    else:
        st.error("請輸入內容")
