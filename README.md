# Brazil Air Traffic Analysis 🛫🇧🇷  

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)  
[![Docker](https://img.shields.io/badge/docker-enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)  
[![Airflow](https://img.shields.io/badge/airflow-2.x-017CEE.svg?logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)  
[![Grafana](https://img.shields.io/badge/grafana-dashboard-F46800.svg?logo=grafana&logoColor=white)](https://grafana.com/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  

Pipeline **ETL** para análise de tráfego aéreo no Brasil, utilizando dados públicos da **[ANAC](https://siros.anac.gov.br)**. Permite explorar métricas de desempenho das companhias aéreas, analisar rotas e visualizar conexões entre aeroportos em dashboards interativos.  

---

## 🔍 Visão Geral  

O projeto constrói um **pipeline de análise de tráfego aéreo brasileiro** que:  
- Extrai dados da ANAC  
- Transforma e padroniza informações  
- Carrega em um banco de dados relacional  
- Disponibiliza os dados em **dashboards do Grafana**  
- Está preparado para integração futura com dados **meteorológicos**  

---

## ✅ Funcionalidades  

- 📥 **Extração** de dados públicos de voos  
- 🧹 **Transformação** e limpeza dos datasets  
- 💾 **Carga** em banco de dados relacional  
- 📊 Métricas por companhia aérea, rota e período  
- 🗺 **Mapa de rotas aéreas** (geomap Grafana)  
- 🐳 Ambiente **containerizado** com Docker  
- ⏰ Agendamento de tarefas com **Apache Airflow**  

---

## 🏗 Arquitetura & Tecnologias  

| Camada | Ferramenta | Papel |
|--------|------------|-------|
| Orquestração | **Apache Airflow** | DAGs para ETL |
| Banco de Dados | **PostgreSQL** | Armazenamento dos dados transformados |
| Visualização | **Grafana** | Dashboards e mapas de rotas |
| Infraestrutura | **Docker & Docker Compose** | Provisionamento e portabilidade |
| Scripts | **Python** | Extração, transformação e integração |

---

## 🛠 Como usar / Setup  

### 1. Clone o repositório  
```bash
git clone https://github.com/marcoswb/brazil-air-traffic-analysis.git
cd brazil-air-traffic-analysis
```

### 2. Configure variáveis de ambiente  
Crie um arquivo `.env` na raiz do projeto com as credenciais do banco e demais configs:  
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=air_traffic
DB_USER=usuario
DB_PASS=senha
```

### 3. Instale dependências (opcional, fora do Docker)  
```bash
pip install -r requirements.txt
```

### 4. Suba os containers  
```bash
docker-compose up -d
```

### 5. Acesse os serviços  
- Airflow UI → [http://localhost:8080](http://localhost:8080)  
- Grafana → [http://localhost:3000](http://localhost:3000)  

### 6. Rode o pipeline  
Ative as DAGs no Airflow e acompanhe a execução no painel.  

---

## 📂 Estrutura de Pastas  

```
brazil-air-traffic-analysis/
│
├── airflow/                   # Configurações do Airflow (DAGs, plugins)
│   └── dags/
├── database/                  # Scripts de schema e dados
├── grafana/                   # Dashboards e configurações
├── export_configs_grafana.py  # Script auxiliar (exportação/importação Grafana)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── escopo.md
└── LICENSE
```

---

## 📊 Exemplos / Resultados  

### Dashboard Grafana - Mapa aeroportos 
> Pontos em um GeoMap localizando todos os aeroportos que tiveram algum vôo.

### Métricas  
- Média de atrasos por companhia  
- Volume de voos por rota  
- Evolução mensal de passageiros  

(*adicione prints dos dashboards aqui*)  


---

## 📝 Licença  

Este projeto está licenciado sob a [MIT License](LICENSE).  

---

✈️ **Brazil Air Traffic Analysis** — dados que decolam para virar insights! 🚀  
