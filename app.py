import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai

# 1. 頁面配置與高級感 CSS (置中優化)
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    /* 全域背景與置中 */
    .main { background-color: #050505; color: #e0e0e0; }
    .block-container { padding-top: 2rem; max-width: 800px !important; }
    
    /* 輸入框與文字區 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #1a1a1a !important; color: white !important; 
        border-radius: 12px !important; border: 1px solid #333 !important;
        transition: 0.3s;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #4f46e5 !important; box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
    }
    
    /* 按鈕優化 */
    .stButton>button { 
        border-radius: 12px; height: 3.5em; background-color: #4f46e5; 
        color: white; border: none; width: 100%; font-weight: bold;
        letter-spacing: 1px;
    }
    .stButton>button:hover { 
        background-color: #6366f1; transform: translateY(-2px); 
        box-shadow: 0 5px 15px rgba(79, 70, 229, 0.4);
    }
    
    /* AI 擴充結果區 */
    .enhance-res { 
        background-color: #0e1117; padding: 15px; border-radius: 12px; 
        border-left: 4px solid #818cf8; margin: 15px 0; 
        font-style: italic; color: #cbd5e1; font-size: 0.95em;
    }
    
    /* 結果卡片區 */
    .result-card { 
        background-color: #111; padding: 25px; border-radius: 18px; 
        border: 1px solid #222; border-top: 4px solid #4f46e5; 
        margin-top: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    code { color: #818cf8 !important; font-size: 1.1em !important; background-color: #1a1a1a !important; padding: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化 API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 修正 404 關鍵：加上 models/ 前綴
    model = genai.GenerativeModel('models/gemini-1.5-flash')
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
        prompt = f"You are a cinematic prompt expert. Expand the following {part} into a detailed, high-fidelity English description for AI video generation (T2I2V). Use sensory words and professional cinematography terms. Return ONLY the expanded English text.\nContent: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"

# 4. 主畫面介面 (置中排列)
st.title("📽️ T2I2V Studio Pro")
st.markdown("##### 專業實拍提示詞工作站")
st.caption("支援 Gemini AI 自動擴充細節與全套影視運鏡邏輯")

# --- 攝影參數區 ---
with st.expander("🎥 攝影機與運鏡設定 (Camera Settings)", expanded=True):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        style = st.selectbox("影視風格", ["National Geographic", "Kodak Portra 400", "Arri Alexa Cinematic", "IMAX 70mm", "Fashion Editorial"])
        lens = st.selectbox("焦段", ["8mm Fisheye", "14mm Ultra-Wide", "24mm Wide", "35mm Classic", "50mm Standard", "85mm Portrait", "200mm Telephoto"])
    with col_s2:
        angle = st.selectbox("鏡位角度", ["Eye-level shot", "High angle shot", "Low angle shot", "Dutch angle", "Front angle", "Over-the-shoulder"])
        move_map = {
            "Static (靜態)": "static camera, no movement",
            "Handheld (手持微動)": "subtle handheld micro-movement",
            "Zoom In (縮放-近)": "slow zoom in, focusing on details",
            "Orbit (環繞運鏡)": "360-degree orbit around the subject",
            "Dolly In (推入運鏡)": "camera dollies in physically closer",
            "Jib Down (搖臂下降)": "jib down movement, lowering perspective",
            "360 roll (360度翻轉)": "cinematic 360-degree barrel roll"
        }
        move_key = st.selectbox("運鏡方式", list(move_map.keys()))

st.divider()

# --- 輸入區 ---
u_kw = st.text_area("✍️ 主體動作 (中文)", placeholder="例如：女孩在草地上奔跑", height=100)
if st.button("✨ 使用 AI 擴充主體細節"):
    if u_kw:
        with st.spinner("AI 正在編織細節..."):
            st.session_state.sub_en = call_ai(u_kw, "subject action")
    else: st.warning("請先輸入內容")

if st.session_state.sub_en:
    st.markdown(f'<div class="enhance-res"><b>AI Enhanced Subject:</b><br>{st.session_state.sub_en}</div>', unsafe_allow_html=True)

u_env = st.text_input("🌍 地點與光影 (中文)", placeholder="例如：黃昏，金色柔光")
if st.button("✨ 使用 AI 擴充環境細節"):
    if u_env:
        with st.spinner("AI 正在打造場景..."):
            st.session_state.env_en = call_ai(u_env, "environment and lighting")
    else: st.warning("請先輸入內容")

if st.session_state.env_en:
    st.markdown(f'<div class="enhance-res"><b>AI Enhanced Environment:</b><br>{st.session_state.env_en}</div>', unsafe_allow_html=True)

st.divider()

# --- 生成結果 ---
if st.button("🚀 生成最終雙語提示詞", type="primary"):
    if u_kw:
        with st.spinner("正在統整最終提示詞..."):
            # 優先使用 AI 擴充
            final_sub = st.session_state.sub_en if st.session_state.sub_en else translator.translate(u_kw)
            final_env = st.session_state.env_en if st.session_state.env_en else translator.translate(u_env)
            
            neg = "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render"
            
            # 組合 T2I (底圖)
            t2i = f"RAW photo, {final_env}. {angle}, {lens}. {final_sub}. {style}, high-fidelity, documentary feel. {neg}"
            
            # 組合 I2V (動態)
            i2v = f"Mostly {move_map[move_key]}. [Subject: {final_sub} continues action]. Realistic motion blur. {neg}"
            
            st.success("✅ 提示詞組合完成！")
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("#### Step 1: T2I (Kling/Midjourney) 底圖用")
            st.code(t2i)
            st.markdown("#### Step 2: I2V (Runway/Kling) 動態用")
            st.code(i2v)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.info("💡 提示：請先使用 Step 1 生成高品質圖片，再將圖上傳並套用 Step 2 的動態描述。")
    else:
        st.error("請至少輸入主體動作！")
