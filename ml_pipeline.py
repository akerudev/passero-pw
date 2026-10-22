"""
=============================================================================
Autore: Alessandro Passero 
Università: Università Telematica Pegaso
Corso di Laurea: Informatica per le Aziende Digitali (L-31)
Progetto: Project Work (Traccia 28) - Intelligenza Artificiale e Machine Learning 
          per i processi aziendali.
Obiettivo: Progettare un sistema di segmentazione automatica della clientela 
           per un'azienda digitale di servizi.

File: ml_pipeline.py
Descrizione: Pipeline di Machine Learning: pulizia dei dati, standardizzazione,
             valutazione di k (metodo del gomito e indice di silhouette),
             clustering K-Means, salvataggio di risultati e modelli.
=============================================================================
"""

# Importazione delle librerie
import pandas as pd  # tabelle e file CSV
from sklearn.preprocessing import StandardScaler  # standardizzazione
from sklearn.cluster import KMeans  # algoritmo di clustering
from sklearn.metrics import silhouette_score  # indice di silhouette
import joblib  # salvataggio dei modelli (.pkl)

print("Avvio pipeline di Machine Learning...")

# 1. Caricamento dati
try:
    df = pd.read_csv('clienti_startup.csv')  # dataset creato da data_generator.py
except FileNotFoundError:
    print("Errore: Esegui prima data_generator.py per creare il dataset.")
    exit()

# 2. Pulizia di base: duplicati e valori mancanti
features = ['Giorni_Ultima_Richiesta', 'Numero_Richieste', 'Importo_Speso']  # le 3 variabili RFM usate nel clustering
righe_iniziali = len(df)
df = df.drop_duplicates(subset='ID_Cliente')  # un solo record per cliente
df[features] = df[features].apply(pd.to_numeric, errors='coerce')  # valori non numerici -> mancanti
df[features] = df[features].fillna(df[features].median())  # imputazione con la mediana
df = df.dropna(subset=['ID_Cliente', 'Zona', 'Categoria_Preferita']).reset_index(drop=True)
print(f"Pulizia dati: {righe_iniziali} righe in ingresso, {len(df)} dopo la pulizia.")

# Selezione feature per il clustering
X = df[features]

# 3. Standardizzazione: porta le variabili a media 0 e deviazione standard 1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # fit: media e dev. std; transform: le applica

# 4. Scelta di k: metodo del gomito (inertia) e silhouette per k = 2..6
risultati_k = []
for k in range(2, 7):  # k = 2, 3, 4, 5, 6
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    risultati_k.append({'k': k,
                        'inertia': round(km.inertia_, 2),  # per il metodo del gomito
                        'silhouette': round(silhouette_score(X_scaled, km.labels_), 3)})
df_k = pd.DataFrame(risultati_k)
df_k.to_csv('valutazione_k.csv', index=False)  # letto dalla dashboard per i grafici
print("Confronto configurazioni:")
print(df_k.to_string(index=False))

# 5. Applicazione K-Means con k scelto (3, coerente con i 3 profili latenti
#    e con l'intervallo 3-5 richiesto dalla traccia)
K_SCELTO = 3  # scelto con gomito e silhouette
kmeans = KMeans(n_clusters=K_SCELTO, random_state=42, n_init=10)  # n_init=10: 10 avvii, tiene il migliore
df['Cluster_ID'] = kmeans.fit_predict(X_scaled)  # calcola i centroidi e assegna 0, 1 o 2

# 6. Valutazione con Indice di Silhouette
sil_score = silhouette_score(X_scaled, df['Cluster_ID'])
print(f"Qualità del clustering (k={K_SCELTO}) (Indice di Silhouette): {sil_score:.3f} (Più vicino a 1 è meglio)")

# 7. Assegnazione nomi ai cluster in base alla spesa media
# I numeri 0, 1, 2 sono arbitrari: i cluster vengono ordinati per spesa media
cluster_means = df.groupby('Cluster_ID')['Importo_Speso'].mean().sort_values()
nomi_mappa = {
    cluster_means.index[0]: 'Occasionali/Basso Valore',
    cluster_means.index[1]: 'Fedeli/Medio Valore',
    cluster_means.index[2]: 'Campioni/Alto Valore'
}
df['Nome_Cluster'] = df['Cluster_ID'].map(nomi_mappa)

# 8. Salvataggio risultati e modelli
df.to_csv('clienti_clusterizzati.csv', index=False)  # risultati: un cliente per riga con il segmento
joblib.dump(scaler, 'scaler.pkl')  # riusato dalla dashboard per i nuovi clienti
joblib.dump(kmeans, 'kmeans_model.pkl')

print("Modello addestrato. Dati salvati in 'clienti_clusterizzati.csv'.")
print("Modello e Scaler esportati (.pkl) per la dashboard.")