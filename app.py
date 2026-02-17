import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io

# API Key
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Ultimate Studio", page_icon="📸", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("💎 Studio Panel")
    
    st.subheader("1. Background & Size")
    size_option = st.selectbox("Platform Standards", ["Original Size", "Square (1:1)", "Portrait (4:5)"])
    
    # ARKA PLAN SENARYOLARI (Geliştirildi)
    bg_style = st.selectbox(
        "Background Scenario",
        ["Pure White", "Soft Grey", "Modern Marble", "Warm Wood", "Luxury Black"]
    )
    
    # Senaryo Renk/Doku Ayarları
    bg_config = {
        "Pure White": (255, 255, 255),
        "Soft Grey": (240, 240, 240),
        "Modern Marble": (220, 220, 220), # Mermer tonu
        "Warm Wood": (210, 180, 140),     # Ahşap tonu
        "Luxury Black": (20, 20, 20)      # Siyah tonu
    }
    
    st.divider()
    st.subheader("2. Pro Effects")
    add_shadow = st.checkbox("Add Depth Shadow", value=True)
    
    st.divider()
    st.subheader("3. Tuning")
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    
    st.divider()
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- MAIN PAGE ---
st.title("📸 SellSnap AI: Ultimate Product Studio")

uploaded_files = st.file_uploader("Upload product photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button('🚀 Apply AI Magic'):
        for uploaded_file in uploaded_files:
            with st.status(f"Processing {uploaded_file.name}..."):
                # 1. Background Removal (Transparent Mode)
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto'}, # Şeffaf olarak alıyoruz ki alta doku ekleyebilelim
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    foreground = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    # 2. Senaryo Arka Planı Oluşturma
                    # Sadece renk değil, resmin boyutunda bir katman oluşturuyoruz
                    background = Image.new("RGBA", foreground.size, bg_config[bg_style] + (255,))
                    
                    # Ürünü arka plana yapıştır
                    img = Image.alpha_composite(background, foreground)
                    
                    # 3. Resizing
                    if size_option == "Square (1:1)":
                        w, h = img.size
                        side = min(w, h)
                        img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))

                    # 4. Brightness
                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    
                    # 5. YENİ FİLİGRAN (Daha Büyük ve Ortada)
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    wm_text = "SellSnap AI Preview"
                    
                    # Font boyutu resmin genişliğine göre otomatik ayarlansın
                    font_size = int(w / 10) 
                    try:
                        # Streamlit sunucusunda varsayılan fontu yükle
                        font = ImageFont.load_default() 
                    except:
                        font = None
                    
                    # Filigranı resmin tam ortasına büyükçe yaz (yarı şeffaf)
                    draw.text((w//6, h//2), wm_text, fill=(150, 150, 150, 180))
                    
                    st.image(img, caption=f'Ultimate Studio: {uploaded_file.name}', width=500)
                    
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(
                        label=f"Download {uploaded_file.name}", 
                        data=buf.getvalue(), 
                        file_name=f"sellsnap_{uploaded_file.name}", 
                        mime="image/png",
                        key=f"final_{uploaded_file.name}"
                    )
