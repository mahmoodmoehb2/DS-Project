from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
from content import RQ_META




DATA_DIR = Path(__file__).resolve().parents[1] / "data"

COUNTRY_TRENDS_FILE = DATA_DIR / "RQ3_country_trends.csv"
EVENT_FILE = DATA_DIR / "RQ3_heatwaves_events.csv"

ANALYSIS_START = 1980
ANALYSIS_END = 2025




EUROPE_TRENDS = pd.DataFrame(
    [
        ("Frequency", 3.995, 0.0000, True),
        ("Peak Temperature", 0.016, 0.1854, False),
        ("Average Temperature", 0.004, 0.6896, False),
        ("Duration", 0.039, 0.0000, True),
    ],
    columns=["metric", "slope", "p_value", "significant"],
)

EUROPE_TRENDS_1991 = pd.DataFrame(
    [
        ("Frequency", 5.015, 0.0000, True),
        ("Peak Temperature", 0.032, 0.0566, False),
        ("Average Temperature", 0.015, 0.3058, False),
        ("Average Duration", 0.046, 0.0000, True),
    ],
    columns=["metric", "slope", "p_value", "significant"],
)




@st.cache_data
def load_country_trends():
    if not COUNTRY_TRENDS_FILE.exists():
        return None

    return pd.read_csv(COUNTRY_TRENDS_FILE)


@st.cache_data
def load_events():
    if not EVENT_FILE.exists():
        return None

    df = pd.read_csv(EVENT_FILE)

    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"], errors="coerce")

    if "end" in df.columns:
        df["end"] = pd.to_datetime(df["end"], errors="coerce")

    if "year" not in df.columns and "start" in df.columns:
        df["year"] = df["start"].dt.year

    return df



def build_yearly(events, start_year=ANALYSIS_START, end_year=ANALYSIS_END, selected_countries=None):
    if events is None or events.empty:
        return None

    required = {"year", "max_temp", "avg_temp", "duration_days"}

    if not required.issubset(events.columns):
        return None

    events = events[
        events["year"].between(start_year, end_year, inclusive="both")
    ].copy()

    if selected_countries and "country" in events.columns:
        events = events[events["country"].isin(selected_countries)].copy()

    yearly = (
        events.groupby("year")
        .agg(
            n_heatwaves=("year", "size"),
            avg_max_temp=("max_temp", "mean"),
            avg_avg_temp=("avg_temp", "mean"),
            avg_duration=("duration_days", "mean"),
        )
        .reset_index()
    )

    all_years = pd.DataFrame(
        {"year": range(start_year, end_year + 1)}
    )

    yearly = all_years.merge(yearly, on="year", how="left")

    yearly["n_heatwaves"] = yearly["n_heatwaves"].fillna(0)

    for col in [
        "n_heatwaves",
        "avg_max_temp",
        "avg_avg_temp",
        "avg_duration",
    ]:
        yearly[f"{col}_smooth"] = (
            yearly[col]
            .rolling(
                window=5,
                min_periods=1,
                center=True,
            )
            .mean()
        )

    return yearly




def apply_plot_style(fig, y_title):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            color="#1F2937",
            size=13,
        ),
        xaxis_title="Year",
        yaxis_title=y_title,
        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10,
        ),
        height=440,
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        dtick=5,
    )

    fig.update_yaxes(
        gridcolor="#EDE9FE",
        zeroline=False,
    )

    return fig




def render_summary_cards():
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Cities studied",
        "99",
    )

    c2.metric(
        "Countries represented",
        "50",
    )

    c3.metric(
        "Detected heatwaves",
        "3,459",
    )

    c4.metric(
        "Analysis period",
        "1980-2025",
    )




