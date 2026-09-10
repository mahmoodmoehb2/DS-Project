"""Content/config for all six research questions.

IMPORTANT: only RQ2 (Germany) and RQ4 (Italy) have an actual finished
analysis behind them in this project so far. RQ1, RQ3, RQ5 and RQ6 are kept
here as placeholders that match the navigation structure of the team's
mockup, but they intentionally show NO numbers, charts or "key findings" —
inventing those would misrepresent results nobody has computed yet
(RQ5/RQ6 in particular would need UV radiation data, which this project
has not analysed at all so far). Fill each one in once that analysis
exists, following the RQ2/RQ4 pattern below.
"""

# Metrics shown via the pill selector on a finished RQ page. The `file`
# fields are filled in per-country inside RQ_META below.
METRICS = [
    {"key": "frequency", "label": "Heatwave frequency", "suffix": "frequency",
     "chart_title": "Average heatwave frequency by city size"},
    {"key": "peak_temp", "label": "Peak temperature", "suffix": "peak_temp",
     "chart_title": "Average peak temperature by city size"},
    {"key": "avg_temp", "label": "Average temperature", "suffix": "avg_temp",
     "chart_title": "Average temperature by city size"},
    {"key": "duration", "label": "Duration", "suffix": "duration",
     "chart_title": "Average heatwave duration by city size"},
]

RQ_META = {
    "rq1": {
        "code": "RQ1",
        "icon": "trending_up",
        "short": "German cities over time",
        "title": "How have heatwaves in German cities changed over time?",
        "status": "planned",
    },
    "rq2": {
        "code": "RQ2",
        "icon": "location_city",
        "short": "Germany: City sizes",
        "title": "How do heatwaves differ across city sizes in Germany?",
        "description": (
            "We compare heatwave frequency, intensity (peak and average temperature), "
            "and duration from large cities to rural municipalities within the same region."
        ),
        "status": "ready",
        "country": "Germany",
        "image_prefix": "RQ2_heatwaves_yearly_trend",
        "stats_csv": "RQ2_heatwaves_summary_by_sizeclass.csv",
        "trend_csv": "RQ2_trend_statistics.csv",
        "key_findings": {
            "frequency": "Add the regression result for heatwave frequency here once it is available "
                         "(e.g. slope per year and significance per city-size class).",
            "peak_temp": "Add the regression result for peak temperature here once it is available.",
            "avg_temp": "Add the regression result for average temperature here once it is available.",
            "duration": "Add the regression result for duration here once it is available.",
        },
        "methodology": (
            "**Vorgehen in zwei Teilen:** Für jede der 56 deutschen Großstädte (≥150.000 Einwohner) "
            "wird der jeweils nächstgelegene Vergleichsort dreier Größenklassen gesucht: eine "
            "Mittelstadt (20.000–149.999), eine Kleinstadt (5.000–19.999) und eine Gemeinde "
            "(1.000–4.999, ohne Stadtrecht). Auf alle gefundenen Orte wird die DWD-Hitzewellen-"
            "Definition angewendet (≥3 aufeinanderfolgende Tage über dem ortsspezifischen "
            "98.-Perzentil-Schwellenwert **und** über 28 °C).\n\n"
            "Pro Kennzahl wurde ein Kruskal-Wallis-Test über die vier Größenklassen gerechnet — "
            "getestet auf Ebene der eindeutigen Orte, nicht der Einzelereignisse. `p < 0.05` gilt "
            "als Signifikanzschwelle."
        ),
    },
    "rq3": {
        "code": "RQ3",
        "icon": "public",
        "short": "European cities",
        "title": "How do heatwave trends differ across European cities?",
        "status": "planned",
    },
    "rq4": {
        "code": "RQ4",
        "icon": "🇮🇹",
        "short": "Italy: Urban vs. rural",
        "title": "Are rising heatwave trends in Italy concentrated in large cities?",
        "description": (
            "Italy applies the same DWD heatwave definition and methodology as RQ2, adapted for "
            "Italian comuni. We test whether rising trends are limited to large cities or present "
            "across all size classes."
        ),
        "status": "ready",
        "country": "Italy",
        "image_prefix": "RQ2_Italy_heatwaves_yearly_trend",
        "stats_csv": "RQ2_Italy_heatwaves_summary_by_sizeclass.csv",
        "trend_csv": "RQ2_Italy_trend_statistics.csv",
        "key_findings": {
            "frequency": "Add the regression result for heatwave frequency here once it is available.",
            "peak_temp": "Add the regression result for peak temperature here once it is available.",
            "avg_temp": "Add the regression result for average temperature here once it is available.",
            "duration": "Add the regression result for duration here once it is available.",
        },
        "methodology": (
            "Diese Version wendet exakt dieselbe Methodik wie die Deutschland-Analyse (RQ2) auf "
            "Italien an — gleiche Hitzewellen-Definition, gleiche Bevölkerungsschwellen, gleicher "
            "Ablauf. Angepasst werden nur die länderspezifischen Teile: Datenabfrage (italienische "
            "Gemeinden, ISTAT-Gemeindeschlüssel) und Kartengrundlage (italienische Regionen).\n\n"
            "**Wichtige methodische Anpassung:** Italien kennt kein dem deutschen Stadtrecht "
            "vergleichbares Konzept — alle italienischen Orte sind rechtlich gleichgestellte "
            "*comuni*. Die Größenklassen werden hier deshalb ausschließlich über die Einwohnerzahl "
            "bestimmt, bei identischen Schwellenwerten wie in der Deutschland-Version.\n\n"
            "Anders als bei Deutschland zeigt das Häufigkeits-Diagramm hier keine Rohdaten oder "
            "Zoom-Ausschnitt: In den italienischen Daten gab es praktisch in jedem Jahr und jeder "
            "Größenklasse mindestens eine Hitzewelle."
        ),
    },
    "rq5": {
        "code": "RQ5",
        "icon": "wb_sunny",
        "short": "UV trends",
        "title": "How has UV exposure changed across Europe?",
        "status": "planned",
    },
    "rq6": {
        "code": "RQ6",
        "icon": "monitor_heart",
        "short": "UV and health",
        "title": "How are UV exposure and health outcomes related?",
        "status": "planned",
    },
}
