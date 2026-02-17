import streamlit as st
import requests

# Your API Key (from remove.bg)
API_KEY = 'fJNYY4acxhupHR9Rpi3Qoriw' 

st.set_page_config(page_title="SellSnap - AI Background Remover", page_icon="📸")

# --- SIDEBAR ---
with st.sidebar:
    st.title("💎 Pro Options")
    st.write("Need more credits for your professional photos?")
    # Shopier onayından sonra bu linki güncelleyeceğiz
    st.link_button("Buy 50 Credits - $4.99", "https://www.shopier.com/sellsnap_coming_soon")
    st.divider()
    st.info("Credits will be manually added to your account after payment. Support: sellsnap-support@mail.com")

# --- MAIN PAGE ---
st.title("📸 SellSnap: AI-Powered Background Remover")
st.markdown("""
### 🚀 Transform Your Product Photos into Studio Quality in Seconds!
* **Lightning Fast:** Get results with just one click.
* **Professional:** Perfect for e-commerce (Amazon, Etsy, Shopify, etc.).
* **Free Trial:** Your first removals are on us!
""")

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Photo', use_container_width=True)
    
    if st.button('Remove Background'):
        with st.spinner('Processing...'):
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': uploaded_file.getvalue()},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )
            
            if response.status_code == requests.codes.ok:
                st.image(response.content, caption='Result', use_container_width=True)
                st.download_button(label="Download Image", data=response.content, file_name="sellsnap_result.png", mime="image/png")
                st.success("Success!")
            else:
                st.error(f"Error: {response.status_code}. Your API credits might be empty.")

st.divider()

# --- FAQ SECTION ---
st.header("🤔 Frequently Asked Questions")

with st.expander("How does SellSnap work?"):
    st.write("""
    SellSnap uses advanced Artificial Intelligence to detect the subject of your photo and remove the background instantly. 
    It's designed specifically for e-commerce sellers who need clean, white backgrounds for their products.
    """)

with st.expander("Is it free to use?"):
    st.write("""
    Yes! We offer a free trial for every user. If you need to process a large number of photos, 
    you can purchase affordable credit packs from the 'Pro Options' menu.
    """)

with st.expander("Which platforms are these photos suitable for?"):
    st.write("""
    The results are perfect for Amazon, Etsy, eBay, Shopify, and any other online marketplace 
    that requires professional product presentation.
    """)

with st.expander("What happens after I buy credits?"):
    st.write("""
    Once your payment via Shopier is confirmed, our team will manually top up your account credits 
    within 24 hours. You will receive an email notification when your credits are ready to use.
    """)
