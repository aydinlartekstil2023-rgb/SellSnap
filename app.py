import streamlit as st
import requests
from PIL import Image, ImageEnhance
import io

API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap AI - Pro Editor", page_icon="📸")

# --- SIDEBAR (Pro Options) ---
with st.sidebar:
    st.title("💎 Pro Options")
    # YENİ ÖZELLİK: Arka Plan Rengi Seçici
    bg_color = st.color_picker("Pick a Background Color", "#FFFFFF")
    
    st.divider()
    # YENİ ÖZELLİK: Parlaklık Ayarı
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
    
    st.divider()
    st.link_button("Buy 50 Credits - $4.99", "https://www.shopier.com/sellsnap_coming_soon")

# --- MAIN PAGE ---
st.title("📸 SellSnap: AI Pro Photo Editor")

uploaded_file = st.file_uploader("Upload your product photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption='Original Photo', use_container_width=True)
    
    if st.button('Magic: Remove & Enhance'):
        with st.spinner('Processing...'):
            # 1. API ile Arka Planı Sil (Şeffaf yap)
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': uploaded_file.getvalue()},
                data={'size': 'auto', 'bg_color': bg_color.replace("#", "")}, # Rengi API'ye gönderiyoruz
                headers={'X-Api-Key': API_KEY},
            )
            
            if response.status_code == requests.codes.ok:
                # 2. Gelen resmi işle (Parlaklık ve Kontrast)
                img = Image.open(io.BytesIO(response.content))
                
                # Parlaklık uygula
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
                
                # Kontrast uygula
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
                
                # Sonucu Göster
                with col2:
                    st.image(img, caption='SellSnap AI Result', use_container_width=True)
                    
                    # İndirme Butonu Hazırla
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(label="Download Pro Result", data=buf.getvalue(), file_name="sellsnap_pro.png", mime="image/png")
            else:
                st.error("API Error. Please check your credits.")

st.divider()
# FAQ Kısmı burada kalabilir...
