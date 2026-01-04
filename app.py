 import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione Pagina
st.set_page_config(page_title="Gatto Fortuna Dashboard 🐾", layout="wide")

# CSS per il tema Oro/Fortuna
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    h1 { color: #d4af37; text-align: center; }
    .stMetric { border: 2px solid #d4af37; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Carichiamo il file dati.csv saltando la primissima riga inutile
    # header=1 indica che i nomi delle colonne sono sulla seconda riga
    df = pd.read_csv('dati.csv', header=1)
    # Puliamo i nomi delle colonne da spazi invisibili
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_data()
    
    st.title("🐾 Lucky Cat Jackpot Dashboard 💰")
    st.markdown("---")

    # --- KPI (Indicatori) ---
    # Prendiamo l'ultima riga dei dati
    last_row = df.iloc[-1]
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("💰 Jackpot Attuale", f"€ {last_row['SOMMA JACKPOT SUPERENA8']:,.2f}")
    with c2:
        st.metric("✨ Valore Netto", f"€ {last_row['VALORE NETTO JACKPOT']:,.2f}")
    with c3:
        # Colonna M (Disponibilità mensile su Netto E)
        mensile = last_row['disponibilità mensile (12 mesi) su valore Netto E']
        st.metric("🍀 Spesa Mensile", f"€ {mensile:,.2f}")

    st.markdown("---")

    # --- GRAFICI ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Crescita Jackpot")
        fig_line = px.line(df, x='Data', y='SOMMA JACKPOT SUPERENA8', 
                           color_discrete_sequence=['#FFD700'], markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col_right:
        st.subheader("🍕 Tasse vs Netto (Oggi)")
        netto = last_row['VALORE NETTO JACKPOT']
        tasse = last_row['VALORE TAX DA TOGLIERE€']
        fig_pie = px.pie(names=['Netto', 'Tasse'], values=[netto, tasse],
                         color_discrete_sequence=['#228B22', '#FF4500'])
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABELLA ---
    st.subheader("📋 Storico Dati Completo")
    st.dataframe(df, use_container_width=True)

    # --- EXPORT ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Scarica in CSV", data=csv, file_name="jackpot_report.csv")

except Exception as e:
    st.error(f"Errore: {e}")
    st.info("Assicurati che il file su GitHub si chiami esattamente: dati.csv")
