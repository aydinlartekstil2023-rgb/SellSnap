import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw, ImageFont # ImageFont'u ekledik
import io

# API Anahtarı
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

# Sayfa Yapılandırması
st.set_page_config(page_title="SellSnap AI - Ultimate Pro", page_icon="📸", layout="wide")

# --- SIDEBAR (Tüm Kontroller Bir Arada) ---
with st.sidebar:
    st.title("💎 Studio Panel")
    
    st.subheader("1. Background & Size")
    size_option = st.selectbox("Platform Standards", ["Original Size", "Square (1:1)", "Portrait (4:5)"])
    
    bg_style = st.selectbox(
        "Background Scenario",
        ["Pure White", "Soft Grey", "Modern Marble", "Warm Wood", "Luxury Black"]
    )
    
    # Renk/Doku Tanımları (Arka planın çalışmama hatası düzeltildi)
    bg_config = {
        "Pure White": (255, 255, 255),
        "Soft Grey": (225, 225, 225),
        "Modern Marble": (210, 210, 210),
        "Warm Wood": (190, 150, 100),
        "Luxury Black": (10, 10, 10)
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
    st.success("Pro Account: No Watermark")
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- ANA SAYFA ---
st.title("📸 SellSnap AI: Ultimate Product Studio")
st.write("Professional photos for Amazon, Etsy & Instagram. (Bulk processing enabled)")

uploaded_files = st.file_uploader("Upload product photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button('🚀 Apply AI Magic (Process All)'):
        for uploaded_file in uploaded_files:
            with st.status(f"Processing {uploaded_file.name}..."):
                # 1. API - Arka Planı Kaldır
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto'}, 
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    foreground = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    # 2. HD Yükseltme (HD buton hatası düzeltildi)
                    if hd_upgrade:
                        w, h = foreground.size
                        foreground = foreground.resize((w*2, h*2), Image.Resampling.LANCZOS)
                    
                    # 3. Senaryo Uygulama (Arka plan çalışıyor)
                    background = Image.new("RGBA", foreground.size, bg_config[bg_style] + (255,))
                    img = Image.alpha_composite(background, foreground)
                    
                    # 4. Kırpma
                    if size_option == "Square (1:1)":
                        w, h = img.size
                        side = min(w, h)
                        img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))

                    # 5. Görsel Ayarları
                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                    
                    # 6. SHUTTERSTOCK TARZI FİLİGRAN
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    wm_text = "SellSnap AI"
                    wm_color = (255, 255, 255, 128) # Beyaz ve yarı şeffaf
                    
                    # Font Boyutu ve Tipi
                    try:
                        # Streamlit cloud'da varsayılan fontu yüklemeye çalış
                        font_size = int(min(w, h) / 10) # Resmin boyutuna göre ayarla
                        font = ImageFont.truetype("arial.ttf", font_size) 
                    except IOError:
                        # Eğer arial.ttf yoksa, varsayılan bir font kullan
                        font = ImageFont.load_default()
                        font_size = int(min(w, h) / 15) # Varsayılan font daha küçük görünebilir
                        
                    # Filigranı 4 köşeye ve ortaya dağıt (köşelerde biraz içeriden başla)
                    positions = [
                        (w * 0.05, h * 0.05), # Sol üst
                        (w * 0.75, h * 0.05), # Sağ üst (metin genişliğini hesaba katarak)
                        (w * 0.05, h * 0.85), # Sol alt
                        (w * 0.75, h * 0.85), # Sağ alt
                        (w * 0.4, h * 0.45)   # Merkez (ürünün üzerine denk gelebilir)
                    ]
                    
                    for pos in positions:
                        draw.text(pos, wm_text, font=font, fill=wm_color)
                        
                    # Gösterim
                    st.image(img, caption=f'Final Output: {uploaded_file.name}', width=500)
                    
                    # İndirme Butonu
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(
                        label=f"Download {uploaded_file.name}", 
                        data=buf.getvalue(), 
                        file_name=f"sellsnap_{uploaded_file.name}", 
                        mime="image/png",
                        key=f"btn_{uploaded_file.name}"
                    )
                else:
                    st.error(f"Error on {uploaded_file.name}: API check failed.")

st.divider()

# --- FAQ SECTION (Geri Getirildi) ---
st.header("🤔 Frequently Asked Questions")
col1, col2 = st.columns(2)
with col1:
    with st.expander("How to remove watermarks?"):
        st.write("Upgrade to a Pro account by purchasing credits. Pro users get watermark-free, 4K results.")
    with st.expander("Is bulk upload free?"):
        st.write("Yes, you can upload multiple photos at once, but each processing step uses AI credits.")
with col2:
    with st.expander("Which platforms are supported?"):
        st.write("We support Amazon, Etsy, Instagram, and Shopify standard sizes automatically.")
    with st.expander("How do I get support?"):
        st.write("Contact us at sellsnap-support@mail.com for any technical issues.")
