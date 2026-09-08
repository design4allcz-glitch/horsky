import streamlit as st
import urllib.parse

st.set_page_config(page_title="Porovnání inzerce aut", page_icon="🚗", layout="centered")

st.title("🚗 Rychlé porovnání inzerce aut")
st.write("Zadejte parametry vozidla a aplikace pro vás připraví přímé odkazy na předvyhledané inzeráty na českých webech.")

with st.form("car_search_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.text_input("Značka", value="Skoda")
        model = st.text_input("Model / typ", value="Scala")
        year = st.number_input("Rok výroby", min_value=2000, max_value=2026, value=2020)
        
    with col2:
        fuel = st.selectbox("Typ paliva", ["Benzín", "Nafta", "Hybrid", "Elektro"])
        km = st.number_input("Počet kilometrů", min_value=0, max_value=500000, value=85000, step=5000)
        price = st.number_input("Zadaná cena (Kč)", min_value=0, value=350000, step=10000)

    submitted = st.form_submit_button("Vygenerovat odkazy na inzerci")

if submitted:
    query = f"{brand} {model}"
    
    sauto_url = f"https://www.sauto.cz/inzerce/osobni/{urllib.parse.quote(brand.lower())}/{urllib.parse.quote(model.lower())}"
    tipcars_url = f"https://www.tipcars.com/zarazeni?s=hledat&q={urllib.parse.quote(query)}"
    bazos_url = f"https://auto.bazos.cz/inzerce/?hledat={urllib.parse.quote(query)}&rubriky=auto"
    
    st.success("Parametry byly úspěšně zpracovány!")
    
    st.markdown("**Přehled odkazů na trh**")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("**🇨🇿 Sauto.cz**")
        st.markdown(f"[Otevřít výsledky]({sauto_url})")
        
    with col_b:
        st.markdown("**🚗 TipCars.com**")
        st.markdown(f"[Otevřít výsledky]({tipcars_url})")
        
    with col_c:
        st.markdown("**🛒 Bazoš.cz**")
        st.markdown(f"[Otevřít výsledky]({bazos_url})")
        
    st.markdown("---")
    st.info(
        f"Porovnávané auto: **{brand} {model}** | Rok: **{year}** | "
        f"Nájezd: **{km:,} km** | Vaše cena: **{price:,.0f} Kč**"
    )
