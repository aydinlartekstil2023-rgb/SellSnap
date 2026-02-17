import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw
import io

# API Anahtarı
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Ultimate Studio", page_icon="📸", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("💎 Studio Panel")
    st.subheader("1. Background & Size")
    size_option = st.selectbox("Platform Standards", ["Original Size", "Square (1:1)", "Portrait (4:5)"])
    bg_style = st.selectbox("Background Scenario", ["Pure White", "Soft Grey", "Modern Marble", "Warm Wood", "Luxury Black"])
    
    bg_config = {
        "Pure White": (255, 255, 255), "Soft Grey": (225, 225, 225),
        "Modern Marble": (210, 210, 210), "Warm Wood": (190, 150, 100), "Luxury Black": (10, 10, 10)
    }
    
    st.divider()
    st.subheader("2. Pro Effects")
    hd_upgrade = st.checkbox("HD Resolution Upgrade (2x)", value=True)
    add_shadow = st.checkbox("Add Depth Shadow", value=True)
    
    st.divider()
    st.subheader("3. Tuning")
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    
    st.divider()
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- MAIN PAGE ---
st.title("📸 SellSnap AI: Ultimate Product Studio")

uploaded_files = st.file_uploader("Upload product photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button('🚀 Apply AI Magic (Process All)'):
        for uploaded_file in uploaded_files:
            with st.status(f"Processing {uploaded_file.name}..."):
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto'}, 
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    foreground = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    if hd_upgrade:
                        w, h = foreground.size
                        foreground = foreground.resize((w*2, h*2), Image.Resampling.LANCZOS)
                    
                    background = Image.new("RGBA", foreground.size, bg_config[bg_style] + (255,))
                    img = Image.alpha_composite(background, foreground)
                    
                    if size_option == "Square (1:1)":
                        w, h = img.size
                        side = min(w, h)
                        img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))

                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                    
                    # --- YENİ NESİL PROFESYONEL FİLİGRAN (Grid & Box Style) ---
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    wm_text = " SellSnap AI " # Kenarlarda boşluk bıraktık
                    
                    # Izgara şeklinde tüm resmi kapla
                    step_w = w // 3
                    step_h = h // 4
                    
                    for i in range(0, w, step_w):
                        for j in range(0, h, step_h):
                            # Şekil (Kutu) Çizimi - Görseldeki gibi "Box" efekti verir
                            box_pos = [i + 20, j + 20, i + 280, j + 80]
                            draw.rectangle(box_pos, outline=(150, 150, 150, 80), width=2)
                            # Kalın ve Büyük Metin
                            draw.text((i + 40, j + 35), wm_text, fill=(130, 130, 130, 100))
                    
                    st.image(img, caption=f'Studio Result: {uploaded_file.name}', width=550)
                    
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(
                        label=f"Download {uploaded_file.name}", 
                        data=buf.getvalue(), 
                        file_name=f"sellsnap_{uploaded_file.name}", 
                        mime="image/png",
                        key=f"final_{uploaded_file.name}"
                    )
                else:
                    st.error(f"Error on {uploaded_file.name}")

st.divider()

# --- FAQ SECTION ---
st.header("🤔 Frequently Asked Questions")
col1, col2 = st.columns(2)
with col1:
    with st.expander("How to remove watermarks?"):
        st.write("Watermarks are automatically removed when you upgrade to a Pro Account.")
    with st.expander("Is my data secure?"):
        st.write("Yes, images are processed in real-time and never stored on our servers.")
with col2:
    with st.expander("Payment issues?"):
        st.write("If your credits don't appear after payment, please email sellsnap-support@mail.com.")
