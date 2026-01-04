import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gatto Fortuna Dashboard", layout="wide")

# Funzione per leggere il file caricato su GitHub
@st.cache_data
def load_initial_data():
    # header=1 perché il tuo file ha una riga vuota all'inizio
    df = pd.read_csv('dati.csv', header=1)
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_initial_data()
    st.title("🐾 Jackpot Dashboard")
    
    # Grafico a torta richiesto
    st.subheader("💰 Ripartizione Valore Netto e Tasse")
    ultima_riga = df.iloc[-1]
    fig = px.pie(values=[ultima_riga['VALORE NETTO JACKPOT'], ultima_riga['VALORE TAX DA TOGLIERE€']], 
                 names=['Netto', 'Tasse'],
                 color_discrete_sequence=['#FFD700', '#FF4500'])
    st.plotly_chart(fig)
    
    st.dataframe(df)
except Exception as e:
    st.error(f"Miao! C'è un problema con i dati: {e}")
