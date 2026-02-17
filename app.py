import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io

# API Key
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Ultimate Studio", page_icon="📸", layout="wide")

# --- SIDEBAR (Stüdyo Kontrolleri) ---
with st.sidebar:
    st.title("💎 Studio Panel")
    
    st.subheader("1. Background & Size")
    size_option = st.selectbox("Platform Standards", ["Original Size", "Square (1:1)", "Portrait (4:5)"])
    
    # Arka Plan Senaryoları
    bg_style = st.selectbox(
        "Background Scenario",
        ["Pure White", "Soft Grey", "Modern Marble", "Warm Wood", "Luxury Black"]
    )
    
    # Senaryo için renk/doku tanımları
    bg_config = {
        "Pure White": (255, 255, 255),
        "Soft Grey": (220, 222, 225),
        "Modern Marble": (214, 214, 214), # Mermer doku tonu
        "Warm Wood": (193, 154, 107),     # Ahşap doku tonu
        "Luxury Black": (15, 15, 15)      # Derin siyah
    }
    
    st.divider()
    
    st.subheader("2. Pro Effects")
    # HD Seçeneği Geri Geldi!
    hd_upgrade = st.checkbox("HD Resolution Upgrade (2x)", value=True)
    add_shadow = st.checkbox("Add Depth Shadow", value=True)
    
    st.divider()
    st.subheader("3. Tuning")
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    
    st.divider()
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- ANA SAYFA ---
st.title("📸 SellSnap AI: Ultimate Product Studio")

uploaded_files = st.file_uploader("Upload product photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button('🚀 Apply AI Magic'):
        for uploaded_file in uploaded_files:
            with st.status(f"Processing {uploaded_file.name}..."):
                # 1. API - Arka Planı SİL (Şeffaf Mod)
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto'}, 
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    foreground = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    # 2. HD Yükseltme
                    if hd_upgrade:
                        w, h = foreground.size
                        foreground = foreground.resize((w*2, h*2), Image.Resampling.LANCZOS)
                    
                    # 3. Arka Plan Senaryosu Uygulama (Arka Plan Çalışıyor!)
                    background = Image.new("RGBA", foreground.size, bg_config[bg_style] + (255,))
                    img = Image.alpha_composite(background, foreground)
                    
                    # 4. Boyutlandırma
                    if size_option == "Square (1:1)":
                        w, h = img.size
                        side = min(w, h)
                        img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))

                    # 5. Görsel Ayarları
                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                    
                    # 6. DEV FİLİGRAN (Tam Ortada ve Büyük)
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    wm_text = "SellSnap AI\nPreview" # Alt alta iki satır
                    
                    # Font boyutu ve yerleşimi
                    draw.multiline_text((w//5, h//2.5), wm_text, fill=(180, 180, 180, 150), align="center", spacing=10)
                    
                    st.image(img, caption=f'Studio Result: {uploaded_file.name}', width=600)
                    
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
                    st.error(f"Error: {uploaded_file.name} - API Credits Empty.")
