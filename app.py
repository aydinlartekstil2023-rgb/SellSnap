import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw
import io

# API Key
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

# Sayfa Ayarları
st.set_page_config(page_title="SellSnap AI - Business Editor", page_icon="📸", layout="wide")

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
    
    # Fiyatlandırma ve Shopier Linki
    st.success("Pro Account: No Watermark & High Speed")
    # Shopier onayından sonra linki buradan güncelleyebilirsin
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")
    st.info("Support: sellsnap-support@mail.com")

# --- MAIN PAGE ---
st.title("📸 SellSnap AI: Business Photo Editor")
st.write("Professional product photos in one click. Bulk upload supported!")

# Toplu Dosya Yükleme
uploaded_files = st.file_uploader("Upload your product photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.info(f"📂 {len(uploaded_files)} photos ready for processing.")
    
    if st.button('🚀 Start Bulk Processing'):
        # Her bir fotoğraf için döngü
        for uploaded_file in uploaded_files:
            with st.status(f"Processing: {uploaded_file.name}...", expanded=False):
                # 1. Background Removal API
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto', 'bg_color': bg_color.replace("#", "")},
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    # 2. Resizing
                    if size_option == "Square (1:1) - Amazon/Etsy":
                        width, height = img.size
                        new_size = min(width, height)
                        img = img.crop(((width - new_size) // 2, (height - new_size) // 2, (width + new_size) // 2, (height + new_size) // 2))
                    
                    # 3. Enhancements
                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                    
                    # 4. Watermark (Filigran)
                    draw = ImageDraw.Draw(img)
                    w, h = img.size
                    draw.text((w//4, h//2), "SellSnap AI Preview", fill=(200, 200, 200, 128))
                    
                    # Sonuçları Göster
                    st.image(img, caption=f'Result: {uploaded_file.name}', width=400)
                    
                    # İndirme Butonu (Hatanın düzeltildiği kısım: Özel Key eklendi)
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

# --- FAQ SECTION ---
st.header("🤔 Frequently Asked Questions")
with st.expander("How to remove watermarks?"):
    st.write("Watermarks are automatically removed when you upgrade to a Pro Account by purchasing credits.")
with st.expander("Is my data secure?"):
    st.write("Yes, we do not store your images. They are processed and deleted immediately.")
