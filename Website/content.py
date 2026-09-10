"""Content/config for all six research questions.

RQ1–RQ4 now have completed heatwave analyses behind them.
RQ5–RQ6 remain planned until the UV analyses are completed.
"""

# Metrics used on heatwave research pages.
METRICS = [
    {
        "key": "frequency",
        "label": "Heatwave frequency",
        "suffix": "frequency",
        "chart_title": "Heatwave frequency",
    },
    {
        "key": "peak_temp",
        "label": "Peak temperature",
        "suffix": "peak_temp",
        "chart_title": "Average peak temperature",
    },
    {
        "key": "avg_temp",
        "label": "Average temperature",
        "suffix": "avg_temp",
        "chart_title": "Average heatwave temperature",
    },
    {
        "key": "duration",
        "label": "Duration",
        "suffix": "duration",
        "chart_title": "Average heatwave duration",
    },
]


RQ_META = {
    "rq1": {
        "code": "RQ1",
        "short": "German heatwave trends",
        "title": (
            "How have the frequency, intensity (peak and average temperature),"
            " and duration of heatwaves in major German cities (≥150,000 inhabitants)"
            " changed between 1980 and today?"
        ),
        "description": (
            "We analyse long-term changes in heatwave frequency, peak temperature, "
            "average temperature and duration across 56 major German cities."
        ),
        "status": "ready",
        "country": "Germany",
        "events_csv": "RQ1_heatwaves_events.csv",
        "key_findings": {
            "frequency": (
                "Heatwave frequency increased significantly across the studied "
                "German major cities between 1980 and 2025."
            ),
            "peak_temp": (
                "No statistically significant full-period increase in average "
                "heatwave peak temperature was detected."
            ),
            "avg_temp": (
                "No statistically significant full-period increase in average "
                "heatwave temperature was detected."
            ),
            "duration": (
                "Heatwave duration increased significantly over the study period."
            ),
        },
        "methodology": (
            "Major German cities were selected using a population threshold of "
            "at least 150,000 inhabitants. Heatwaves were identified for 1980–2025 "
            "using a city-specific 98th-percentile threshold based on the 1961–1990 "
            "reference period together with an absolute threshold above 28 °C. "
            "A heatwave required at least 3 consecutive qualifying days."
        ),
    },

    "rq2": {
        "code": "RQ2",
        "short": "Germany: Urban vs. rural",
        "title": (
            "How do heatwave frequency, intensity (peak and average temperature), "
            "and duration differ across city sizes, from large cities to rural "
            "municipalities, within the same region in Germany?"
        ),
        "description": (
            "We compare large cities, medium-sized cities, small towns and rural "
            "municipalities using the same heatwave definition."
        ),
        "status": "ready",
        "country": "Germany",
        "events_csv": "RQ2_heatwaves_events.csv",
        "key_findings": {
            "frequency": (
                "Since 1980, heatwave frequency has increased significantly across "
                "all four city-size classes in Germany, at roughly +0.03 heatwaves "
                "per place per year."
            ),
            "peak_temp": (
                "No statistically significant increase in heatwave peak temperature "
                "was observed in any city-size class."
            ),
            "avg_temp": (
                "No statistically significant increase in average heatwave "
                "temperature was observed in any city-size class."
            ),
            "duration": (
                "Heatwave duration increased significantly only in large and "
                "medium-sized cities."
            ),
        },
        "methodology": (
            "Locations were grouped into four population classes: large cities "
            "(≥150,000), medium-sized cities (20,000–149,999), small towns "
            "(5,000–19,999) and rural municipalities (1,000–4,999). Rural "
            "municipalities were operationally required to be at least 15 km from "
            "a large-city centre. Heatwaves were defined as at least 3 consecutive "
            "days above both the location-specific 98th-percentile threshold "
            "(1961–1990 reference period) and 28 °C. The analysis covers 1980–2025."
        ),
    },

    "rq3": {
        "code": "RQ3",
        "short": "Europe heatwave trends",
        "title": (
            "How have the frequency, intensity, and duration of heatwaves changed "
            "across major European cities since 1980, and which country is most "
            "strongly affected?"
        ),
        "description": (
            "We analyse 99 European cities across 50 countries, including cities "
            "with at least 500,000 inhabitants and national capitals."
        ),
        "status": "ready",
        "country": "Europe",
        "events_csv": "RQ3_heatwaves_events.csv",
        "country_trends_csv": "RQ3_country_trends.csv",
        "key_findings": {
            "frequency": (
                "Across the studied European cities, heatwave frequency increased "
                "significantly by about +4.0 events per year between 1980 and 2025."
            ),
            "peak_temp": (
                "Peak heatwave temperature did not show a statistically significant "
                "full-period trend."
            ),
            "avg_temp": (
                "Average heatwave temperature did not show a statistically "
                "significant full-period trend."
            ),
            "duration": (
                "Average heatwave duration increased significantly by about "
                "+0.04 days per year."
            ),
        },
        "methodology": (
            "The sample contains European cities with at least 500,000 inhabitants "
            "plus national capitals even when below that threshold. After excluding "
            "historical duplicate entries for Pest and Buda, 99 cities in 50 "
            "countries remained. Heatwaves were detected for 1980–2025 using a "
            "city-specific 98th-percentile threshold based on 1961–1990 together "
            "with an absolute threshold above 28 °C, for at least 3 consecutive days."
        ),
    },

    "rq4": {
        "code": "RQ4",
        "short": "Italy: Urban vs. rural",
        "title": (
            "In the European country most strongly affected by rising heatwave "
            "trends, does this effect concentrate in large cities, or is it equally "
            "present in smaller cities and rural municipalities?"
        ),
        "description": (
            "Italy was identified in RQ3 as the country with the strongest median "
            "city-level increase in heatwave frequency. We compare trends across "
            "four population classes."
        ),
        "status": "ready",
        "country": "Italy",
        "events_csv": "RQ4_Italy_heatwaves_events.csv",
        "key_findings": {
            "frequency": (
                "Since 1980, heatwave frequency increased significantly across all "
                "city sizes in Italy, at roughly +0.07 heatwaves per place per year."
            ),
            "peak_temp": (
                "Peak temperature increased significantly only in the large-city "
                "class; the other size classes showed no significant trend."
            ),
            "avg_temp": (
                "Average heatwave temperature did not increase significantly in "
                "any city-size class."
            ),
            "duration": (
                "Heatwave duration increased significantly across all four "
                "city-size classes, at roughly +0.06 days per year."
            ),
        },
        "methodology": (
            "The Italy analysis applies the same heatwave definition and population "
            "thresholds as the Germany city-size analysis. Because Italy does not "
            "use a city-status distinction equivalent to the German system, the "
            "classes are defined only by population. The analysis covers 1980–2025 "
            "with a 1961–1990 reference period."
        ),
    },

    "rq5": {
        "code": "RQ5",
        "short": "UV trends across Europe",
        "title": (
            "How has the UV Index across Europe changed over the past 20 years, "
            "and are there significant temporal and regional trends?"
        ),
        "status": "ready",
    },

    "rq6": {
        "code": "RQ6",
        "short": "UV exposure & health",
        "title": (
            "What are the public health implications of rising UV Index trends "
            "in highly affected European regions, particularly regarding sunburn risk?"
        ),
        "status": "ready",
    },
}