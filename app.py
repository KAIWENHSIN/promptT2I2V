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
    
    /* 輸入框與文字區樣式 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #1a1a1a !important; color: white !important; 
        border-radius: 12px !important; border: 1px solid #333 !important;
        transition: 0.3s;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #4f46e5 !important; box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
    }
    
    /* 按鈕樣式優化 */
    .stButton>button { 
        border-radius: 12px; height: 3.5em; background-color: #4f46e5; 
        color: white; border: none; width: 100%; font-weight: bold;
        letter-spacing: 1px;
    }
    .stButton>button:hover { 
        background-color: #6366f1; transform: translateY(-2px); 
        box-shadow: 0 5px 15px rgba(79, 70, 229, 0.4);
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
        margin-top: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    code { color: #818cf8 !important; font-size: 1.1em !important; background-color: #1a1a1a !important; padding: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化 API
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 使用標準模型名稱，解決 404 報錯
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
        # 移除可能導致 API 報錯的特殊字元
        clean_text = text.replace('\n', ' ').strip()
        prompt = f"You are a cinematic prompt expert. Expand the following {part} into a detailed, high-fidelity English description for AI video generation. Return ONLY the expanded English text.\nContent: {clean_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"

# 4. 主畫面介面
st.title("📽️ T2I2V Studio Pro")
st.markdown("##### 專業實拍提示詞工作站")
st.caption("支援 Gemini AI 自動擴充與全套實拍運鏡邏輯")

# --- 攝影參數設定 ---
with st.expander("🎥 攝影機與運鏡設定 (Camera Settings)", expanded=True):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        style = st.selectbox("影視風格", ["National Geographic", "Kodak Portra 400", "Arri Alexa Cinematic", "IMAX 70mm", "Fashion Editorial"])
        lens = st.selectbox("焦段", ["8mm Fisheye", "14mm Ultra-Wide", "24mm Wide", "35mm Classic", "50mm Standard", "85mm Portrait", "200mm Telephoto"])
    with col_s2:
        angle = st.selectbox("鏡位角度", ["Eye-level shot", "High angle shot", "Low angle shot", "Dutch angle", "Front angle", "Over-the-shoulder"])
        # 根據 image_3f56d4.png 完整對應運鏡清單
        move_map = {
            "Static (靜態)": "static camera, no movement",
            "Handheld (手持微動)": "subtle handheld micro-movement",
            "Zoom Out (縮放-遠)": "slow zoom out movement",
            "Zoom in (縮放-近)": "slow zoom in movement",
            "Camera follows (跟鏡)": "camera follows the subject movement",
            "Pan left (左橫移搖鏡)": "smooth pan left",
            "Pan right (右橫移搖鏡)": "smooth pan right",
            "Tilt up (仰拍搖鏡)": "slow tilt up",
            "Tilt down (俯拍搖鏡)": "slow tilt down",
            "Orbit around (環繞運鏡)": "360-degree orbit around subject",
            "Dolly In (推入運鏡)": "camera dollies in closer",
            "Dolly Out (拉出運鏡)": "camera dollies out away",
            "Dolly Left (向左平移)": "camera dollies to the left",
            "Dolly Right (向右平移)": "camera dollies to the right",
            "Jib up (搖臂上升)": "jib up shot, rising",
            "Jib down (搖臂下降)": "jib down shot, lowering",
            "Drone shot (航拍)": "high altitude drone sweeping",
            "360 roll (360度翻轉)": "cinematic 360-degree barrel roll"
        }
        move_key = st.selectbox("運鏡方式", list(move_map.keys()))

st.divider()

# --- 使用者輸入區域 ---
u_kw = st.text_area("✍️ 主體動作 (中文)", placeholder="例如：女孩在草地上奔跑", height=100)
if st.button("✨ 使用 AI 擴充主體細節"):
    if u_kw:
        with st.spinner("AI 正在分析動作..."):
            st.session_state.sub_en = call_ai(u_kw, "subject action")
    else: st.warning("請先輸入主體動作")

if st.session_state.sub_en:
    st.markdown(f'<div class="enhance-res"><b>AI Enhanced Subject:</b><br>{st.session_state.sub_en}</div>', unsafe_allow_html=True)

u_env = st.text_input("🌍 地點與光影 (中文)", placeholder="例如：黃昏，金色柔光")
if st.button("✨ 使用 AI 擴充環境細節"):
    if u_env:
        with st.spinner("AI 正在構建場景..."):
            st.session_state.env_en = call_ai(u_env, "environment and lighting")
    else: st.warning("請先輸入地點環境")

if st.session_state.env_en:
    st.markdown(f'<div class="enhance-res"><b>AI Enhanced Environment:</b><br>{st.session_state.env_en}</div>', unsafe_allow_html=True)

st.divider()

# --- 生成最終提示詞 ---
if st.button("🚀 生成最終雙語提示詞組", type="primary"):
    if u_kw:
        with st.spinner("正在翻譯並統整..."):
            # 若無 AI 擴充結果則使用直接翻譯
            final_sub = st.session_state.sub_en if st.session_state.sub_en else translator.translate(u_kw)
            final_env = st.session_state.env_en if st.session_state.env_en else translator.translate(u_env)
            
            neg = "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render"
            
            # Step 1: T2I Prompt
            t2i = f"RAW photo, {final_env}. {angle}, {lens}. {final_sub}. {style}, high-fidelity, documentary feel. {neg}"
            
            # Step 2: I2V Prompt
            i2v = f"Mostly {move_map[move_key]}. [Subject: {final_sub} continues action]. Realistic motion blur. {neg}"
            
            st.success("✅ 提示詞組合完成！")
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("#### Step 1: T2I (Kling/Midjourney/Luma) 底圖生成")
            st.code(t2i)
            st.markdown("#### Step 2: I2V (Runway/Kling) 影片動態生成")
            st.code(i2v)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.info("💡 建議：請先使用 Step 1 生成高品質底圖，再將圖上傳至影片模型並搭配 Step 2 提示詞。")
    else:
        st.error("主體動作為必填項")
