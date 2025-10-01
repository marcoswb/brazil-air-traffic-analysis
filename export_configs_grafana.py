import os
import requests
import json
import dotenv

dotenv.load_dotenv()

GRAFANA_URL = "http://localhost:3000"
API_KEY = os.getenv('API_GRAFANA')
EXPORT_DIR = "./grafana"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def export_dashboards():
    dashboards_dir = os.path.join(EXPORT_DIR, "dashboards")
    os.makedirs(dashboards_dir, exist_ok=True)

    r = requests.get(f"{GRAFANA_URL}/api/search?query=&", headers=headers)
    r.raise_for_status()
    dashboards = r.json()

    print(f"📊 Encontrados {len(dashboards)} dashboards.")

    for d in dashboards:
        uid = d["uid"]
        title = d["title"].replace(" ", "_").replace("/", "_")

        r = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{uid}", headers=headers)
        r.raise_for_status()
        dashboard_json = r.json()

        filepath = os.path.join(dashboards_dir, f"{title}_{uid}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(dashboard_json, f, indent=2, ensure_ascii=False)

        print(f"✅ Dashboard exportado: {filepath}")


def export_datasources():
    datasources_dir = os.path.join(EXPORT_DIR, "datasources")
    os.makedirs(datasources_dir, exist_ok=True)

    r = requests.get(f"{GRAFANA_URL}/api/datasources", headers=headers)
    r.raise_for_status()
    datasources = r.json()

    print(f"🔌 Encontradas {len(datasources)} datasources.")

    for ds in datasources:
        name = ds["name"].replace(" ", "_")
        filepath = os.path.join(datasources_dir, f"{name}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(ds, f, indent=2, ensure_ascii=False)

        print(f"✅ Datasource exportada: {filepath}")


if __name__ == "__main__":
    os.makedirs(EXPORT_DIR, exist_ok=True)
    export_dashboards()
    export_datasources()
    print("\n📂 Exportação concluída! Tudo salvo em:", os.path.abspath(EXPORT_DIR))