def render_yearly_chart(yearly, metric):
    if yearly is None:
        st.info(
            "The yearly event data could not be loaded. "
            "Make sure `RQ3_heatwaves_events.csv` is stored in `website/data/`."
        )

        render_europe_trend_summary(metric)

        return

    config = {
        "Frequency": (
            "n_heatwaves_smooth",
            "Number of heatwaves per year",
            "Heatwave frequency across the studied European cities",
        ),
        "Peak temperature": (
            "avg_max_temp_smooth",
            "peak temperature (°C)",
            "peak temperature of detected heatwaves",
        ),
        "Average temperature": (
            "avg_avg_temp_smooth",
            "Average heatwave temperature (°C)",
            "Average temperature within detected heatwaves",
        ),
        "Duration": (
            "avg_duration_smooth",
            "Average heatwave duration (days)",
            "Average duration of detected heatwaves",
        ),
    }

    column, y_label, title = config[metric]

    fig = px.line(
        yearly,
        x="year",
        y=column,
    )

    fig.update_traces(
        line_width=3,
    )

    apply_plot_style(
        fig,
        y_label,
    )

    fig.update_layout(
        title=dict(
            text=title,
            x=0,
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


def render_europe_trend_summary(metric):
    row = EUROPE_TRENDS[
        EUROPE_TRENDS["metric"] == metric
    ].iloc[0]

    unit = {
        "Frequency": "heatwaves/year",
        "Peak Temperature": "°C/year",
        "Average Temperature": "°C/year",
        "Duration": "days/year",
    }[metric]

    status = (
        "Statistically significant"
        if row["significant"]
        else "Not statistically significant"
    )

    st.metric(
        metric,
        f"{row['slope']:+.3f} {unit}",
    )

    st.caption(
        f"p={row['p_value']:.4f} · {status}"
    )




def render_country_comparison(country_df, metric):
    if country_df is None or country_df.empty:
        st.error(
            "Missing `data/RQ3_country_trends.csv`."
        )

        st.caption(
            f"Expected file: `{COUNTRY_TRENDS_FILE}`"
        )

        if DATA_DIR.exists():
            files = sorted(
                p.name
                for p in DATA_DIR.iterdir()
                if p.is_file()
            )

            if files:
                st.caption(
                    "Files currently found in the data folder:"
                )

                st.code(
                    "\n".join(files)
                )

        return

    config = {
        "Frequency": (
            "frequency_slope",
            "n_cities_frequency",
            "Median change in heatwave frequency per city and year",
        ),
        "Average temperature": (
            "temperature_slope",
            "n_cities_temperature",
            "Median temperature change (°C/year)",
        ),
        "Average Duration": (
            "duration_slope",
            "n_cities_duration",
            "Median duration change (days/year)",
        ),
    }



    country_metric = metric

    if country_metric == "Peak temperature":
        st.info(
            "Country-level peak-temperature trends are not available in the "
            "RQ3 country trend table, so the frequency ranking is shown instead."
        )
        country_metric = "Frequency"

    if country_metric not in config:
        country_metric = "Frequency"

    value_col, n_col, y_label = config[country_metric]

    required_columns = {
        "country",
        value_col,
        n_col,
    }

    if not required_columns.issubset(country_df.columns):
        st.error(
            "The country-trend CSV does not contain the expected columns."
        )

        st.write(
            "Columns found:",
            list(country_df.columns),
        )

        return

    plot_df = (
        country_df
        .sort_values(
            value_col,
            ascending=False,
        )
        .copy()
    )

    plot_df["Evidence"] = plot_df[n_col].apply(
        lambda n: "≥3 cities" if n >= 3 else "<3 cities"
    )

    fig = px.bar(
        plot_df,
        x="country",
        y=value_col,
        color="Evidence",
        text=value_col,
        color_discrete_map={
            "≥3 cities": "#2A78D6",
            "<3 cities": "#C9CED6",
        },
    )

    fig.update_traces(
        texttemplate="%{text:+.3f}",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            color="#1F2937",
            size=13,
        ),
        xaxis_title="",
        yaxis_title=y_label,
        legend_title="Evidence base",
        height=460,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10,
        ),
    )

    fig.update_yaxes(
        gridcolor="#EDE9FE",
        zeroline=True,
        zerolinecolor="#9CA3AF",
    )

    fig.update_xaxes(
        showgrid=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )





