# Zugriff auf das Betriebssystem und der zugehörigen  Ordnerstruktur
import os
import zipfile
# Import zum Erstellen von Anfragen an die APIs
import requests
# Erstellen einer Datenmenge, um die gesammelten Daten zu speichern 
import xarray as xr
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Startjahr für das Erfassen der Daten 
START_YEAR = 2000
# Endjahr für das Erfassen der Daten
END_YEAR = 2025
# Variablen für den Zugriff auf die erstellten Dateien
GEONAMES_ZIP = "cities500.zip"
GEONAMES_TXT = "cities500.txt"

# Ländercode Array
european_countries = [
    "AD", "AL", "AT", "AX", "BA", "BE", "BG", "BY",
    "CH", "CZ", "DE", "DK", "EE", "ES", "FI", "FO",
    "FR", "GB", "GG", "GI", "GR", "HR", "HU", "IE",
    "IM", "IS", "IT", "JE", "LI", "LT", "LU", "LV",
    "MC", "MD", "ME", "MK", "MT", "NL", "NO", "PL",
    "PT", "RO", "RS", "SE", "SI", "SJ", "SK",
    "SM", "UA", "VA"
]

# Array zum Erzeugen des Plots für Europäische Regionen
regions = {

    # Nord Europa
    "DK": "Northern Europe","EE": "Northern Europe","FI": "Northern Europe","IS": "Northern Europe","LT": "Northern Europe",
    "LV": "Northern Europe","NO": "Northern Europe","SE": "Northern Europe","GB": "Northern Europe", "IE": "Northern Europe",

    # West Europa
    "AT": "Western Europe","BE": "Western Europe","CH": "Western Europe","DE": "Western Europe","FR": "Western Europe",
    "LI": "Western Europe","LU": "Western Europe","MC": "Western Europe","NL": "Western Europe",

    # Ost Europa
    "BG": "Eastern Europe","BY": "Eastern Europe","CZ": "Eastern Europe","HU": "Eastern Europe","MD": "Eastern Europe",
    "PL": "Eastern Europe","RO": "Eastern Europe","SK": "Eastern Europe","UA": "Eastern Europe",

    # Süd Europa
    "AL": "Southern Europe", "AD": "Southern Europe","BA": "Southern Europe","ES": "Southern Europe",
    "GR": "Southern Europe","HR": "Southern Europe","IT": "Southern Europe","ME": "Southern Europe",
    "MK": "Southern Europe","MT": "Southern Europe","PT": "Southern Europe","RS": "Southern Europe",
    "SI": "Southern Europe","SM": "Southern Europe","VA": "Southern Europe"
}


# Download der Europäischen Städte von GeoNames (API)

def download_geonames():

    # Nicht erneut herunterladen, wenn bereits vorhanden
    if os.path.exists(GEONAMES_TXT):
        print("GeoNames bereits vorhanden.")
        return

    

    url = (
        "https://download.geonames.org/"
        "export/dump/cities500.zip"
    )
    # Anfrage an GeoNames mittels URL und Abfrage des Status der Anfrage
    response = requests.get(url)
    response.raise_for_status()
    # Speichern der Datei GEONAMES_ZIP, wenn noch nicht vorhanden und Daten aus Abfrage speichern 
    with open(GEONAMES_ZIP, "wb") as file:
        file.write(response.content)

   
    # Öffnen und Entpacken der zuvor erstellten ZIP Datei
    with zipfile.ZipFile(GEONAMES_ZIP, "r") as zip_ref:
        zip_ref.extractall(".")

    print("GeoNames fertig.")


def load_cities():
    # Spaltenbezeichnungen für die Tabelle der Städte 
    columns = ["geonameid","name","asciiname","alternatenames","latitude","longitude","feature_class","feature_code",
               "country_code","cc2","admin1","admin2","admin3","admin4","population","elevation","dem","timezone","modification_date"]
    # Dataframe für GeoNames(API) und Darstellung in der Tabelle nach Columns bei Trennung nach Tabulator
    df = pd.read_csv(
        GEONAMES_TXT,
        sep="\t",
        names=columns,
        low_memory=False
    )
    # cities collects all countries with a population with min. 500.000
    cities = df[
        (df["country_code"].isin(european_countries))
        & (df["population"] >= 500000)
    ].copy()
    
   
                

    cities = cities[["name","country_code","population","latitude","longitude"]]

    cities = cities.sort_values(
        "population",
        ascending=False
    )

    return cities
