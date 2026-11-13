"""
=============================================================================
Autore: Alessandro Passero 
Università: Università Telematica Pegaso
Corso di Laurea: Informatica per le Aziende Digitali (L-31)
Progetto: Project Work (Traccia 28) - Intelligenza Artificiale e Machine Learning 
          per i processi aziendali.
Obiettivo: Progettare un sistema di segmentazione automatica della clientela 
           per un'azienda digitale di servizi.

File: app.py
Descrizione: Dashboard interattiva Streamlit: filtri (zona, periodo, categoria),
             grafici 3D e 2D dei segmenti, profilo medio, scelta di k e
             classificazione di un nuovo cliente.
=============================================================================
"""

# Importazione delle librerie

import streamlit as st  # framework della dashboard web
import pandas as pd  # tabelle e filtri
import plotly.express as px  # grafici interattivi
import joblib  # caricamento dei modelli (.pkl)

# Configurazione pagina
st.set_page_config(page_title="Dashboard Segmentazione Clienti", layout="wide")

# Funzioni di caching per non ricaricare file e modelli a ogni click
@st.cache_data  # dati caricati una sola volta
def load_data():
    d = pd.read_csv('clienti_clusterizzati.csv')
    d['Data_Iscrizione'] = pd.to_datetime(d['Data_Iscrizione'])  # testo -> data, per il filtro sul periodo
    return d

@st.cache_data
def load_valutazione_k():
    return pd.read_csv('valutazione_k.csv')

@st.cache_resource  # modello e scaler tenuti in memoria
def load_models():
    scaler = joblib.load('scaler.pkl')
    kmeans = joblib.load('kmeans_model.pkl')
    return scaler, kmeans

# Caricamento dei file prodotti da ml_pipeline.py
try:
    df = load_data()
    scaler, kmeans = load_models()
except FileNotFoundError:
    st.error("File mancanti. Assicurati di aver eseguito ml_pipeline.py prima di lanciare la dashboard.")
    st.stop()

# --- SIDEBAR: Simulatore Nuovo Cliente ---
st.sidebar.header("🎯 Analizza Nuovo Cliente")
st.sidebar.write("Inserisci i dati per scoprire il segmento di appartenenza.")

new_recency = st.sidebar.number_input("Giorni dall'ultima richiesta (Recency)", min_value=1, value=30)
new_freq = st.sidebar.number_input("Numero di richieste (Frequency)", min_value=1, value=5)
new_money = st.sidebar.number_input("Importo totale speso (Monetary)", min_value=1.0, value=100.0)

if st.sidebar.button("Calcola Cluster"):  # il calcolo parte al clic
    # Stesso ordine delle variabili usato nell'addestramento
    new_data = [[new_recency, new_freq, new_money]]  # giorni, richieste, spesa
    new_data_scaled = scaler.transform(new_data)  # solo transform: media e dev. std dell'addestramento
    pred_cluster = kmeans.predict(new_data_scaled)[0]  # centroide più vicino; [0]: unico cliente
    
    # Recuperiamo il nome del cluster dal dataframe esistente
    nome_cluster = df[df['Cluster_ID'] == pred_cluster]['Nome_Cluster'].iloc[0]
    st.sidebar.success(f"Appartiene al segmento: **{nome_cluster}**")

# --- CORPO PRINCIPALE ---
st.title("📊 Segmentazione Automatica della Clientela")
st.markdown("""
Questa dashboard mostra i risultati dell'algoritmo K-Means applicato ai dati della startup. 
I clienti sono stati raggruppati in base a comportamento di spesa, frequenza e tempo trascorso dall'ultima richiesta.
""")

# Filtri interattivi
col1, col2 = st.columns(2)
zona_scelta = col1.multiselect("Filtra per Zona", options=df['Zona'].unique(), default=df['Zona'].unique())
cat_scelta = col2.multiselect("Filtra per Categoria", options=df['Categoria_Preferita'].unique(), default=df['Categoria_Preferita'].unique())

# Filtro per periodo (data di iscrizione)
d_min, d_max = df['Data_Iscrizione'].min().date(), df['Data_Iscrizione'].max().date()
periodo = st.date_input("Filtra per periodo di iscrizione", value=(d_min, d_max), min_value=d_min, max_value=d_max)
if isinstance(periodo, tuple) and len(periodo) == 2:
    inizio, fine = pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1])
else:  # intervallo incompleto: tutto il periodo
    inizio, fine = pd.Timestamp(d_min), pd.Timestamp(d_max)

# Applicazione filtri
df_filtered = df[(df['Zona'].isin(zona_scelta)) & (df['Categoria_Preferita'].isin(cat_scelta))
                 & (df['Data_Iscrizione'] >= inizio) & (df['Data_Iscrizione'] <= fine)]
if df_filtered.empty:  # nessun cliente: avviso e stop
    st.warning("Nessun cliente corrisponde ai filtri selezionati.")
    st.stop()

st.subheader(f"Distribuzione Clienti ({len(df_filtered)} utenti mostrati)")

# Grafico 3D: le tre variabili RFM, un colore per segmento
fig = px.scatter_3d(df_filtered, 
                    x='Giorni_Ultima_Richiesta', 
                    y='Numero_Richieste', 
                    z='Importo_Speso',
                    color='Nome_Cluster',
                    hover_name='ID_Cliente',
                    hover_data=['Zona', 'Categoria_Preferita'],  # dettagli al passaggio del mouse
                    title="Mappa 3D dei Segmenti (RFM)")

fig.update_layout(scene=dict(
    xaxis_title='Recency (Giorni)',
    yaxis_title='Frequency (Q.tà)',
    zaxis_title='Monetary (€)'
), margin=dict(l=0, r=0, b=0, t=40))

st.plotly_chart(fig, width="stretch")

# Scatter Plot 2D su due caratteristiche significative (Monetary e Recency)
fig_2d = px.scatter(df_filtered,
                    x='Giorni_Ultima_Richiesta',
                    y='Importo_Speso',
                    color='Nome_Cluster',
                    hover_name='ID_Cliente',
                    hover_data=['Zona', 'Categoria_Preferita', 'Numero_Richieste'],
                    title="Importo speso e giorni dall'ultima richiesta",
                    labels={'Giorni_Ultima_Richiesta': 'Recency (Giorni)',
                            'Importo_Speso': 'Monetary (€)',
                            'Nome_Cluster': 'Segmento'})
st.plotly_chart(fig_2d, width="stretch")

# Profilo medio dei segmenti (valori originali, filtrati)
st.subheader("Profilo Medio dei Segmenti")
profilo_medio = df_filtered.groupby('Nome_Cluster')[['Giorni_Ultima_Richiesta', 'Numero_Richieste', 'Importo_Speso']].mean().round(2)
profilo_medio['Numero_Clienti'] = df_filtered['Nome_Cluster'].value_counts()
st.dataframe(profilo_medio, width="stretch")

# Scelta del numero di gruppi: gomito e silhouette
st.subheader("Scelta del numero di gruppi (k)")
try:
    df_k = load_valutazione_k()  # risultati del confronto
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.line(df_k, x='k', y='inertia', markers=True, title="Metodo del gomito (inertia)"), width="stretch")
    c2.plotly_chart(px.line(df_k, x='k', y='silhouette', markers=True, title="Indice di silhouette"), width="stretch")
except FileNotFoundError:
    st.info("Esegui ml_pipeline.py per generare valutazione_k.csv.")


