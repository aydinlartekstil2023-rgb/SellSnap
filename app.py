import streamlit as st
import requests
from PIL import Image, ImageEnhance
import io

API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Ultimate Editor", page_icon="📸")

# --- SIDEBAR (Pro Options) ---
with st.sidebar:
    st.title("💎 Pro Options")
    
    # BOYUT SEÇENEĞİ (Yeni eklendi)
    st.subheader("1. Choose Size")
    size_option = st.selectbox(
        "Platform Standards",
        ["Original Size", "Square (1:1) - Instagram/Amazon", "Portrait (4:5)", "Landscape (16:9)"]
    )
    
    st.divider()
    
    # RENK VE DÜZENLEME
    st.subheader("2. Enhancement")
    bg_color = st.color_picker("Background Color", "#FFFFFF")
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    
    st.divider()
    st.link_button("Buy 100 Credits - $9.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- MAIN PAGE ---
st.title("📸 SellSnap AI: Ultimate Photo Editor")
st.write("Professional product photos in one click.")

uploaded_file = st.file_uploader("Upload your product photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption='Original', use_container_width=True)
    
    if st.button('🚀 Process Photo'):
        with st.spinner('AI is working...'):
            # 1. Background Removal
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': uploaded_file.getvalue()},
                data={'size': 'auto', 'bg_color': bg_color.replace("#", "")},
                headers={'X-Api-Key': API_KEY},
            )
            
            if response.status_code == requests.codes.ok:
                img = Image.open(io.BytesIO(response.content))
                
                # 2. Resizing (Yeni eklendi)
                if size_option == "Square (1:1) - Instagram/Amazon":
                    width, height = img.size
                    new_size = min(width, height)
                    img = img.crop(((width - new_size) // 2, (height - new_size) // 2, (width + new_size) // 2, (height + new_size) // 2))
                
                # 3. Brightness & Contrast
                img = ImageEnhance.Brightness(img).enhance(brightness)
                img = ImageEnhance.Contrast(img).enhance(contrast)
                
                with col2:
                    st.image(img, caption='SellSnap AI Result', use_container_width=True)
                    
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(label="Download Pro Result", data=buf.getvalue(), file_name="sellsnap_pro.png", mime="image/png")
            else:
                st.error("API Error. Please check your connection or credits.")
