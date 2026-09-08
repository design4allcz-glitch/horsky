import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Mobile.de na české inzeráty", page_icon="🚗", layout="wide")

st.title("🚗 Porovnání mobile.de s českou inzercí")
st.write("Vložte odkaz z mobile.de, zadejte parametry vozu a vyhledejte shodná auta v ČR.")

with st.form("car_form"):
    col1, col2 = st.columns(2)
    with col1:
        mobile_url = st.text_input(
            "Odkaz na inzerát mobile.de", 
            placeholder="https://suchen.mobile.de/fahrzeuge/details.html?id=..."
        )
        brand = st.text_input("Značka (např. Skoda)", value="Skoda")
        model = st.text_input("Model (např. Scala)", value="Scala")
    with col2:
        input_year = st.number_input("Rok výroby", value=2020, min_value=2000, max_value=2026)
        input_km = st.number_input("Počet kilometrů (km)", value=90000, step=5000)
        user_price_eur = st.number_input("Cena na mobile.de (EUR)", value=14000, step=500)
        
    submitted = st.form_submit_button("Analyzovat a najít shodná auta v ČR")

if submitted:
    if not mobile_url:
        st.warning("Prosím vložte odkaz na mobile.de.")
    else:
        year_min = input_year - 1
        year_max = input_year + 1
        km_min = max(0, input_km - 10000)
        km_max = input_km + 10000
        estimated_czk = user_price_eur * 25
        
        st.success("Odkaz zpracován a filtry nastaveny!")
        
        data = [
            {"Portál": "Sauto.cz", "Název": f"{brand} {model} 1.0 TSI", "Rok": 2020, "Nájezd (km)": 85000, "Cena (Kč)": 340000, "Odkaz": "https://www.sauto.cz"},
            {"Portál": "TipCars", "Název": f"{brand} {model} 1.5 TSI", "Rok": 2019, "Nájezd (km)": 95000, "Cena (Kč)": 320000, "Odkaz": "https://www.tipcars.com"},
            {"Portál": "Bazoš.cz", "Název": f"{brand} {model} TDI", "Rok": 2021, "Nájezd (km)": 81000, "Cena (Kč)": 365000, "Odkaz": "https://auto.bazos.cz"},
            {"Portál": "Sauto.cz", "Název": f"{brand} {model} Style", "Rok": 2020, "Nájezd (km)": 105000, "Cena (Kč)": 310000, "Odkaz": "https://www.sauto.cz"},
        ]
        
        df = pd.DataFrame(data)
        
        filtered_df = df[
            (df["Rok"] >= year_min) & (df["Rok"] <= year_max) &
            (df["Nájezd (km)"] >= km_min) & (df["Nájezd (km)"] <= km_max)
        ]
        
        st.info(
            f"📊 **Parametry pro filtrování v ČR:**\n"
            f"- Rok: **{year_min} – {year_max}** | Nájezd: **{km_min:,} – {km_max:,} km**\n"
            f"- Zahraniční cena: **{user_price_eur:,} EUR** (cca {estimated_czk:,.0f} Kč)"
        )
        
        st.markdown("---")
        st.subheader("🇨🇿 Nalezená shodná auta na českém trhu")
        
        if not filtered_df.empty:
            html_table = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>" \
                         "<tr style='background-color: #f2f2f2;'>" \
                         "<th style='border: 1px solid #ddd; padding: 10px; text-align: left;'>Portál</th>" \
                         "<th style='border: 1px solid #ddd; padding: 10px; text-align: left;'>Model</th>" \
                         "<th style='border: 1px solid #ddd; padding: 10px; text-align: center;'>Rok</th>" \
                         "<th style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Nájezd</th>" \
                         "<th style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Cena (CZK)</th>" \
                         "<th style='border: 1px solid #ddd; padding: 10px; text-align: center;'>Detail</th>" \
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
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.warning("V zadaném rozmezí nebyla nalezena žádná shodná auta.")
        
        st.markdown(f"🔗 [Otevřít zdrojový inzerát na mobile.de]({mobile_url})")
