import csv
import random
from datetime import datetime, timedelta

random.seed(42)

MACHINES = ["M-001", "M-002", "M-003", "M-004", "M-005"]

MACHINE_PROFILES = {
    "M-001": {"base_temp": 215, "cycle_output": 42, "defect_rate": 0.018, "reliability": 0.92},
    "M-002": {"base_temp": 230, "cycle_output": 55, "defect_rate": 0.025, "reliability": 0.85},
    "M-003": {"base_temp": 205, "cycle_output": 38, "defect_rate": 0.012, "reliability": 0.95},
    "M-004": {"base_temp": 245, "cycle_output": 60, "defect_rate": 0.035, "reliability": 0.78},
    "M-005": {"base_temp": 220, "cycle_output": 48, "defect_rate": 0.020, "reliability": 0.90},
}

STATES = ["Produktion", "Stillstand", "Wartung"]

end_date = datetime(2026, 4, 13, 0, 0, 0)
start_date = end_date - timedelta(days=30)

rows = []

for machine_id in MACHINES:
    profile = MACHINE_PROFILES[machine_id]
    current = start_date

    current_status = "Produktion"
    status_remaining = random.randint(4, 12)

    while current < end_date:
        hour = current.hour
        weekday = current.weekday()

        if status_remaining <= 0:
            roll = random.random()
            if current_status == "Produktion":
                if roll < (1 - profile["reliability"]) * 0.6:
                    current_status = "Stillstand"
                    status_remaining = random.randint(1, 4)
                elif roll < (1 - profile["reliability"]):
                    current_status = "Wartung"
                    status_remaining = random.randint(3, 8)
                else:
                    status_remaining = random.randint(6, 24)
            else:
                current_status = "Produktion"
                status_remaining = random.randint(8, 30)

        if weekday == 6 and random.random() < 0.4:
            if current_status == "Produktion":
                current_status = "Stillstand"
                status_remaining = max(status_remaining, 4)

        if current_status == "Produktion":
            temp_drift = random.gauss(0, 2.5)
            hour_effect = 3 * (1 if 10 <= hour <= 16 else 0)
            temperatur = round(profile["base_temp"] + temp_drift + hour_effect, 1)

            stueckzahl = max(0, int(random.gauss(profile["cycle_output"], profile["cycle_output"] * 0.08)))
            fehlteile = 0
            for _ in range(stueckzahl):
                if random.random() < profile["defect_rate"]:
                    fehlteile += 1

        elif current_status == "Stillstand":
            temperatur = round(profile["base_temp"] - random.uniform(80, 140) + random.gauss(0, 3), 1)
            stueckzahl = 0
            fehlteile = 0

        else:
            temperatur = round(random.uniform(25, 60) + random.gauss(0, 2), 1)
            stueckzahl = 0
            fehlteile = 0

        rows.append([
            current.strftime("%Y-%m-%d %H:%M:%S"),
            machine_id,
            current_status,
            temperatur,
            stueckzahl,
            fehlteile,
        ])

        current += timedelta(hours=1)
        status_remaining -= 1

rows.sort(key=lambda r: (r[0], r[1]))

output_path = r"C:\Users\Lenox\Documents\demo_claude_code\demo_cc\Produktions-Dashboard\maschinen_daten.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Zeitstempel", "Maschinen_ID", "Status", "Temperatur", "produzierte_Stueckzahl", "Fehlteile"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows to {output_path}")
