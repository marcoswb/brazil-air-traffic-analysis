# 📊 Projeto – Análise de Fluxo Aéreo no Brasil

## 🎯 Objetivo
Criar um pipeline **ETL** que consolide e analise os voos nacionais no Brasil usando dados públicos da **ANAC**, permitindo:
- Identificar as rotas mais movimentadas.
- Analisar a movimentação por aeroporto, companhia aérea e tipo de aeronave.
- Criar visualizações geográficas das conexões aéreas.
- Futuramente integrar com dados meteorológicos do **INMET** para investigar impactos climáticos.

---

## 📂 Fontes de Dados
- **ANAC – Voos Domésticos e Aeronaves**
  - **Movimento de Aeronaves**: data, aeroporto de origem/destino, companhia aérea, tipo de voo.
  - **Cadastro de Aeródromos**: nome, código ICAO/IATA, município, estado, latitude/longitude.
  - **Cadastro de Aeronaves**: fabricante, modelo, capacidade, ano de fabricação.
  - **Cadastro de Operadores** (companhias aéreas).
- **[Futuro] INMET – Dados Meteorológicos Históricos**:
  - Temperatura, chuva, vento e condições do tempo por estação meteorológica.

---

## 🏛 Arquitetura de Dados
O projeto seguirá o modelo de camadas **Raw → Staging → Analytics**:

1. **Raw (Bruta)** – dados extraídos sem alterações (formato original CSV/Excel).
2. **Staging (Tratada)** – padronização de nomes, tipos de dados e chaves.
3. **Analytics (Curada)** – tabelas otimizadas para consulta e análise.

---

## 🗄 Modelo de Dados

**Tabelas Dimensão:**
- `dim_aeroporto` (id, nome, iata, icao, cidade, estado, lat, lon)
- `dim_companhia` (id, nome, cnpj, país)
- `dim_aeronave` (id, fabricante, modelo, capacidade, ano_fabricacao)
- `dim_tempo` (id_data, data, ano, mes, dia, dia_semana, feriado)

**Tabela Fato:**
- `fato_voo`  
  (`id_voo`, `id_aeroporto_origem`, `id_aeroporto_destino`, `id_companhia`,  
   `id_aeronave`, `id_data_partida`, `id_data_chegada`,  
   `quantidade_voos`, `assentos_ofertados`, `passageiros`, `carga_kg`)

---

## 🔄 Transformações Principais
- Padronização de códigos IATA/ICAO para aeroportos e companhias.
- Normalização de datas e criação de dimensão de tempo.
- Enriquecimento geográfico dos aeroportos (latitude/longitude).
- Agregações:
  - Quantidade de voos por rota (origem → destino).
  - Voos por companhia aérea.
  - Voos por tipo de aeronave.
  - Top 10 rotas mais movimentadas.
- **[Futuro]** Cruzamento de voos com condições meteorológicas.

---

## 🔍 Queries de Exemplo

**Top 10 rotas mais movimentadas:**
```sql
SELECT origem.nome AS aeroporto_origem,
       destino.nome AS aeroporto_destino,
       SUM(f.quantidade_voos) AS total_voos
FROM fato_voo f
JOIN dim_aeroporto origem ON f.id_aeroporto_origem = origem.id
JOIN dim_aeroporto destino ON f.id_aeroporto_destino = destino.id
GROUP BY origem.nome, destino.nome
ORDER BY total_voos DESC
LIMIT 10;
