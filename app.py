import streamlit as st
from deep_translator import GoogleTranslator

# 1. 頁面基本配置
st.set_page_config(page_title="T2I2V Studio Pro", page_icon="🎬", layout="wide")

# 套用深色系高級感 CSS
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; border-radius: 10px; border: 1px solid #333; }
    .stTextArea>div>div>textarea { background-color: #1a1a1a; color: white; border-radius: 10px; border: 1px solid #333; }
    .stButton>button { border-radius: 12px; height: 3.5em; background-color: #4f46e5; color: white; border: none; width: 100%; }
    .stButton>button:hover { background-color: #4338ca; border: none; transform: scale(1.02); transition: 0.2s; }
    .result-card { background-color: #111; padding: 20px; border-radius: 15px; border-left: 5px solid #4f46e5; margin-bottom: 20px; }
    code { color: #818cf8 !important; font-size: 1.1em !important; }
    </style>
    """, unsafe_allow_html=True)

# 初始化翻譯器
translator = GoogleTranslator(source='auto', target='en')

# 2. 側邊欄設定 (根據你提供的圖片運鏡)
with st.sidebar:
    st.title("⚙️ Camera Settings")
    style = st.selectbox("影視風格 / Style", ["National Geographic", "Kodak Portra 400", "Arri Alexa Cinematic", "IMAX 70mm", "Fashion Editorial"])
    lens = st.selectbox("焦段 / Lens", ["8mm Fisheye", "24mm Wide", "35mm Classic", "50mm Standard", "85mm Portrait", "200mm Telephoto"])
    angle = st.selectbox("鏡位 / Angle", ["Eye-level shot", "High angle shot", "Low angle shot", "Dutch angle", "Front angle", "Over-the-shoulder"])
    
    st.divider()
    
    # 完全對照圖片的運鏡選項
    move_map = {
        "Static (靜態)": "static camera, no movement",
        "Handheld (手持微動)": "subtle handheld micro-movement, organic feel",
        "Zoom Out (縮放-遠)": "slow zoom out, revealing more environment",
        "Zoom in (縮放-近)": "slow zoom in, focusing on details",
        "Camera follows (跟鏡)": "camera follows the subject movement",
        "Pan left (左橫移搖鏡)": "smooth pan left movement",
        "Pan right (右橫移搖鏡)": "smooth pan right movement",
        "Tilt up (仰拍搖鏡)": "camera tilts up slowly",
        "Tilt down (俯拍搖鏡)": "camera tilts down slowly",
        "Orbit around (環繞運鏡)": "360-degree orbit around the subject",
        "Dolly in (推入運鏡)": "camera dollies in physically closer",
        "Dolly out (拉出運鏡)": "camera dollies out physically away",
        "Jib up (搖臂上升)": "jib up movement, rising perspective",
        "Jib down (搖臂下降)": "jib down movement, lowering perspective",
        "Drone shot (航拍)": "high altitude drone sweeping view",
        "360 roll (360度翻轉)": "cinematic 360-degree barrel roll"
    }
    move_key = st.selectbox("運鏡方式 / Camera Movement", list(move_map.keys()))

# 3. 主畫面介面
st.title("🌐 雙語自動翻譯 T2I2V 工作站")
st.caption("輸入中文自動轉譯為英文 Prompt，支援全套實拍運鏡邏輯")

col1, col2 = st.columns(2)

with col1:
    u_kw = st.text_area("✍️ 主體動作 (直接輸入中文)", placeholder="例如：女孩在草地上奔跑", height=120)
    if st.button("✨ Enhance Subject"):
        if u_kw: st.info(f"AI 建議增強：{u_kw} with cinematic lighting and realistic skin textures.")

with col2:
    u_env = st.text_input("🌍 地點與光影 (直接輸入中文)", placeholder="例如：黃昏，金色柔光")
    if st.button("✨ Enhance Environment"):
        if u_env: st.info(f"AI 建議增強：{u_env}, volumetric fog, highly detailed background.")

st.divider()

# 4. 生成邏輯
if st.button("🚀 生成翻譯提示詞", type="primary"):
    if u_kw:
        with st.spinner("正在轉譯專業影視術語..."):
            # 翻譯 (已處理全形標點問題)
            en_kw = translator.translate(u_kw)
            en_env = translator.translate(u_env) if u_env else "natural lighting"
            
            neg = "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render"
            
            # 組合 T2I (底圖)
            t2i = f"RAW photo, {en_env}. {angle}, {lens}. {en_kw}. {style}, high-fidelity, documentary feel. {neg}"
            
            # 組合 I2V (動態)
            move_desc = move_map[move_key]
            i2v = f"Mostly static camera with {move_desc}. [Subject: {en_kw} continues the same action]. Realistic motion blur, no dramatic camera moves. {neg}"
            
            # 顯示結果
            st.success("✅ 生成完成！")
            
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.markdown("##### 📝 翻譯對照 (Keywords)")
                st.caption(f"EN: {en_kw}")
            with res_c2:
                st.markdown("##### 🌍 翻譯對照 (Environment)")
                st.caption(f"EN: {en_env}")
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("#### Step 1: T2I (Kling/Midjourney) 底圖用")
            st.code(t2i)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("#### Step 2: I2V (Runway/Kling) 動態用")
            st.code(i2v_prompt := i2v)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.info("💡 Pro Tip: 請務必先生成 Step 1 的高品質圖，再將其作為 I2V 的參考圖上傳至 Runway 或 Kling 以維持畫面一致性。")
    else:
        st.error("請輸入主體動作內容！")
