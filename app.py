import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione Pagina
st.set_page_config(page_title="Lucky Cat Jackpot 🐾", layout="wide")

# Funzione per caricare i dati in modo sicuro
def load_data():
    try:
        # Carichiamo saltando la riga vuota iniziale che c'è nel tuo CSV
        df = pd.read_csv('dati.csv', header=1)
        # Puliamo i nomi delle colonne
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")
        return None

df = load_data()

if df is not None:
    st.title("🐾 Lucky Cat: Progressione Jackpot 💰")
    
    # Calcolo indicatori rapidi (usando i nomi reali delle tue colonne)
    ultimo_jackpot = df['SOMMA JACKPOT SUPERENA8'].iloc[-1]
    netto = df['VALORE NETTO JACKPOT'].iloc[-1]
    mensile = df['disponibilità mensile (12 mesi) su valore Netto E'].iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Jackpot Lordo", f"€ {ultimo_jackpot:,.2f}")
    col2.metric("Valore Netto (Post Tasse)", f"€ {netto:,.2f}")
    col3.metric("Spesa Mensile Possibile", f"€ {mensile:,.2f}", delta="🍀 Fortuna")

    st.divider()

    # Grafici
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📈 Crescita nel Tempo")
        fig_line = px.line(df, x='Data', y='SOMMA JACKPOT SUPERENA8', 
                           color_discrete_sequence=['#FFD700'])
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.subheader("📊 Distribuzione Tasse vs Netto")
        tasse = df['VALORE TAX DA TOGLIERE€'].iloc[-1]
        fig_pie = px.pie(values=[netto, tasse], names=['Netto', 'Tasse'], 
                         color_discrete_sequence=['#228B22', '#FF4500'])
        st.plotly_chart(fig_pie, use_container_width=True)

    # Tabella
    st.subheader("📋 Dettaglio Dati")
    st.dataframe(df)

    # Esportazione
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Scarica Report CSV", data=csv, file_name="report_fortuna.csv") 
