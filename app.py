import streamlit as st
import requests
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import io

# API Key
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Ultimate Studio", page_icon="📸", layout="wide")

# --- SIDEBAR (Advanced Pro Options) ---
with st.sidebar:
    st.title("💎 Studio Panel")
    
    st.subheader("1. AI Background & Size")
    size_option = st.selectbox(
        "Platform Standards",
        ["Original Size", "Square (1:1) - Amazon/Etsy", "Portrait (4:5)", "Landscape (16:9)"]
    )
    
    # Yeni Özellik: AI Arka Plan Senaryoları
    bg_style = st.selectbox(
        "Background Style",
        ["Pure White", "Soft Grey", "Warm Wood", "Modern Marble", "Studio Blue"]
    )
    
    # Renk eşleştirme sözlüğü
    bg_map = {
        "Pure White": "#FFFFFF", "Soft Grey": "#F2F2F2",
        "Warm Wood": "#D2B48C", "Modern Marble": "#E0E0E0", "Studio Blue": "#E3F2FD"
    }
    
    st.divider()
    
    st.subheader("2. Professional Effects")
    # Yeni Özellik: Gölge ve HD Upgrade
    add_shadow = st.checkbox("Add Soft Shadow (Depth)", value=True)
    hd_upgrade = st.checkbox("HD Resolution Upgrade", value=False)
    
    st.divider()
    
    st.subheader("3. Image Tuning")
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    
    st.divider()
    st.success("Pro Account: No Watermark")
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- MAIN PAGE ---
st.title("📸 SellSnap AI: Ultimate Product Studio")
st.write("The all-in-one AI solution for global e-commerce sellers.")

uploaded_files = st.file_uploader("Upload product photos (Bulk Processing)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button('🚀 Process with AI Magic'):
        for uploaded_file in uploaded_files:
            with st.status(f"Enhancing: {uploaded_file.name}...", expanded=False):
                # 1. Background Removal
                target_bg = bg_map[bg_style].replace("#", "")
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto', 'bg_color': target_bg},
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                    
                    # 2. HD Upgrade (Upscaling)
                    if hd_upgrade:
                        w, h = img.size
                        img = img.resize((w*2, h*2), Image.Resampling.LANCZOS)
                    
                    # 3. Add Soft Shadow (Gölge Efekti)
                    if add_shadow:
                        # Basit bir gölge katmanı oluşturma
                        shadow = Image.new("RGBA", img.size, (0,0,0,0))
                        draw = ImageDraw.Draw(shadow)
                        # Ürünün altına hafif bir siyahlık
                        draw.ellipse([img.size[0]//4, img.size[1]-50, 3*img.size[0]//4, img.size[1]], fill=(0,0,0,60))
                        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
                        img = Image.alpha_composite(img, shadow)

                    # 4. Resizing Logic
                    if size_option == "Square (1:1) - Amazon/Etsy":
                        width, height = img.size
                        new_size = min(width, height)
                        img = img.crop(((width - new_size) // 2, (height - new_size) // 2, (width + new_size) // 2, (height + new_size) // 2))

                    # 5. Final Enhancements
                    img = ImageEnhance.Brightness(img).enhance(brightness)
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                    
                    # 6. Watermark
                    draw = ImageDraw.Draw(img)
                    draw.text((10, 10), "SellSnap AI Preview", fill=(150, 150, 150, 100))
                    
                    st.image(img, caption=f'Ultimate Result: {uploaded_file.name}', width=400)
                    
                    # Download Button
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(
                        label=f"Download {uploaded_file.name}", 
                        data=buf.getvalue(), 
                        file_name=f"sellsnap_pro_{uploaded_file.name}", 
                        mime="image/png",
                        key=f"pro_{uploaded_file.name}"
                    )
                else:
                    st.error(f"Error: {uploaded_file.name} could not be processed.")

st.divider()
# FAQ ...
