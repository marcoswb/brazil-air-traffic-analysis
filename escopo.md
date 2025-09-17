# 📊 Projeto – Análise de Fluxo Aéreo no Brasil

## 📂 Fontes de Dados
- **[Futuro] INMET – Dados Meteorológicos Históricos**:
  - Temperatura, chuva, vento e condições do tempo por estação meteorológica.


## 🔄 Transformações Principais
- **[Futuro]** Cruzamento de voos com condições meteorológicas.



## 📊 Ideias de Dashboards no Grafana (ANAC + Postgres)


#### 1. Volume de voos por período

Objetivo: analisar tendências sazonais ao longo do tempo.

Visualização sugerida: gráfico de linhas ou barras.

Query SQL:

```
SELECT DATE_TRUNC('month', scheduled_departure) AS mes,
       COUNT(*) AS total_voos
FROM flights
GROUP BY mes
ORDER BY mes;
```

#### 2. Aeroportos mais movimentados

Objetivo: identificar os aeroportos com maior fluxo de voos.

Visualização sugerida: gráfico de barras horizontal (Top 10).

Query SQL:

```
SELECT a.name AS aeroporto, COUNT(f.id) AS total
FROM flights f
JOIN airport a ON f.departure_airport_id = a.id
GROUP BY a.name
ORDER BY total DESC
LIMIT 10;
```

#### 3. Pontualidade dos voos

Objetivo: medir atraso médio de decolagem por companhia aérea.

Visualização sugerida: gráfico de barras ou gauge.

Query SQL:

```
SELECT al.name AS companhia,
       AVG(EXTRACT(EPOCH FROM (actual_departure - scheduled_departure))/60) AS atraso_medio_min
FROM flights f
JOIN airline al ON f.airline_id = al.id
WHERE actual_departure IS NOT NULL
GROUP BY al.name
ORDER BY atraso_medio_min DESC;
```

#### 4. Capacidade de assentos por companhia

Objetivo: comparar a oferta de assentos no mercado aéreo.

Visualização sugerida: gráfico de barras ou gauge.

Query SQL:

```
SELECT al.name AS companhia,
       SUM(seat_capacity) AS total_assentos
FROM flights f
JOIN airline al ON f.airline_id = al.id
GROUP BY al.name
ORDER BY total_assentos DESC;
```

#### 5. Mapa de rotas aéreas

Objetivo: visualizar conexões entre aeroportos.

Visualização sugerida: Geomap (linhas entre pontos).

Query SQL:

```
SELECT da.latitude AS dep_lat, da.longitude AS dep_lon,
       aa.latitude AS arr_lat, aa.longitude AS arr_lon
FROM flights f
JOIN airport da ON f.departure_airport_id = da.id
JOIN airport aa ON f.arrival_airport_id = aa.id
LIMIT 1000;
```

#### 6. Distribuição de voos por companhia aérea

Objetivo: mostrar participação de mercado das companhias.

Visualização sugerida: gráfico de pizza.

Query SQL:

```
SELECT al.name AS companhia, COUNT(*) AS total_voos
FROM flights f
JOIN airline al ON f.airline_id = al.id
GROUP BY al.name
ORDER BY total_voos DESC;
```