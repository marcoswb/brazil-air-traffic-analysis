# Brazil Air Traffic Analysis

[![Python](https://img.shields.io/badge/python-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Airflow](https://img.shields.io/badge/airflow-2.9.0-017CEE.svg?logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![Grafana](https://img.shields.io/badge/grafana-10.4.2-F46800.svg?logo=grafana&logoColor=white)](https://grafana.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

ETL pipeline for Brazilian air traffic analysis using public flight data from [ANAC (SIROS)](https://siros.anac.gov.br). The project downloads and normalizes flight records, loads them into PostgreSQL, and supports interactive exploration through Grafana dashboards.

## Overview

Public ANAC datasets are useful for studying airline performance, airport activity, and schedule punctuality, but they arrive as separate CSV files that need cleaning and relational modeling before analysis. This project automates that process with Apache Airflow and exposes the results in Grafana.

The pipeline:

1. Downloads VRA (flight) CSVs for configured years, plus airport, aircraft, and airline reference files
2. Normalizes column names and flight fields into consistent CSV outputs
3. Creates an `etl` schema in PostgreSQL and loads aircraft, airline, airport, and flight tables
4. Supports visualization through exported Grafana dashboards

## Features

- Manual Airflow DAGs for download, normalize, and database load steps
- Extraction of ANAC VRA data plus reference CSVs (`aerodromos.csv`, `aeronaves.csv`, `cias.csv`)
- CSV normalization (column renaming, float formatting, timestamp parsing, flight field cleanup)
- Relational load into PostgreSQL (`aircraft`, `airline`, `airport`, `flights`) under the `etl` schema
- Docker Compose stack for PostgreSQL, pgAdmin, Airflow, and Grafana
- Exported Grafana dashboards for airport map, busiest airports, seat supply, daily/monthly flights, flight comparison, and punctuality
- Helper script to export Grafana dashboards and datasources via API

## Technologies

| Layer | Tool | Role |
|-------|------|------|
| Orchestration | Apache Airflow 2.9.0 (LocalExecutor) | Runs ETL DAGs |
| Database | PostgreSQL 15 | Stores transformed data and Airflow metadata |
| Visualization | Grafana 10.4.2 | Dashboards over PostgreSQL |
| Administration | pgAdmin 4 | Optional database UI |
| Infrastructure | Docker & Docker Compose | Local multi-service environment |
| Processing | Python, pandas, BeautifulSoup, requests, unidecode, SQLAlchemy | Download, transform, and load |

## Project structure

```
brazil-air-traffic-analysis/
├── airflow/
│   └── variables.json          # Airflow Variables used by the DAGs
├── dags/                       # Airflow DAGs and application code
│   ├── controllers/            # Download, normalize, and load logic
│   ├── models/                 # SQLAlchemy models
│   ├── utils/                  # File helpers
│   ├── download_data_anac.py
│   ├── normalize_data_anac.py
│   └── load_data_db.py
├── grafana/
│   ├── dashboards/             # Exported dashboard JSON files
│   └── datasources/            # Exported datasource JSON
├── data/                       # Runtime data directory (mounted into Airflow)
├── database/
│   └── backup.zip              # PostgreSQL dump of the etl schema (backup.sql)
├── export_configs_grafana.py   # Exports Grafana dashboards/datasources
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── LICENSE
```

## Prerequisites

- Docker and Docker Compose
- Git

Optional (only if running helper scripts outside Docker):

- Python
- Packages from `requirements.txt`

## Installation and setup

### 1. Clone the repository

```bash
git clone https://github.com/marcoswb/brazil-air-traffic-analysis.git
cd brazil-air-traffic-analysis
```

### 2. Start the stack

On Linux/macOS, set an Airflow UID if needed:

```bash
export AIRFLOW_UID=$(id -u)
```

Then start services:

```bash
docker compose up -d
```

The first run initializes the Airflow database and creates the default Airflow admin user.

### 3. Import Airflow Variables

DAG configuration is read from **Airflow Variables**. Import the sample file after the stack is running:

```bash
docker compose cp airflow/variables.json airflow-webserver:/tmp/variables.json
docker compose exec airflow-webserver airflow variables import /tmp/variables.json
```

You can also import them in the Airflow UI under **Admin → Variables**.

| Variable | Sample value | Purpose |
|----------|--------------|---------|
| `ANAC_RESOURCE` | `https://siros.anac.gov.br` | ANAC base URL |
| `BASE_PATH` | `/opt/airflow/data/anac` | Working directory inside the Airflow container |
| `YEARS_TO_DOWNLOAD` | `2025` | Year(s) to download (comma-separated if multiple) |
| `HOST_DB` | `db` | PostgreSQL host (Compose service name) |
| `PORT_DB` | `5432` | PostgreSQL port |
| `DATABASE_DB` | `airflow` | PostgreSQL database name |
| `USERNAME_DB` | `airflow` | PostgreSQL user |
| `PASSWORD_DB` | `airflow` | PostgreSQL password |

### 4. Optional local Python dependencies

```bash
pip install -r requirements.txt
```

## Environment variables and configuration

### Docker Compose defaults

These values are defined in `docker-compose.yml`:

| Service | URL / Port | Default credentials |
|---------|------------|---------------------|
| Airflow UI | http://localhost:8080 | `admin` / `admin` |
| Grafana | http://localhost:3000 | `admin` / `admin` |
| pgAdmin | http://localhost:5050 | `admin@admin.com` / `admin` |
| PostgreSQL | `localhost:5432` | `airflow` / `airflow` (database `airflow`) |

Related Compose settings:

- `AIRFLOW_UID` — host user mapped into Airflow containers (defaults to `50000`)
- Airflow DAGs start **paused**
- Airflow example DAGs are disabled
- Transformed ETL tables are created in the PostgreSQL schema `etl`

### Grafana export script (`.env`)

`export_configs_grafana.py` reads:

```env
API_GRAFANA=<Grafana API token>
```

Create a `.env` file in the project root with that key when using the export script. The script targets `http://localhost:3000`.

## How to run

### Option A — Run the ETL pipeline

1. Start the stack and import Airflow Variables (see [Installation and setup](#installation-and-setup)).
2. Open Airflow at http://localhost:8080.
3. Unpause and run the DAGs **in order**:
   1. `download_data_anac` — downloads ANAC CSVs into `BASE_PATH/downloaded`
   2. `normalize_data_anac` — writes normalized files to `BASE_PATH/normalized`
   3. `create_db_and_load_data` — recreates the `etl` schema/tables and loads data

All three DAGs use `schedule=None` (manual trigger only).

### Option B — Restore the database backup

To skip the full ETL download/load and use the included dump of the `etl` schema:

```bash
# Extract the SQL dump
unzip database/backup.zip -d database

# Restore into the Compose PostgreSQL service
docker compose exec -T db psql -U airflow -d airflow < database/backup.sql
```

On Windows PowerShell, you can extract with `Expand-Archive database\backup.zip -DestinationPath database` and restore with:

```powershell
Get-Content database\backup.sql | docker compose exec -T db psql -U airflow -d airflow
```

### Configure Grafana (one-time)

Do this once after the first setup:

1. Open Grafana at http://localhost:3000.
2. Create a PostgreSQL datasource using the Compose database (see `grafana/datasources/grafana-postgresql-datasource.json` for a reference: host `db:5432`, database `airflow`, user `airflow`, password `airflow`).
3. Import the dashboard JSON files from `grafana/dashboards/`.

After that, Grafana keeps the datasource and dashboards in its volume (`grafana_data`), so you do not need to import them again on later starts.

### Example: download a different year

Set Airflow Variable `YEARS_TO_DOWNLOAD` to a comma-separated list, for example:

```text
2023,2024,2025
```

Then run `download_data_anac`, followed by normalize and load.

### Export Grafana configuration

With Grafana running and `API_GRAFANA` set in `.env`:

```bash
pip install python-dotenv requests
python export_configs_grafana.py
```

This writes dashboard and datasource JSON files under `./grafana`.

## Grafana dashboards included

Exported dashboards in `grafana/dashboards/`:

- Mapa Aeroportos
- Aeroportos mais movimentados
- Oferta de assentos
- Voôs por mês
- voos por dia
- Comparação Total voôs
- Pontualidade voôs

## Screenshots

### Airflow DAGs

<img width="1884" height="551" alt="Airflow DAGs" src="https://github.com/user-attachments/assets/c0da1333-8dd9-40e2-a8d2-a65af1fba5b9" />

### Airport map

<img width="1579" height="796" alt="Airport map dashboard" src="https://github.com/user-attachments/assets/9dbb2a0d-b911-4c3a-9441-8d5176a01e70" />

### Punctuality and flight volume

<img width="1589" height="833" alt="Punctuality dashboard" src="https://github.com/user-attachments/assets/b803b8d2-ade0-4a4d-8d4b-d3e2a907472e" />

<img width="1589" height="842" alt="Flight volume dashboard" src="https://github.com/user-attachments/assets/eba651ff-1df9-4ca4-8ea2-073c3ef3fc78" />

<img width="1579" height="794" alt="Airline comparison dashboard" src="https://github.com/user-attachments/assets/cf587926-0e21-4d24-aa89-af1e3c2f0c6c" />

## License

This project is licensed under the [MIT License](LICENSE).
