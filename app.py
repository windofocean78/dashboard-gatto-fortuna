import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Lucky Cat Jackpot Dashboard 🐱💰",
    page_icon="🐾",
    layout="wide"
)

# --- STILE CSS PERSONALIZZATO (Tema Gatto/Oro) ---
st.markdown("""
    <style>
    .main { background-color: #fdfaf0; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; border: 2px solid #ffd700; }
    h1, h2, h3 { color: #b8860b; font-family: 'Trebuchet MS'; }
    .stButton>button { background-color: #ffd700; color: black; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE CARICAMENTO DATI ---
@st.cache_data
def load_data(file):
    # Salta la prima riga di metadati se necessario e carica gli header corretti
    df = pd.read_csv(file, header=1)
    # Pulizia nomi colonne (rimozione spazi extra)
    df.columns = [c.strip() for c in df.columns]
    # Conversione Data
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])
    return df

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616430.png", width=100) # Icona Gatto
st.sidebar.title("🐾 Menu Fortuna")

uploaded_file = st.sidebar.file_uploader("Carica il file della Progressione", type=["csv", "xlsx"])

# Input manuali richiesti
st.sidebar.markdown("---")
st.sidebar.subheader("💎 Parametri Target")
jackpot_target = st.sidebar.number_input("Jackpot Previsto (€)", value=100000000, step=1000000)
tasso_tasse = st.sidebar.slider("Percentuale Tasse (%)", 0, 30, 20)

# --- LOGICA PRINCIPALE ---
if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    st.title("🍀 Dashboard Jackpot: Il Gatto della Fortuna 🐱")
    st.markdown(f"### Analisi della progressione fino a € {jackpot_target:,.2f}")

    # --- KPI (INDICATORI ALTO) ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcolo valori basati sull'ultimo record o sul target
    ultimo_jackpot = df['SOMMA JACKPOT SUPERENA8'].iloc[-1]
    netto_stimato = ultimo_jackpot * (1 - tasso_tasse/100)
    mensile_max = netto_stimato / (50 * 12) # Esempio su 50 anni
    
    col1.metric("Jackpot Attuale", f"€ {ultimo_jackpot:,.0f} 💰")
    col2.metric("Valore Netto (Stimato)", f"€ {netto_stimato:,.0f} ✨")
    col3.metric("Spesa Mensile (50 anni)", f"€ {mensile_max:,.2f} 🐾")
    col4.metric("Tasse Dovute", f"€ {ultimo_jackpot - netto_stimato:,.0f} 🏛️")

    st.markdown("---")

    # --- GRAFICI ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("📈 Crescita del Jackpot nel Tempo")
        fig_line = px.line(df, x='Data', y='SOMMA JACKPOT SUPERENA8', 
                           title="Progressione Jackpot",
                           line_shape='spline', render_mode='svg')
        fig_line.update_traces(line_color='#ffd700')
        st.plotly_chart(fig_line, use_container_width=True)

    with row1_col2:
        st.subheader("🍕 Ripartizione Valore (Ultimo Dato)")
        labels = ['Valore Netto', 'Tasse']
        values = [netto_stimato, ultimo_jackpot - netto_stimato]
        fig_pie = px.pie(names=labels, values=values, 
                         color_discrete_sequence=['#228B22', '#FF4500'],
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- ISTOGRAMMA ---
    st.subheader("📊 Frequenza Valori Jackpot")
    fig_hist = px.histogram(df, x='SOMMA JACKPOT SUPERENA8', nbins=20, 
                            color_discrete_sequence=['#b8860b'],
                            title="Distribuzione degli importi")
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- TABELLA DATI ---
    with st.expander("📄 Visualizza Tabella Dati Completa"):
        st.dataframe(df.style.format(subset=['SOMMA JACKPOT SUPERENA8', 'VALORE NETTO JACKPOT'], formatter="€ {:,.2f}"))

    # --- EXPORT ---
    st.markdown("### 📥 Esporta i tuoi sogni")
    c_csv, c_xlsx = st.columns(2)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    c_csv.download_button("Scarica in CSV 📄", data=csv_data, file_name="jackpot_data.csv", mime="text/csv")
    
    st.info("💡 **Consiglio del Gatto:** Per salvare in **PDF**, premi `Ctrl+P` (o `Cmd+P` su Mac) e seleziona 'Salva come PDF'. La dashboard è già formattata per la stampa!")

else:
    st.warning("🐾 Benvenuto! Per favore, carica il file Excel o CSV nella barra laterale per iniziare l'analisi.")
    # Mostra un'immagine di benvenuto
    st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?q=80&w=1000&auto=format&fit=crop", caption="Il tuo gatto della fortuna ti aspetta!")
