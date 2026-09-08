import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tabulka podobných aut", page_icon="🚗", layout="wide")

st.title("🚗 Vyhledání a tabulka podobných aut")
st.write("Filtruje data v rozmezí $\pm 1$ rok a $\pm 10\,000$ km od zadaných hodnot.")

with st.form("car_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        brand = st.text_input("Značka", value="Skoda")
        model = st.text_input("Model", value="Scala")
    with col2:
        input_year = st.number_input("Rok výroby", value=2020, min_value=2000, max_value=2026)
        input_km = st.number_input("Počet kilometrů (km)", value=90000, step=5000)
    with col3:
        user_price = st.number_input("Vaše cena (Kč)", value=350000, step=10000)
        
    submitted = st.form_submit_button("Filtrovat a zobrazit HTML tabulku")

if submitted:
    year_min = input_year - 1
    year_max = input_year + 1
    km_min = max(0, input_km - 10000)
    km_max = input_km + 10000
    
    # Vzorová databáze inzerátů (zde v reálném provozu probíhá napojení na data ze scraperu nebo API)
    data = [
        {"Portál": "Sauto.cz", "Název": f"{brand} {model} 1.0 TSI", "Rok": 2020, "Nájezd (km)": 85000, "Cena (Kč)": 340000, "Odkaz": "https://www.sauto.cz"},
        {"Portál": "TipCars", "Název": f"{brand} {model} 1.5 TSI", "Rok": 2019, "Nájezd (km)": 95000, "Cena (Kč)": 320000, "Odkaz": "https://www.tipcars.com"},
        {"Portál": "Bazoš.cz", "Název": f"{brand} {model} TDI", "Rok": 2021, "Nájezd (km)": 81000, "Cena (Kč)": 365000, "Odkaz": "https://auto.bazos.cz"},
        {"Portál": "Sauto.cz", "Název": f"{brand} {model} Style", "Rok": 2020, "Nájezd (km)": 105000, "Cena (Kč)": 310000, "Odkaz": "https://www.sauto.cz"},
        {"Portál": "TipCars", "Název": f"{brand} {model} Old", "Rok": 2017, "Nájezd (km)": 140000, "Cena (Kč)": 250000, "Odkaz": "https://www.tipcars.com"},
    ]
    
    df = pd.DataFrame(data)
    
    # Filtrování podle tolerancí: Rok ±1, Nájezd ±10000
    filtered_df = df[
        (df["Rok"] >= year_min) & (df["Rok"] <= year_max) &
        (df["Nájezd (km)"] >= km_min) & (df["Nájezd (km)"] <= km_max)
    ]
    
    st.success(f"Nalezeno {len(filtered_df)} vozů splňujících kritéria (Rok: {year_min}–{year_max}, Nájezd: {km_min:,}–{km_max:,} km).")
    
    if not filtered_df.empty:
        # Vytvoření vlastní HTML tabulky s proklikávacími odkazy
        html_table = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>" \
                     "<tr style='background-color: #f2f2f2;'>" \
                     "<th style='border: 1px solid #ddd; padding: 10px; text-align: left;'>Portál</th>" \
                     "<th style='border: 1px solid #ddd; padding: 10px; text-align: left;'>Model</th>" \
                     "<th style='border: 1px solid #ddd; padding: 10px; text-align: center;'>Rok</th>" \
                     "<th style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Nájezd</th>" \
                     "<th style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Cena</th>" \
                     "<th style='border: 1px solid #ddd; padding: 10px; text-align: center;'>Inzerát</th>" \
                     "</tr>"
        
        for _, row in filtered_df.iterrows():
            html_table += f"<tr>" \
                          f"<td style='border: 1px solid #ddd; padding: 8px;'>{row['Portál']}</td>" \
                          f"<td style='border: 1px solid #ddd; padding: 8px;'>{row['Název']}</td>" \
                          f"<td style='border: 1px solid #ddd; padding: 8px; text-align: center;'>{row['Rok']}</td>" \
                          f"<td style='border: 1px solid #ddd; padding: 8px; text-align: right;'>{row['Nájezd (km)']:,} km</td>" \
                          f"<td style='border: 1px solid #ddd; padding: 8px; text-align: right;'>{row['Cena (Kč)']:,.0f} Kč</td>" \
                          f"<td style='border: 1px solid #ddd; padding: 8px; text-align: center;'><a href='{row['Odkaz']}' target='_blank'>Otevřít</a></td>" \
                          f"</tr>"
        
        html_table += "</table>"
        
        # Vykreslení HTML tabulky v aplikaci
        st.markdown(html_table, unsafe_allow_html=True)
    else:
        st.warning("V tomto rozmezí nebyla v datech nalezena žádná auta. Upravte parametry nebo rozšiřte datovou základnu.")
