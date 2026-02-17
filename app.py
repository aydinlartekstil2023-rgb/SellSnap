import streamlit as st
import requests

API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw'

st.set_page_config(page_title="Fast Background Remover", page_icon="📸")
st.title("📸 ShopBG: AI-Powered Background Remover")
st.markdown("""
### 🚀 Transform Your Product Photos into Studio Quality in Seconds!
Don't let messy home backgrounds get in the way of your sales. 
* **Lightning Fast:** Get results with just one click.
* **Professional:** Perfect white background for e-commerce.
* **Try for Free:** Your first few removals are on us!
""")
uploaded_file = st.file_uploader("Bir fotoğraf seçin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Yüklenen Fotoğraf', use_column_width=True)
    
    if st.button('Arka Planı Temizle'):
        with st.spinner('İşleniyor...'):
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': uploaded_file.getvalue()},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )
            
            if response.status_code == requests.codes.ok:
                st.image(response.content, caption='Sonuç', use_column_width=True)
                st.download_button(label="Fotoğrafı İndir", data=response.content, file_name="temizlenmiş_foto.png", mime="image/png")
                st.success("İşlem Tamamlandı!")
            else:
                st.error(f"Hata: {response.status_code}")