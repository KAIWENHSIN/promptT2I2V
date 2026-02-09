import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai

# 1. 頁面配置與高級感 CSS (置中優化)
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    /* 全域背景與置中限制 */
    .main { background-color: #050505; color: #e0e0e0; }
    .block-container { padding-top: 2rem; max-width: 800px !important; }
    
    /* 輸入框樣式 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #1a1a1a !important; color: white !important; 
        border-radius: 12px !important; border: 1px solid #333 !important;
    }
    
    /* 按鈕樣式 */
    .stButton>button { 
        border-radius: 12px; height: 3.5em; background-color: #4f46e5; 
        color: white; border: none; width: 100%; font-weight: bold;
    }
    .stButton>button:hover { 
        background-color: #6366f1; transform: translateY(-2px); 
    }
    
    /* AI 擴充結果區塊 */
    .enhance-res { 
        background-color: #0e1117; padding: 15px; border-radius: 12px; 
        border-left: 4px solid #818cf8; margin: 15px 0; 
        font-style: italic; color: #cbd5e1; font-size: 0.95em;
    }
    
    /* 結果顯示卡片 */
    .result-card { 
        background-color: #111; padding: 25px; border-radius: 18px; 
        border: 1px solid #222; border-top: 4px solid #4f46e5; 
        margin-top: 25px;
    }
    code { color: #818cf8 !important; font-size: 1.1em !important; background-color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化 API (解決 404 問題的核心寫法)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 直接指定模型名稱，不加 "models/"
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API 設定失敗: {str(e)}")
        model = None
else:
    st.error("❌ 尚未在 Streamlit Secrets 中設定 GEMINI_API_KEY")
    model = None

translator = GoogleTranslator(source='auto', target='en')

# 3. 初始化 Session State
if 'sub_en' not in st.session_state: st.session_state.sub_en = ""
if 'env_en' not in st.session_state: st.session_state.env_en = ""

def call_ai(text, part):
    if not model or not text: return ""
    try:
        # 強制指定不使用 v1beta 的內容生成邏輯
        prompt = f"Expand this {part} into a cinematic English prompt: {text}. Output only the English text."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # 如果還是 404，嘗試最後一種模型名稱備案
        try:
            alt_model = genai.GenerativeModel('gemini-pro')
            response = alt_model.generate_content(f"Cinematic prompt for: {text}")
            return response.text.strip()
        except:
            return f"AI Error: {str(e)}"

# 4. 主畫面介面
st.title("📽️ T2I2V Studio Pro")
st.markdown("##### 專業實拍提示詞工作站")

# 攝影參數
with st.expander("🎥 攝影機與運鏡設定", expanded=True):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        style = st.selectbox("影視風格", ["National Geographic", "Arri Alexa Cinematic", "Kodak Portra 400", "IMAX 70mm"])
        lens = st.selectbox("焦段", ["24mm Wide", "14mm Ultra-Wide", "35mm Classic", "50mm Standard", "85mm Portrait"])
    with col_s2:
        angle = st.selectbox("鏡位角度", ["Eye-level shot", "High angle shot", "Low angle shot", "Dutch angle"])
        move_map = {
            "Static (靜態)": "static camera",
            "Handheld (手持微動)": "handheld micro-movement",
            "Zoom In (縮放)": "slow zoom in",
            "Orbit (環繞)": "360-degree orbit",
            "Dolly In (推入)": "camera dollies in",
            "360 roll (翻轉)": "barrel roll"
        }
        move_key = st.selectbox("運鏡方式", list(move_map.keys()))

st.divider()

# 輸入區
u_kw = st.text_area("✍️ 主體動作 (中文)", placeholder="例如：男孩在跳舞", height=100)
if st.button("✨ 使用 AI 擴充主體細節"):
    if u_kw:
        with st.spinner("AI 生成中..."):
            st.session_state.sub_en = call_ai(u_kw, "subject action")
    else: st.warning("請先輸入內容")

if st.session_state.sub_en:
    st.markdown(f'<div class="enhance-res"><b>AI Enhanced Subject:</b><br>{st.session_state.sub_en}</div>', unsafe_allow_html=True)

u_env = st.text_input("🌍 地點與光影 (中文)", placeholder="例如：黃昏，金色柔光")
if st.button("✨ 使用 AI 擴充環境細節"):
    if u_env:
        with st.spinner("AI 生成中..."):
            st.session_state.env_en = call_ai(u_env, "environment and lighting")

if st.session_state.env_en:
    st.markdown(f'<div class="enhance-res"><b>AI Enhanced Environment:</b><br>{st.session_state.env_en}</div>', unsafe_allow_html=True)

st.divider()

# 生成結果
if st.button("🚀 生成最終雙語提示詞組", type="primary"):
    if u_kw:
        final_sub = st.session_state.sub_en if st.session_state.sub_en else translator.translate(u_kw)
        final_env = st.session_state.env_en if st.session_state.env_en else translator.translate(u_env)
        neg = "--no flicker, no warping, no text, no watermark"
        
        t2i = f"RAW photo, {final_env}. {angle}, {lens}. {final_sub}. {style}, high-fidelity. {neg}"
        i2v = f"Mostly {move_map[move_key]}. [Subject: {final_sub} continues action]. {neg}"
        
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("#### Step 1:
