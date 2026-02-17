import streamlit as st
import requests

# API Anahtarın (Yeni Metin Belgesi.py içindeki anahtarın)
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap - Profesyonel Arka Plan Silici", page_icon="📸")

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("💎 Pro Seçenekler")
    st.write("Daha fazla fotoğraf düzenlemek için kredi satın alın.")
    
    # Shopier onaylanınca buradaki linki gerçek ürün linkinle değiştireceğiz
    st.link_button("50 Kredi Satın Al - 149 TL", "https://www.shopier.com/sellsnap_yakinda")
    
    st.divider()
    st.info("Ödeme sonrası kredileriniz manuel olarak tanımlanacaktır. Destek için: sellsnap-support@mail.com")

# --- ANA SAYFA ---
st.title("📸 SellSnap: Yapay Zeka ile Arka Plan Sil")
st.markdown("""
### 🚀 Ürün Fotoğraflarınızı Saniyeler İçinde Stüdyo Kalitesine Getirin!
* **Yıldırım Hızı:** Tek tıkla sonuç alın.
* **Profesyonel:** E-ticaret siteleri (Amazon, Trendyol vb.) için tam uyumlu.
* **Ücretsiz Deneme:** İlk 3 fotoğrafın temizlenmesi tamamen bizden!
""")

uploaded_file = st.file_uploader("Bir fotoğraf seçin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Yüklenen Fotoğraf', use_container_width=True)
    
    if st.button('Arka Planı Temizle'):
        with st.spinner('İşleniyor...'):
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': uploaded_file.getvalue()},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )
            
            if response.status_code == requests.codes.ok:
                st.image(response.content, caption='Sonuç', use_container_width=True)
                st.download_button(label="Fotoğrafı İndir", data=response.content, file_name="sellsnap_sonuc.png", mime="image/png")
                st.success("İşlem Başarılı!")
            else:
                st.error(f"Hata: {response.status_code}. API krediniz bitmiş olabilir.")
