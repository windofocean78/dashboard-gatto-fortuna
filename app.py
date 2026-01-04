 import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lucky Cat Dashboard 🐾", layout="wide")

# Tema Gatto e Fortuna
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    h1 { color: #d4af37; text-align: center; font-weight: bold; }
    .stMetric { background-color: #ffffff; border: 2px solid #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('dati.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

try:
    df = load_data()
    st.title("🐾 Lucky Cat Jackpot Dashboard 💰")
    
    # Ultimi dati disponibili
    last = df.iloc[-1]

    # Indicatori Principali
    c1, c2, c3 = st.columns(3)
    c1.metric("Jackpot Lordo", f"€ {last['Somma_Jackpot']:,.2f}")
    c2.metric("Valore Netto", f"€ {last['Valore_Netto']:,.2f}")
    c3.metric("Disponibilità Mensile", f"€ {last['Disp_Mensile_E']:,.2f}")

    st.markdown("---")

    # Grafici
    g1, g2 = st.columns(2)
    
    with g1:
        st.subheader("📈 Crescita del Sogno")
        fig1 = px.line(df, x='Data', y='Somma_Jackpot', color_discrete_sequence=['#d4af37'])
        st.plotly_chart(fig1, use_container_width=True)
        
    with g2:
        st.subheader("🍕 Ripartizione Stato vs Te")
        fig2 = px.pie(names=['Tuo Netto', 'Tasse Stato'], 
                     values=[last['Valore_Netto'], last['Valore_Tax']],
                     color_discrete_sequence=['#228B22', '#FF4500'], hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📊 Analisi dei 4 Conti")
    split_val = last['Split_4_Conti']
    fig3 = px.bar(x=['Conto 1', 'Conto 2', 'Conto 3', 'Conto 4'], 
                  y=[split_val]*4, 
                  title="Suddivisione del Capitale nei conti",
                  color_discrete_sequence=['#d4af37'])
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📋 Guarda la tabella dei dati puliti"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Errore tecnico: {e}")
