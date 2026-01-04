import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione stile Gatto della Fortuna
st.set_page_config(page_title="Lucky Cat Dashboard 🐾", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    h1 { color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Il tuo file ha una riga vuota all'inizio, quindi usiamo header=1
    df = pd.read_csv('dati.csv', header=1)
    df.columns = [c.strip() for c in df.columns]
    # Convertiamo la colonna Data
    df['Data'] = pd.to_datetime(df['Data'])
    return df

try:
    df = load_data()
    st.title("🐾 Lucky Cat Jackpot Dashboard 💰")
    
    # --- KPI SUPERIORI ---
    ultima_riga = df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Jackpot Totale", f"€ {ultima_riga['SOMMA JACKPOT SUPERENA8']:,.2f}")
    c2.metric("Netto in Tasca", f"€ {ultima_riga['VALORE NETTO JACKPOT']:,.2f}")
    c3.metric("Mensile (su 50 anni)", f"€ {ultima_riga.iloc[13]:,.2f}") # Colonna M

    st.divider()

    # --- GRAFICI ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Crescita Jackpot")
        fig_line = px.line(df, x='Data', y='SOMMA JACKPOT SUPERENA8', color_discrete_sequence=['#FFD700'])
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col_right:
        st.subheader("🍕 Tasse vs Netto")
        fig_pie = px.pie(names=['Netto', 'Tasse'], 
                         values=[ultima_riga['VALORE NETTO JACKPOT'], ultima_riga['VALORE TAX DA TOGLIERE€']],
                         color_discrete_sequence=['#228B22', '#FF4500'])
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABELLA ---
    st.subheader("📑 Storico Completo")
    st.dataframe(df)

except Exception as e:
    st.error(f"Miao! Qualcosa non va nel file dati.csv: {e}")
    st.info("Assicurati che il file si chiami esattamente 'dati.csv' su GitHub.")