# Anfrage an Temis und erstellen der Datei mit den angefragten Daten von Temis
 
def download_temis(year):
    # Datei-Name für die zu erstellende Datei
    filename = f"uv_{year}.nc"

    # Datei nicht erneut herunterladen
    if os.path.exists(filename):
        print(f"TEMIS {year} bereits vorhanden.")
        return filename
    # Anzufragende URL von Temis 
    url = (
        "https://www.temis.nl/uvradiation/v2.0/msr2/nc/"
        f"{year}/uvief{year}_msr_europe.nc"
    )

    
    # Anfrage an TEMIS mittels URL nach Jahr
    response = requests.get(url)
    response.raise_for_status()
    # Erstellen der Datei, falls noch nicht vorhanden und ansonsten vorhandene Datei nutzen um die Daten der Abfrage zu speichern
    with open(filename, "wb") as file:
        file.write(response.content)
    # Rückgabe des Dateinamens
    return filename



# Ausführung der Anfrage an GeoNames, um die Datei mit Städten zu erzeugen 
download_geonames()
#
cities = load_cities()



# Liste für alle Ergebnisse zu UV-Index, duchschnittlicher UV Index und Uv-Maximum zu jedem Koordinatenpunkt und Jahr 
results = []
# Für jedes Jahr zwischen dem Startjahr und Endjahr die Daten von Temis laden 
for year in range(START_YEAR, END_YEAR + 1):
    # Laden der Informationen von TEMIS
    filename = download_temis(year)
    # ds ist der geööfnete Datensatz von TEMIS
    ds = xr.open_dataset(filename,group="PRODUCT")
    # 
    for index, city in cities.iterrows():
        # Extrahieren der UV Daten aus dem TEMIS-Datensatz am nahgelegensten Koordinatenpunkt (xArray-Objekt)
        uv = ds["uvi_clear"].sel(latitude=city["latitude"],longitude=city["longitude"],method="nearest")
        # Berechnet aus den UV Daten eines Koordinatenpunktes(Stadt) den Durchschnittswert der UV-Werte 
        mean_uvi = float(uv.mean(skipna=True).values)
        # Findet aus dem xarray zu uv den maximalen UV-Wert und liefert deren Wert zurück 
        max_uvi = float(uv.max(skipna=True).values)
        # In result Dictionary hinzufügen zu dem jeweiligen Land und Jahr 
        results.append({"city": city["name"],"country": city["country_code"],"population": city["population"],"latitude": city["latitude"],
                         "longitude": city["longitude"],"year": year,"mean_uvi": mean_uvi,"max_uvi": max_uvi})

    ds.close()
# Erstellung eines Dataframes aus allen Daten zu jedem Koordinatenpunkt und zu jedem Jahr 
df = pd.DataFrame(results)

# Region anhand des Landes hinzufügen
df["region"] = df["country"].map(regions)
# Erstellung einer CSV Datei aus dem erstellten Dataframe 
df.to_csv( "europe_uv_2000_2025.csv",index=False)

trends = []

for (city_name,country_code), city_data in df.groupby(["city", "country"]):
    # sortiert die Daten einer Stadt nach dem Kriterium Jahr 
    city_data = city_data.sort_values("year")
    # Berechnet die Regression  mit der abhängigen Variable mean_uvi (y) und unabhängige Variable year(x)
    # Es werden alle Wertpaare zwischen year und mean_uvi von einer Stadt herangezogen
    regression = linregress(city_data["year"],city_data["mean_uvi"])
    
    # city: Neme der Stadt
    # Country_code : Ländercode für die Stadt
    # trend_per_year : Steigung der Regressionsgeraden
    # trend_25_years: Steigung der Regressionsgeraden(trend_per_year) * 25
    # significant : Ist das Signifikanzniveau höher oder niederiger als 5% (Signifikanzniveau)
    # r_squared : 
    trends.append({"city": city_name,"country": country_code,"trend_per_year": regression.slope,"trend_25_years": regression.slope * 25,"p_value": regression.pvalue,"significant": regression.pvalue < 0.05,"r_squared": regression.rvalue ** 2 })

