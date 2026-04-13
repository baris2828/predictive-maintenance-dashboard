# Predictive Maintenance Dashboard

End-to-end analytics case study for a simulated German injection-molding factory. Python generates 87,600 hourly sensor records; Power BI turns them into a Predictive Maintenance Dashboard that identifies the physical driver of unplanned downtime.

---

## Project Overview

This project simulates **one full year of operations (365 days × 24 hours × 10 machines = 87,600 data points)** for a fictional German plastics manufacturer. The synthetic dataset is engineered to contain a realistic, non-trivial correlation between a leading indicator (machine vibration) and a lagging outcome (machine downtime and scrap), so that BI tooling and its built-in AI features have a meaningful signal to uncover.

The deliverable is a Power BI `.pbip` project that visualizes throughput, scrap rate, status distribution, and — most importantly — surfaces the **root cause of unplanned stoppages** via Power BI's Key Influencers visual.

## Business Context

A typical mid-sized German `Kunststoffwerk` operates on a **reactive maintenance** model: machines run until they break, and maintenance is triggered by failure. Consequences:

- Unplanned downtime crushes OEE (Overall Equipment Effectiveness).
- Scrap rates rise silently as worn components produce out-of-spec parts.
- Maintenance crews are dispatched without knowing *why* the machine failed.

The goal of this dashboard is to support the transition from **reactive** to **predictive maintenance**: instead of reacting to failures, the shop-floor team watches a leading sensor metric and intervenes *before* the machine enters a failure regime.

## Key Insight — The "Aha!" Moment

Power BI's **Key Influencers** visual (shown in German in the screenshots — `Wichtigste Einflussfaktoren`) performs a logistic-regression-style analysis on the feature set and ranks which variable most increases the probability of `Status = Stillstand` (downtime).

**Finding:** When `Vibration_mm_s` exceeds **25 mm/s**, the likelihood of a machine entering downtime increases dramatically — by roughly **60× versus the nominal operating range** (~0.5% hourly failure probability below threshold vs. ~30% above it). Vibration is the single strongest driver; temperature and machine ID are secondary.

**Operational takeaway:** A vibration reading of **25 mm/s is the actionable early-warning threshold**. Any machine crossing it should be flagged for inspection within the current shift — not at the next scheduled maintenance window. This single threshold converts a reactive workflow into a predictive one without requiring a dedicated ML model.

## Tech Stack

| Layer | Tooling |
| --- | --- |
| Data simulation | **Python 3.10+**, `pandas`, `numpy` |
| Storage | CSV (semicolon-delimited, UTF-8) |
| BI / Modeling | **Power BI Desktop** — `.pbip` project format (source-control friendly) |
| Measures | **DAX** (KPIs: scrap rate, downtime %, OEE proxy) |
| AI / Analytics | Power BI **Key Influencers** visual |

## Repository Structure

```
Produktions-Dashboard/
├── generate_factory_data.py          # 87,600-row simulation (10 machines × 1 year)
├── generate_data.py                  # Smaller 5-machine / 30-day demo dataset
├── maschinen_daten.csv               # Demo dataset (checked in)
├── production_big_data.csv           # Full dataset (gitignored — regenerate locally)
├── Produktions_Monitoring.pbip       # Power BI project entry point
├── Produktions_Monitoring.Report/    # Report layout (JSON, version-controllable)
├── Produktions_Monitoring.SemanticModel/  # Data model + DAX measures
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Setup Instructions

### 1. Clone and install

```bash
git clone https://github.com/<your-user>/predictive-maintenance-dashboard.git
cd predictive-maintenance-dashboard
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate the dataset

```bash
python generate_factory_data.py
```

This produces `production_big_data.csv` (~5 MB, 87,600 rows). The file is intentionally gitignored — each contributor regenerates it locally.

### 3. Open the Power BI project

1. Open **Power BI Desktop** (version 2.124+ for `.pbip` support).
2. File → Open → select `Produktions_Monitoring.pbip`.
3. In the ribbon: **Home → Refresh** to re-read `production_big_data.csv`.
4. Save. The `.Report` and `.SemanticModel` folders will be updated as plain text — commit them to version control.

### 4. Reproduce the Key Influencers view

On the report page, the **Key Influencers** visual is pre-bound to:

- **Analyze:** `Status`
- **Explain by:** `Vibration_mm_s`, `Temperatur_C`, `Maschinen_ID`

Filter `Status` to `Stillstand` to see what drives downtime.

## Data Dictionary

| Column | Type | Description |
| --- | --- | --- |
| `Zeitstempel` | datetime | Hourly reading (2025-01-01 00:00 → 2025-12-31 23:00) |
| `Maschinen_ID` | string | `Maschine_01` … `Maschine_10` |
| `Vibration_mm_s` | float | Sensor vibration, drifts upward over the year (wear simulation) |
| `Status` | string | `Produktion` or `Stillstand` |
| `Produzierte_Stueck` | int | Parts produced in the hour (0 during downtime) |
| `Fehlteile` | int | Scrap count; scrap rate grows with vibration |
| `Temperatur_C` | float | Operating temperature; 100 values intentionally `NaN` to exercise Power Query cleaning |

## License

MIT — see `LICENSE`.
