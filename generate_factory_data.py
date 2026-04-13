import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Data Science Überlegung ---
# Ziel: Ein Datensatz, der Verschleiß und Korrelation zwischen Sensorwerten (Vibration) 
# und Maschinenausfällen zeigt. Das ist die perfekte Basis für ein Portfolio-Projekt.
np.random.seed(42)

n_machines = 10
days = 365
hours_per_day = 24

# Zeitstempel generieren
start_date = datetime(2025, 1, 1)
timestamps = [start_date + timedelta(hours=i) for i in range(days * hours_per_day)]

data_list = []

print("Generiere Daten... Bitte warten.")

for m_id in range(1, n_machines + 1):
    # Basis-Vibration für jede Maschine individuell festlegen
    base_vibration = np.random.uniform(10, 18)
    
    for ts in timestamps:
        # Tag des Jahres berechnen (1 bis 365) für die Verschleiß-Simulation
        day_of_year = ts.timetuple().tm_yday
        
        # 1. Vibration simulieren: Basis + Rauschen + leichter Anstieg über das Jahr (Verschleiß)
        vibration = base_vibration + np.random.normal(0, 1.5) + (day_of_year / 40)
        
        # 2. Logik für Maschinenausfälle:
        # Wenn Vibration > 25, steigt das Ausfallrisiko exponentiell
        failure_threshold = 25
        if vibration > failure_threshold:
            # Risiko ist hoch (30% Chance auf Stillstand pro Stunde bei hoher Vibration)
            failure_prob = 0.3
        else:
            # Normales Risiko (0.5% Chance auf zufälligen Stillstand)
            failure_prob = 0.005
            
        status = "Produktion"
        if np.random.random() < failure_prob:
            status = "Stillstand"
            
        # 3. Produktion und Ausschuss
        # Nur im Status "Produktion" werden Teile gefertigt
        pieces = np.random.randint(90, 110) if status == "Produktion" else 0
        
        # Die Ausschussquote steigt ebenfalls mit der Vibration (Qualitätsverlust durch Vibration)
        scrap_rate = 0.01 + (vibration / 800) 
        scrap = int(pieces * scrap_rate) if pieces > 0 else 0
        
        data_list.append({
            "Zeitstempel": ts,
            "Maschinen_ID": f"Maschine_{m_id:02d}",
            "Vibration_mm_s": round(vibration, 2),
            "Status": status,
            "Produzierte_Stueck": pieces,
            "Fehlteile": scrap,
            "Temperatur_C": round(np.random.normal(65, 4) + (vibration/5), 1)
        })

# DataFrame erstellen
df = pd.DataFrame(data_list)

# 4. Data Quality "Injections" für den DS-Beweis
# Wir löschen zufällig 100 Temperaturwerte, um Cleaning-Skills in Power BI zu zeigen
nan_indices = np.random.choice(df.index, size=100, replace=False)
df.loc[nan_indices, "Temperatur_C"] = np.nan

# Speichern als CSV für Power BI
df.to_csv("production_big_data.csv", index=False, sep=";")

print(f"Fertig! {len(df)} Zeilen wurden in 'production_big_data.csv' gespeichert.")