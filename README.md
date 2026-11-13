# Project Work: Segmentazione Automatica della Clientela

Questo repository contiene il codice sorgente e la documentazione relativi al Project Work finale per il corso di studi in Informatica per le Aziende Digitali (Università Telematica Pegaso). 

Il progetto mira a progettare e implementare un sistema per la segmentazione automatica della clientela di una startup digitale, utilizzando tecniche di Machine Learning non supervisionato (K-Means) e fornendo una dashboard interattiva per l'analisi dei risultati.
## 🔊 Attiva l'audio dal player per sentire la spiegazione


https://github.com/user-attachments/assets/e48b6e4e-d30d-4818-b7d8-982bd0d4200e

## 🔊 Attiva l'audio dal player per sentire la spiegazione

## 🎯 Obiettivi del Progetto

1. **Generazione Dati:** Creazione procedurale di un dataset sintetico (300 record) basato su distribuzioni statistiche realistiche (metriche RFM: Recency, Frequency, Monetary).
2. **Machine Learning:** Sviluppo di una pipeline di preprocessing e clustering (K-Means) per individuare segmenti omogenei di clientela, validati matematicamente tramite Indice di Silhouette.
3. **Business Intelligence:** Implementazione di una dashboard interattiva (Streamlit) per l'esplorazione visuale dei cluster e la classificazione in tempo reale di nuovi clienti (inferenza).

## 📂 Struttura del Repository

- `requirements.txt`: Elenco delle dipendenze e librerie necessarie.
- `data_generator.py`: Script per la generazione sintetica dei dati dei clienti.
- `ml_pipeline.py`: Script per la normalizzazione dei dati e l'addestramento del modello K-Means.
- `app.py`: Codice sorgente della web application interattiva (Dashboard).
- `README.md`: Documentazione del progetto.
- `diagram_project.png`: Immagine del diagramma di flusso.
- `graph.txt`: Codice markup generazione grafico visivo con Mermaid Live Editor.
- `clienti_startup.csv`: il dataset generato.
- `clienti_clusterizzati.csv`: i risultati con il segmento di ogni cliente.
- `valutazione_k.csv`: il confronto di k da 2 a 6.
- `figura_8_dashboard.png`: Dashboard Interattiva.
- `figura_9_segmenti.png`: Profilo medio segmenti.
- `figura_10_grafico_dispersione.png`: Grafico bidimensionale.

*(I file `.csv` e i modelli salvati `.pkl` verranno generati automaticamente durante l'esecuzione degli script).*

## ⚙️ Requisiti di Sistema

Il progetto è stato sviluppato e testato utilizzando **Python 3.14.6**. 
Si consiglia l'utilizzo di un ambiente virtuale (Virtual Environment) per evitare conflitti con altre librerie di sistema.

Librerie principali impiegate:
- `pandas`, `numpy` (Manipolazione dati)
- `scikit-learn` (Machine Learning e preprocessing)
- `streamlit` (Framework interfaccia web)
- `plotly` (Visualizzazione dati interattiva)

## 🚀 Istruzioni per l'Installazione e l'Uso

Seguire i seguenti passaggi per eseguire il progetto in locale.

### Clonazione e Setup dell'Ambiente
Scaricare tutti i file del repository da GitHub (tramite il pulsante **Code -> Download ZIP** ed estraendo la cartella sul proprio computer, oppure clonando il repository con `git clone`).
Aprire il terminale ed entrare nella cartella del progetto appena scaricata:
```bash
cd nome_della_cartella
```
## Creare e attivare l'ambiente virtuale al suo interno:
**Su Windows:**
```bash
python -m venv env
```
```bash
.\env\Scripts\activate
```
**Su macOS:**
```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
**Installazione delle dipendenze con l'ambiente virtuale attivo, installare le librerie richieste eseguendo:**
```bash
pip install -r requirements.txt
```
Attendere qualche istante affinché il sistema scarichi e installi Pandas, NumPy, Scikit-Learn, Joblib, Streamlit e Plotly

**Generazione del Dataset**
```bash
python data_generator.py
```
Il terminale confermerà l'avvenuta creazione nella cartella del file clienti_startup.csv

**Addestramento modello(clustering)**
```bash
python ml_pipeline.py
```
Il terminale stamperà la tabella di confronto per k = 2..6 e il valore dell'Indice di Silhouette (es. 0.691). Nella cartella compariranno automaticamente quattro nuovi file: clienti_clusterizzati.csv (con i dati finali), valutazione_k.csv (metriche per i grafici di validazione), kmeans_model.pkl e scaler.pkl (i modelli salvati per l'inferenza).

**Avvio Dashboard**
```bash
streamlit run app.py
```
Il terminale avvierà un server locale e si aprirà automaticamente una scheda nel browser predefinito all'indirizzo http://localhost:8501 (oppure altra porta se occupata).

Per fermare il comando da terminale Ctrl(windows)/control(mac)+c sulla tastiera.

## 🔁 Riproducibilità
L'impostazione del Seed fisso (`42`) e data di riferimento fissa in `data_generator.py` (2026-10-01) garantisce che ogni esecuzione produce gli stessi dati e gli stessi cluster.





