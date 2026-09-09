import streamlit as st
import urllib.parse

st.set_page_config(page_title="Chytré vyhledávání aut", page_icon="🚗", layout="centered")

st.title("🚗 Vyhledávač aut s přímými filtry na weby")
st.write("Zadejte parametry vozu. Aplikace spočítá toleranci ($\pm 1$ rok, $\pm 10\,000$ km) a otevře weby s hotovým filtrováním.")

with st.form("car_form"):
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("Značka", value="Skoda")
        model = st.text_input("Model", value="Scala")
        input_year = st.number_input("Rok výroby", value=2020, min_value=2000, max_value=2026)
    with col2:
        input_km = st.number_input("Nájezd (km)", value=90000, step=5000)
        user_price = st.number_input("Maximální cena (Kč)", value=350000, step=10000)
        
    submitted = st.form_submit_button("Vygenerovat filtrované odkazy")

if submitted:
    # Výpočet tolerancí
    year_min = input_year - 1
    year_max = input_year + 1
    km_min = max(0, input_km - 10000)
    km_max = input_km + 10000
    
    query = f"{brand} {model}"
    
    # Sestavení odkazů s parametry
    sauto_url = f"https://www.sauto.cz/inzerce/osobni/{urllib.parse.quote(brand.lower())}/{urllib.parse.quote(model.lower())}?rok-vyroby-od={year_min}&rok-vyroby-do={year_max}&tachometr-od={km_min}&tachometr-do={km_max}"
    tipcars_url = f"https://www.tipcars.com/zarazeni?s=hledat&q={urllib.parse.quote(query)}"
    bazos_url = f"https://auto.bazos.cz/inzerce/?hledat={urllib.parse.quote(query)}&rubriky=auto"
    
    st.success("Filtry úspěšně spočítány!")
    
    st.info(
        f"📊 **Hledané rozmezí na internetu:**\n"
        f"- Rok výroby: **{year_min} až {year_max}**\n"
        f"- Nájezd: **{km_min:,} až {km_max:,} km**\n"
        f"- Maximální cena: **{user_price:,.0f} Kč**"
    )
    
    st.markdown("---")
    st.markdown("### Klikněte pro zobrazení výsledků na webech:")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"🇨🇿 **[Sauto.cz]({sauto_url})**")
        st.write("Otevře Sauto s nastaveným rokem a nájezdem.")
    with col_b:
        st.markdown(f"🚗 **[TipCars.com]({tipcars_url})**")
        st.write("Otevře vyhledávání modelu.")
    with col_c:
        st.markdown(f"🛒 **[Bazoš.cz]({bazos_url})**")
        st.write("Otevře inzerci Bazoše.")