def render_trend_statistics():
    display = EUROPE_TRENDS.copy()

    display["Slope / year"] = display["slope"].map(
        lambda x: f"{x:+.3f}"
    )

    display["p-value"] = display["p_value"].map(
        lambda x: (
            "<0.0001"
            if x < 0.0001
            else f"{x:.4f}"
        )
    )

    display["Significant"] = display[
        "significant"
    ].map(
        {
            True: "Yes",
            False: "No",
        }
    )

    st.dataframe(
        display[
            [
                "metric",
                "Slope / year",
                "p-value",
                "Significant",
            ]
        ].rename(
            columns={
                "metric": "Metric"
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown(
        "**Sensitivity check: 1991–2025**"
    )

    sensitivity = EUROPE_TRENDS_1991.copy()

    sensitivity["Slope / year"] = sensitivity[
        "slope"
    ].map(
        lambda x: f"{x:+.3f}"
    )

    sensitivity["p-value"] = sensitivity[
        "p_value"
    ].map(
        lambda x: (
            "<0.0001"
            if x < 0.0001
            else f"{x:.4f}"
        )
    )

    sensitivity["Significant"] = sensitivity[
        "significant"
    ].map(
        {
            True: "Yes",
            False: "No",
        }
    )

    st.dataframe(
        sensitivity[
            [
                "metric",
                "Slope / year",
                "p-value",
                "Significant",
            ]
        ].rename(
            columns={
                "metric": "Metric"
            }
        ),
        hide_index=True,
        use_container_width=True,
    )




def render_method():
    st.markdown(
        """
        **Study population.** European cities with at least 500,000 inhabitants,
        plus national capitals even when their population is below 500,000.

        The raw city list contained 101 entries in 50 countries. Historical
        duplicate entries for Pest and Buda were excluded, leaving 99 cities.

        **Analysis period.** 1980-2025.

        **Reference period.** 1961-1990.

        **Heatwave definition.** At least 3 consecutive days above both a
        city-specific 98th-percentile threshold and an absolute threshold of 28°C.

        **Country ranking.** For each city, the annual heatwave-frequency slope
        was estimated. Countries were ranked by the median city-level slope.
        Countries represented by fewer than 3 cities were excluded from the
        country ranking.

        **Important limitation.** The fixed 28°C threshold can disadvantage
        cooler countries because unusually warm periods below 28°C are not
        counted as heatwaves.
        """
    )




def _render_rq3_content():
    st.markdown(
        '<div class="eyebrow">RQ3 · HEATWAVES · EUROPE</div>',
        unsafe_allow_html=True,
    )

    st.title(
        "How are heatwaves changing across European cities?"
    )

    st.markdown(
        f"**Research question:** {RQ_META['rq3']['title']}"
        )
    
    st.subheader("How the analysis works")
    render_method()

    

    st.write("")
    st.subheader("Explore the results")

    st.markdown(
        "Change the analysis period, select countries, and switch between "
        "heatwave metrics. The long-term chart updates automatically."
    )

    events = load_events()
    country_df = load_country_trends()

    selected_years = st.slider(
        "Select analysis period",
        min_value=ANALYSIS_START,
        max_value=ANALYSIS_END,
        value=(ANALYSIS_START, ANALYSIS_END),
        step=1,
        key="rq3_year_range",
    )
    start_year, end_year = selected_years

    if events is not None and "country" in events.columns:
        all_countries = sorted(
            events["country"].dropna().astype(str).unique().tolist()
        )

        selected_countries = st.multiselect(
            "Select countries",
            options=all_countries,
            default=[],
            placeholder="Leave empty to include all countries",
            key="rq3_country_filter",
        )

        active_countries = (
            selected_countries if selected_countries else all_countries
        )
    else:
        all_countries = []
        selected_countries = []
        active_countries = []

    metric = st.segmented_control(
        "Select heatwave metric",
        [
            "Frequency",
            "Duration",
        ],
        default="Frequency",
        key="rq3_metric",
    )

    if metric is None:
        metric = "Frequency"

    yearly_filtered = build_yearly(
        events,
        start_year=start_year,
        end_year=end_year,
        selected_countries=active_countries if active_countries else None,
    )

    if all_countries:
        if selected_countries:
            if len(selected_countries) == 1:
                country_scope = "1 selected country"
            else:
                country_scope = f"{len(selected_countries)} selected countries"
        else:
            country_scope = f"all {len(all_countries)} countries"

        st.caption(
            f"Current selection: {start_year}–{end_year} · {country_scope}"
        )
    else:
        st.caption(
            f"Current selection: {start_year}–{end_year}"
        )

    tab1, tab2 = st.tabs(
        [
            "Long-term trend",
            "Country comparison",
        ]
    )

    with tab1:
        st.markdown(
            f"#### Development from {start_year} to {end_year}"
        )

        render_yearly_chart(
            yearly_filtered,
            metric,
        )


    with tab2:
        st.markdown("#### Country comparison")

        if selected_countries and country_df is not None and "country" in country_df.columns:
            filtered_country_df = country_df[
                country_df["country"].isin(selected_countries)
            ].copy()
        else:
            filtered_country_df = country_df

        render_country_comparison(
            filtered_country_df,
            metric,
        )


    st.markdown("---")


    
    st.subheader("Conclusion")

    st.markdown(
        """
        As with the German-only analysis, frequency and duration remain clearly significantregardless of the exact time window used, the most robust finding of this research question. Peak temperature stays just short of significance even after removing the reference-period overlap (p = 0.057 for 1991–2025, compared to p = 0.185 for the full period), a weaker signal than seen for 
        Germany alone, so we treat any warming in peak heatwave temperature across Europe as suggestive rather 
        than confirmed. Average heatwave temperature shows no evidence of a trend in either window.
        """
    )

    render_trend_statistics()

def render_method():
    st.markdown(
        """
        The analysis follows four main steps:

        **1. Select European cities**  
        European cities with at least **500,000 inhabitants** were included.
        National capitals were included even if their population was below
        this threshold.

        **2. Detect heatwaves**  
        Heatwaves were identified for **1980-2025** using a city-specific
        **98th-percentile temperature threshold** based on the **1961-1990
        reference period**, together with an absolute threshold above **28 °C**.
        A heatwave required at least **3 consecutive qualifying days**.

        **3. Analyse long-term trends**  
        Annual changes in **heatwave frequency, peak temperature, average
        temperature, and duration** were analysed. Linear regression was used
        to estimate the trend over time and assess statistical significance.

        **4. Compare countries**  
        City-level trends were aggregated by country to identify which
        countries experienced the strongest increases in heatwave frequency.
        Countries with fewer than **3 analysed cities** were excluded from
        the frequency ranking.
        """
    )

def render():
    with st.container(
        key="rq3_page_shell"
    ):
        _render_rq3_content()
