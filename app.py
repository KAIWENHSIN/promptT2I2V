import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# ❌ 錯誤示範：genai.configure(api_key="AIzaSy...") 
# ✅ 正確做法：從 Streamlit 的秘密空間讀取
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def ai_enhance(text, part_type):
    if not text: return ""
    
    # 檢查 API Key 是否存在
    if "GEMINI_API_KEY" not in st.secrets:
        return f"⚠️ 錯誤：請在 Secrets 中設定 API Key！"
        
    try:
        # 確保模型是 1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"你是一位專業影視提示詞專家。請將以下『{part_type}』內容擴充為更具電影感、細節豐富的英文描述。只需回傳擴充後的英文內容，不要解釋。\n內容：{text}"
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ API 呼叫失敗：{str(e)}"

# 1. 頁面配置
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="wide")

# 套用深色系高級感 CSS
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1a1a; color: white; border-radius: 10px; border: 1px solid #333; }
    .stButton>button { border-radius: 12px; height: 3.5em; background-color: #4f46e5; color: white; border: none; width: 100%; }
    .stButton>button:hover { background-color: #4338ca; transform: scale(1.02); transition: 0.2s; }
    .result-card { background-color: #111; padding: 20px; border-radius: 15px; border-left: 5px solid #4f46e5; margin-bottom: 20px; }
    code { color: #818cf8 !important; font-size: 1.1em !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化 API (Gemini & Translator)
# 請務必在 Streamlit Secrets 設定 GEMINI_API_KEY
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.warning("⚠️ 偵測到未設定 API Key，Enhance 功能將使用預設模板。")
    model = None

translator = GoogleTranslator(source='auto', target='en')

def ai_enhance(text, part_type):
    """呼叫 Gemini 進行提示詞優化"""
    if not model or not text:
        return f"{text}, cinematic lighting, 8k, highly detailed"
    try:
        prompt = f"你是一位影視大師。請將以下『{part_type}』內容擴充為更具電影感、細節豐富的英文描述。只需回傳擴充後的『英文內容』，不要有任何解釋。\n內容：{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"{text}, hyper-realistic, 8k"

# 3. 側邊欄運鏡設定
with st.sidebar:
    st.title("⚙️ Camera Settings")
    style = st.selectbox("影視風格", ["National Geographic", "Kodak Portra 400", "Arri Alexa Cinematic", "IMAX 70mm", "Fashion Editorial"])
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

# 4. 主介面
st.title("🌐 雙語自動翻譯 T2I2V 工作站")
st.caption("支援 Gemini AI 自動擴充提示詞細節")

col1, col2 = st.columns(2)

# 使用 Session State 存儲 AI 擴充後的結果
if 'sub_enhanced' not in st.session_state: st.session_state.sub_enhanced = ""
if 'env_enhanced' not in st.session_state: st.session_state.env_enhanced = ""

with col1:
    u_kw = st.text_area("✍️ 主體動作 (中文)", placeholder="例如：貓咪在跑步", height=100)
    if st.button("✨ AI Enhance Subject"):
        with st.spinner("AI 正在構思細節..."):
            st.session_state.sub_enhanced = ai_enhance(u_kw, "主體動作")
        st.success("擴充完成！")

with col2:
    u_env = st.text_input("🌍 地點與光影 (中文)", placeholder="例如：森林，陽光透過樹葉")
    if st.button("✨ AI Enhance Environment"):
        with st.spinner("AI 正在設計場景..."):
            st.session_state.env_enhanced = ai_enhance(u_env, "環境與光影")
        st.success("擴充完成！")

# 5. 生成提示詞
st.divider()
if st.button("🚀 生成最終提示詞 (Combine Everything)", type="primary"):
    if u_kw:
        # 優先使用 AI 擴充後的內容，若無則翻譯原始輸入
        final_sub = st.session_state.sub_enhanced if st.session_state.sub_enhanced else translator.translate(u_kw)
        final_env = st.session_state.env_enhanced if st.session_state.env_enhanced else translator.translate(u_env)
        
        neg = "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render"
        t2i = f"RAW photo, {final_env}. {angle}, {lens}. {final_sub}. {style}, high-fidelity, documentary feel. {neg}"
        i2v = f"Mostly {move_map[move_key]}. [Subject: {final_sub} continues the action]. Realistic motion blur. {neg}"
        
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("#### Step 1: T2I (底圖提示詞)")
        st.code(t2i)
        st.markdown("#### Step 2: I2V (影片提示詞)")
        st.code(i2v)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("請至少輸入主體動作！")
