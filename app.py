import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai

# 1. 頁面配置與高級感 CSS
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1a1a; color: white; border-radius: 10px; border: 1px solid #333; }
    .stButton>button { border-radius: 12px; height: 3em; background-color: #4f46e5; color: white; border: none; width: 100%; }
    .enhance-res { background-color: #0e1117; padding: 15px; border-radius: 10px; border-left: 4px solid #818cf8; margin-top: 10px; font-style: italic; color: #cbd5e1; }
    .result-card { background-color: #111; padding: 20px; border-radius: 15px; border-left: 5px solid #4f46e5; margin-bottom: 20px; }
    code { color: #818cf8 !important; font-size: 1.1em !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化 API (安全讀取 Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 使用 Flash 模型：速度快、免費配額高
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ 尚未在 Streamlit Secrets 中設定 GEMINI_API_KEY")
    model = None

translator = GoogleTranslator(source='auto', target='en')

# 3. 初始化 Session State (確保 AI 擴充內容在頁面重整時不消失)
if 'sub_en' not in st.session_state: st.session_state.sub_en = ""
if 'env_en' not in st.session_state: st.session_state.env_en = ""

def call_ai(text, part):
    if not model or not text: return ""
    try:
        prompt = f"You are a cinematic prompt expert. Expand the following {part} into a detailed, high-fidelity English description for AI video generation. Return ONLY the expanded English text.\nContent: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"

# 4. 側邊欄與運鏡 (完全對照專業影視運鏡圖)
with st.sidebar:
    st.title("⚙️ Camera Settings")
    style = st.selectbox("影視風格", ["National Geographic", "Kodak Portra 400", "Arri Alexa", "IMAX 70mm", "Fashion Editorial"])
    lens = st.selectbox("焦段", ["8mm Fisheye", "24mm Wide", "35mm Classic", "50mm Standard", "85mm Portrait", "200mm Telephoto"])
    angle = st.selectbox("鏡位", ["Eye-level shot", "High angle shot", "Low angle shot", "Dutch angle", "Front angle", "Over-the-shoulder"])
    st.divider()
    move_map = {
        "Static (靜態)": "static camera, no movement",
        "Handheld (手持微動)": "subtle handheld micro-movement",
        "Zoom In (縮放-近)": "slow zoom in, focusing on details",
        "Orbit (環繞運鏡)": "360-degree orbit around the subject",
        "Dolly In (推入運鏡)": "camera dollies in physically closer",
        "360 roll (360度翻轉)": "cinematic 360-degree barrel roll"
    }
    move_key = st.selectbox("運鏡方式", list(move_map.keys()))

# 5. 主畫面：輸入區域
st.title("🌐 雙語自動翻譯 T2I2V 工作站")

c1, c2 = st.columns(2)
with c1:
    u_kw = st.text_area("✍️ 主體動作 (中文)", placeholder="例如：男孩在會議室裡開心跳舞", height=100)
    if st.button("✨ AI Enhance Subject"):
        with st.spinner("AI 正在擴充細節..."):
            st.session_state.sub_en = call_ai(u_kw, "subject action")

    if st.session_state.sub_en:
        st.markdown(f'<div class="enhance-res"><b>AI Enhanced:</b><br>{st.session_state.sub_en}</div>', unsafe_allow_html=True)

with c2:
    u_env = st.text_input("🌍 地點與光影 (中文)", placeholder="例如：現代化辦公室，白畫光")
    if st.button("✨ AI Enhance Environment"):
        with st.spinner("AI 正在優化環境..."):
            st.session_state.env_en = call_ai(u_env, "environment and lighting")

    if st.session_state.env_en:
        st.markdown(f'<div class="enhance-res"><b>AI Enhanced:</b><br>{st.session_state.env_en}</div>', unsafe_allow_html=True)

st.divider()

# 6. 生成提示詞按鈕
if st.button("🚀 生成最終提示詞 (Combine Everything)", type="primary"):
    if u_kw:
        # 邏輯：如果有 AI 擴充就用擴充的，沒有就用翻譯的
        final_sub = st.session_state.sub_en if st.session_state.sub_en else translator.translate(u_kw)
        final_env = st.session_state.env_en if st.session_state.env_en else translator.translate(u_env)
        
        neg = "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render"
        t2i = f"RAW photo, {final_env}. {angle}, {lens}. {final_sub}. {style}, high-fidelity, documentary feel. {neg}"
        i2v = f"Mostly {move_map[move_key]}. [Subject: {final_sub} continues action]. Realistic motion blur. {neg}"
        
        st.success("✅ 生成完成！")
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("#### Step 1: T2I (底圖用)")
        st.code(t2i)
        st.markdown("#### Step 2: I2V (動態用)")
        st.code(i2v)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("請輸入主體動作內容！")
