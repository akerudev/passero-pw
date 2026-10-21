"""
=============================================================================
Autore: Alessandro Passero 
Università: Università Telematica Pegaso
Corso di Laurea: Informatica per le Aziende Digitali (L-31)
Progetto: Project Work (Traccia 28) - Intelligenza Artificiale e Machine Learning 
          per i processi aziendali.
Obiettivo: Progettare un sistema di segmentazione automatica della clientela 
           per un'azienda digitale di servizi.
Data inizio sviluppo: 01/10/2026
File: data_generator.py
Descrizione: Generatore di dataset sintetico per una startup B2B di servizi.
             Lo script crea 300 record realistici basati sul modello RFM,
             utilizzando distribuzioni gaussiane (NumPy) per simulare
             il comportamento di 3 profili latenti, e salva i dati grezzi
             in un file CSV (clienti_startup.csv) formattato con Pandas.
=============================================================================
"""

# Importazione delle librerie 
import pandas as pd  # analisi dei dati, tabelle (DataFrame) ed esportazione CSV
import numpy as np  # libreria matematica, estrazioni casuali e distribuzioni statistiche
from datetime import datetime, timedelta  # gestione delle date

# Impostiamo la riproducibilità (stessi risultati a ogni avvio)
np.random.seed(42)

NUM_RECORDS = 300  # numero di clienti (traccia: 300-600)
zone = ['Nord', 'Centro', 'Sud', 'Isole']  # valori descrittivi: estratti a caso, esclusi dal clustering
categorie = ['Consulenza Base', 'Intervento Tecnico', 'Contenuti Premium', 'Assistenza H24']

dati_clienti = []  # lista di dizionari: un elemento per cliente
# Data di riferimento fissa: rende il dataset identico a ogni esecuzione
data_odierna = datetime(2026, 10, 1)

print("Generazione dati clienti in corso...")
# creazione di 3 profili per garantire realismo nei dati
for client_id in range(1, NUM_RECORDS + 1):  # 300 ripetizioni, client_id da 1 a 300
    # Profilo latente con probabilità 50/30/20 (non salvato nel CSV)
    profile_type = np.random.choice(['Occasionale', 'Fedele', 'Altospendente'], p=[0.5, 0.3, 0.2])
    
    if profile_type == 'Occasionale':  # max() evita valori nulli o negativi, int() rende interi (per tutti i profili)
        recency = max(1, int(np.random.normal(loc=120, scale=30)))  # lontani nel tempo
        frequency = max(1, int(np.random.normal(loc=3, scale=1)))  # poche richieste
        monetary = max(10, np.random.normal(loc=50, scale=15))  # bassa spesa
    elif profile_type == 'Fedele':
        recency = max(1, int(np.random.normal(loc=20, scale=10)))  # molto recenti 
        frequency = max(1, int(np.random.normal(loc=15, scale=4)))  # molte richieste
        monetary = max(10, np.random.normal(loc=150, scale=40))  # spesa media
    else:  # Altospendente
        recency = max(1, int(np.random.normal(loc=60, scale=20)))  # abbastanza recenti
        frequency = max(1, int(np.random.normal(loc=8, scale=2)))  # richieste medie
        monetary = max(50, np.random.normal(loc=500, scale=100))  # spesa molto alta
        
    zona = np.random.choice(zone)  # estrazione uniforme
    categoria = np.random.choice(categorie)
    
    # Calcolo data di iscrizione fittizia
    giorni_iscrizione = recency + np.random.randint(10, 365)  # iscrizione da 10 a 364 giorni prima dell'ultima richiesta
    data_iscrizione = data_odierna - timedelta(days=giorni_iscrizione)
    
    dati_clienti.append({
        'ID_Cliente': f"C{client_id:04d}",  # C0001, C0002, ...
        'Zona': zona,
        'Data_Iscrizione': data_iscrizione.strftime('%Y-%m-%d'),
        'Giorni_Ultima_Richiesta': recency,
        'Numero_Richieste': frequency,
        'Importo_Speso': round(monetary, 2),
        'Categoria_Preferita': categoria
    })

# Creazione del DataFrame e salvataggio in CSV
df = pd.DataFrame(dati_clienti)
df.to_csv('clienti_startup.csv', index=False)  # index=False: nessuna colonna con il numero di riga
print("File 'clienti_startup.csv' generato con successo!")