# Data-Frame erstellen aus den gesammelten Daten 
trend_df = pd.DataFrame(trends)
# Aus Data-Frame CSV Datei erstellen 
trend_df.to_csv("europe_uv_trends.csv", index=False)
# Filtert aus der Boolean-Serie alle Werte mit False raus und sortiert ansschließend absteigend, wobei kein Reset der Indizes vorgenommen werden
significant = trend_df[trend_df["significant"]].sort_values("trend_per_year",ascending=False)
# Sortier das DataFrame nach der Kategorier des Jahres und berechnet anschließend den Durchschnitt 
europe = (df.groupby("year")["mean_uvi"].mean().reset_index())
# Betrachtet die lineare Regression zwischen dem Jahr und dem durchnscittlichen UV-Index 
europe_trend = linregress(europe["year"],europe["mean_uvi"])

# Regressionsgerade anhand der Serie über die Jahre zwischen 2000 und 2026
europe_trend_line = (europe_trend.intercept + europe_trend.slope * europe["year"] )

plt.figure(figsize=(10, 6))

# Gemessene Jahreswerte
plt.plot(europe["year"], europe["mean_uvi"], marker="o",label="Mean UV Index")

# Zeichnen der Regressionsgerade
plt.plot(europe["year"],europe_trend_line,label="Linear Trend")

# Achsen-Beschreibung für den Plot
plt.xlabel("Year") # x-Achse
plt.ylabel("Mean UV Index") # y-Achse 

plt.title(f"European UV Index Trend 2000–2025\n"f"p = {europe_trend.pvalue:.4f} | " f"Significant: {europe_trend.pvalue < 0.05}")

plt.xticks(europe["year"], rotation=45 )
# Sammelt die Labels (dritter Wert im Tripel) der einzelenen Linien und zeigt  es als Legende an 
plt.legend()
# Anlegen eines orthogonalen Rasters
plt.grid()
# Passt alles optisches so an, dass es passt 
plt.tight_layout()
# Anzeigen  die Visualisierung 
plt.show()




regional = (df.groupby(["region", "year"])["mean_uvi"].mean().reset_index())


regional_trends = []

for region, region_data in regional.groupby("region"):

    regression = linregress(region_data["year"],region_data["mean_uvi"]
)

    regional_trends.append({
        "region": region,
        "trend_per_year": regression.slope,
        "trend_25_years": regression.slope * 25,
        "p_value": regression.pvalue,
        "significant": regression.pvalue < 0.05,
        "r_squared": regression.rvalue ** 2
    })


regional_trend_df = pd.DataFrame(
    regional_trends
)

regional_trend_df.to_csv(
    "regional_uv_trends.csv",
    index=False
)

for region, region_data in regional.groupby("region"):
    # Erstellen der Regression der Regionen
    regression = linregress(region_data["year"],region_data["mean_uvi"] )

    # Regressionsgerade (y= b + m * x)
    trend_line = (regression.intercept + regression.slope * region_data["year"])

    # Für jede Region eine neue Figure
    plt.figure(figsize=(10, 6))

    # Tatsächliche Jahreswerte der Region
    plt.plot(region_data["year"],region_data["mean_uvi"],marker="o",label="Mean UV Index")

    # Regressionsgerade zeichnen
    plt.plot(region_data["year"],trend_line,label="Linear Trend")
    # Bezeichnung der X-Achse
    plt.xlabel("Year")
    # Bezeichnung der Y-Achse
    plt.ylabel("Mean UV Index")
    # Setzen des Titels des Plots
    plt.title(f"{region} UV Index Trend 2000–2025\n"f"p = {regression.pvalue:.4f} | " f"Significant: {regression.pvalue < 0.05}")

    plt.xticks(region_data["year"],rotation=45)
    # Sammelt die Labels (dritter Wert im Tripel) der einzelenen Linien und zeigt  es als Legende an 
    plt.legend()
    # Anlegen eines orthogonalen Rasters
    plt.grid()
    # Passt alles optisches so an, dass es passt 
    plt.tight_layout()
    # Anzeigen die Visualisierung 
    plt.show()