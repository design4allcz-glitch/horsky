import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Nastavení stránky
st.set_page_config(page_title="Odstraňovač hvězdičky", page_icon="✨", layout="centered")

st.title("✨ Odstraňovač hvězdičky z pravého rohu")
st.write("Nahrajte fotku a aplikace automaticky odstraní objekt v pravém dolním rohu pomocí AI inpaintingu.")

# Nahrání souboru přes webové rozhraní
uploaded_file = st.file_uploader("Vyberte obrázek (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Načtení obrázku pro OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    h, w, _ = img.shape
    
    # Nastavení velikosti oblasti v pravém dolním rohu
    box_size = st.slider("Velikost oblasti k odstranění (v pixelech od pravého dolního rohu)", min_value=50, max_value=500, value=120, step=10)
    
    # Zobrazení originálu s vyznačenou oblastí (pro kontrolu)
    preview_img = img.copy()
    cv2.rectangle(preview_img, (w - box_size, h - box_size), (w, h), (0, 0, 255), 2) # Červený rámeček
    preview_rgb = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
    
    st.image(preview_rgb, caption="Oblast určená k odstranění (označená červeně)", use_container_width=True)
    
    if st.button("Odstranit hvězdičku a vygenerovat výsledek", type="primary"):
        # Vytvoření masky pro inpainting
        mask = np.zeros((h, w), dtype=np.uint8)
        mask[h - box_size:h, w - box_size:w] = 255
        
        # Algoritmus domaluje pozadí namísto hvězdičky
        cleaned_img = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        
        # Převod zpět do RGB pro Streamlit
        cleaned_rgb = cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2RGB)
        final_pil = Image.fromarray(cleaned_rgb)
        
        st.success("Hvězdička byla úspěšně odstraněna!")
        st.image(final_pil, caption="Výsledek bez hvězdičky", use_container_width=True)
        
        # Tlačítko pro stažení výsledku
        buf = io.BytesIO()
        final_pil.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Stáhnout upravenou fotku",
            data=byte_im,
            file_name="bez_hvezdicky.jpg",
            mime="image/jpeg"
        )
