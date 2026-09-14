# DS-Project

## Climate in Europe

### Project Overview

This Data Science project investigates long-term changes in heatwaves and UV
radiation across Germany and Europe: how heatwave frequency, intensity and
duration have changed since 1980, and how UV exposure has developed since
2000, including its possible public-health relevance.

### Research Questions

**Heatwaves**
1. How have frequency, intensity (peak/average temperature) and duration of
   heatwaves in major German cities (≥150,000 inhabitants) changed between
   1980 and today?
2. How do these heatwave metrics differ across city sizes, from large
   cities to rural municipalities, within the same region in Germany?
3. How have these heatwave metrics changed across major European cities
   (≥500,000 inhabitants) between 1980 and today?
4. In the European country most strongly affected by rising heatwave
   trends, does this effect concentrate in large cities, or is it equally
   present in smaller cities and rural municipalities?

**UV exposure and health**

5. How has the UV Index across Europe changed since 2000, and are there
   significant temporal and regional trends?
6. What are the public-health implications of UV Index trends in highly
   affected European regions, particularly regarding sunburn risk?

### Data

| Source | Used for | Coverage |
|---|---|---|
| [Open-Meteo Archive API](https://open-meteo.com/) (ERA5) | Daily max. temperature per city | 1961–2025 |
| [Wikidata SPARQL API](https://query.wikidata.org/) | German city selection & metadata | ≥150,000 inhabitants |
| [GeoNames API](https://www.geonames.org/) | European city selection & metadata | ≥500,000 inhabitants + capitals |
| [TEMIS API](https://www.temis.nl/) | UV Index across Europe | 2000–2025 |
| [Destatis GENESIS-Online](https://www-genesis.destatis.de/) | German hospital cases: sunburn (ICD-10 L55), heat/light effects (T67) | 2000–2024 |

**Heatwave definition (DWD):** ≥3 consecutive days with daily max.
temperature above *both* the city-specific 98th-percentile threshold
(1961–1990 reference period) *and* 28 °C.

**City-size classes** (RQ2/RQ4): large city ≥150,000, medium 20,000–149,999,
small town 5,000–19,999, rural municipality 1,000–4,999 (≥15 km from a
large-city centre).

### Data Pipeline

Each research question has its own Jupyter notebook, grouped in folders
named after the RQ(s) it covers. Every notebook follows the same steps:
collect the city list (Wikidata/GeoNames) → fetch daily temperatures from
Open-Meteo through a persistent local cache → detect heatwaves per the DWD
definition → aggregate to yearly trends and run linear regressions
(cross-checked on a 1991–2025 window to rule out reference-period overlap)
→ export the processed results as CSV/Parquet.

### Website: Build & Deployment

`Website/` is a multi-page [Streamlit](https://streamlit.io/) app:
`app.py` builds the navigation (`st.navigation`/`st.Page`), one module per
RQ lives in `views/` (`rq1.py`–`rq6.py`), and shared metadata/styling sit in
`content.py`/`theme.py`. Pages don't call any API or database live: they
read the CSV exports copied into `Website/data/` and render interactive
Plotly charts from them. Hosted on Streamlit Community Cloud, built
directly from this repository.

### Usage & Highlights

Use the sidebar to switch between **Heatwaves** (RQ1–RQ4) and **UV**
(RQ5–RQ6). Each RQ page explains the method, then lets you filter by year
range, city/country and metric, with charts updating live.

- Heatwaves are **significantly more frequent and longer** since 1980
  (Germany: +1.8/year, 57 cities; Europe: +4.0/year, 99 cities), but **not
  measurably hotter**.
- **Italy** is the most strongly affected country, and the effect holds
  across all city sizes.
- Europe's **UV Index has stayed flat** since 2000, while German
  sunburn/heat-related hospital cases have **declined substantially**.

Try it yourself: **https://climate-change-europe.streamlit.app/**

### Marking of LLM-Assisted Code

Data collection, definitions and statistical analysis are the team's own
work. Where an LLM (Claude, Anthropic) helped, it's marked in the code
itself: each notebook has an **"LLM note"** in its first cell stating what
it assisted with, and individual AI-generated cells (e.g. map plots) carry
an inline `# Mostly AI-generated` comment.

## Technologies

**Analysis:** Python, Pandas, NumPy, SciPy, Jupyter, requests /
openmeteo-requests, Matplotlib
**Website:** Streamlit, Plotly
**Both:** Git / GitHub
