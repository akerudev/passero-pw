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


