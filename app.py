import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io

API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Pro Business Editor", page_icon="📸", layout="wide")

# --- SIDEBAR (Pro Options) ---
with st.sidebar:
    st.title("💎 Business Panel")
    
    st.subheader("1. Platform Size")
    size_option = st.selectbox(
        "Auto-Resize for:",
        ["Original Size", "Square (1:1) - Amazon/Etsy", "Portrait (4:5) - Instagram", "Landscape (16:9)"]
    )
    
    st.divider()
    
    st.subheader("2. Visual Settings")
    bg_color = st.color_picker("Background Color", "#FFFFFF")
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    
    st.divider()
    
    # Fiyatlandırma Bilgisi
    st.success("Pro Account: No Watermark & High Speed")
    st.link_button("Get 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")
    st.info("Support: sellsnap-support@mail.com")

# --- MAIN PAGE ---
st.title("📸 SellSnap AI: Business Photo Editor")
st.write("Upload multiple photos and get them ready for your store in seconds.")

# ÖZELLİK 2: Toplu Fotoğraf Yükleme (accept_multiple_files=True)
uploaded_files = st.file_uploader("Upload your product photos (Bulk support)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"📂 {len(uploaded_files)} photos uploaded. Ready to process!")
    
    if st.button('🚀 Start Bulk Processing'):
        # Her bir fotoğraf için döngü başlatıyoruz
        for uploaded_file in uploaded_files:
            with st.status(f"Processing {uploaded_file.name}...", expanded=True):
                # 1. API - Arka Plan Silme
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto', 'bg_color': bg_color.replace("#", "")},
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    # 2. Resizing Logic
                    if size_option == "Square (1:1) - Amazon/Etsy":
                        width, height = img.size
                        new_size = min(width, height)
                        img = img.crop(((width - new_size) // 2, (height - new_size) // 2, (width + new_size) // 2, (height + new_size) // 2))
                    
                    # 3. Brightness & Contrast
                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                    
                    # ÖZELLİK 3: Filigran (Watermark) Ekleme
                    # Ücretsiz versiyonda resmin ortasına hafif bir yazı ekliyoruz
                    draw = ImageDraw.Draw(img)
                    width, height = img.size
                    text = "SellSnap AI Preview"
                    # Basit bir filigran çizimi (Yazı tipi dosyası gerektirmeyen standart yöntem)
                    draw.text((width//4, height//2), text, fill=(200, 200, 200, 128))
                    
                    # Görseli Göster ve İndir
                    st.image(img, caption=f'Result: {uploaded_file.name}', width=300)
                    
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(label=f"Download {uploaded_file.name}", data=buf.getvalue(), file_name=f"sellsnap_{uploaded_file.name}", mime="image/png")
                else:
                    st.error(f"Error on {uploaded_file.name}: API credits might be empty.")

st.divider()
# FAQ Kısmı buraya eklenebilir...
