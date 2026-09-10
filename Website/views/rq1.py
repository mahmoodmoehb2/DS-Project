from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from scipy import stats
from content import RQ_META



DATA_DIR = Path(__file__).resolve().parents[1] / "data"
EVENT_FILE = DATA_DIR / "RQ1_heatwaves_events.csv"

ANALYSIS_START = 1980
ANALYSIS_END = 2025
REFERENCE_PERIOD = "1961-1990"

METRICS = {
    "Frequency": {
        "raw": "n_heatwaves",
        "smooth": "n_heatwaves_smooth",
        "title": "Frequency of heatwaves in German major cities",
        "y": "Number of heatwaves per year",
        "unit": "heatwaves/year",
    },
    "Peak temperature": {
        "raw": "avg_max_temp",
        "smooth": "avg_max_temp_smooth",
        "title": "Average peak temperature of heatwaves",
        "y": "Average peak temperature (°C)",
        "unit": "°C/year",
    },
    "Average temperature": {
        "raw": "avg_avg_temp",
        "smooth": "avg_avg_temp_smooth",
        "title": "Average heatwave temperature",
        "y": "Average heatwave temperature (°C)",
        "unit": "°C/year",
    },
    "Duration": {
        "raw": "avg_duration",
        "smooth": "avg_duration_smooth",
        "title": "Average duration of heatwaves",
        "y": "Average heatwave duration (days)",
        "unit": "days/year",
    },
}


RQ1_TRENDS_1991 = pd.DataFrame(
    [
        ("Frequency", 2.2936, 0.0005, True),
        ("Peak Temperature", 0.0674, 0.0245, True),
        ("Average Temperature", 0.0433, 0.0527, False),
        ("Average Duration", 0.0332, 0.0206, True),
    ],
    columns=["metric", "slope", "p_value", "significant"],
)


@st.cache_data
def load_events():
    """Load the event-level heatwave table exported from the RQ1 notebook."""
    if not EVENT_FILE.exists():
        return None

    df = pd.read_csv(EVENT_FILE)

    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"], errors="coerce")

    if "end" in df.columns:
        df["end"] = pd.to_datetime(df["end"], errors="coerce")

    if "year" not in df.columns and "start" in df.columns:
        df["year"] = df["start"].dt.year

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df


def validate_events(df):
    required = {
        "city",
        "year",
        "max_temp",
        "avg_temp",
        "duration_days",
    }

    if df is None:
        return required

    return required - set(df.columns)


def build_yearly(df):
    """
    Same annual aggregation as the notebook:
    - frequency: total detected heatwaves across all cities per year
    - peak temperature: mean max_temp across events per year
    - average temperature: mean avg_temp across events per year
    - duration: mean duration_days across events per year
    """
    yearly = (
        df.groupby("year")
        .agg(
            n_heatwaves=("city", "count"),
            avg_max_temp=("max_temp", "mean"),
            avg_avg_temp=("avg_temp", "mean"),
            avg_duration=("duration_days", "mean"),
        )
        .reset_index()
    )

    years = pd.DataFrame(
        {"year": range(ANALYSIS_START, ANALYSIS_END + 1)}
    )

    yearly = years.merge(yearly, on="year", how="left")
    yearly["n_heatwaves"] = yearly["n_heatwaves"].fillna(0)

    for col in [
        "n_heatwaves",
        "avg_max_temp",
        "avg_avg_temp",
        "avg_duration",
    ]:
        yearly[f"{col}_smooth"] = (
            yearly[col]
            .rolling(5, center=True, min_periods=1)
            .mean()
        )

    return yearly


def calculate_trend(yearly, metric):
    col = METRICS[metric]["raw"]
    valid = yearly.dropna(subset=[col])

    if len(valid) < 3:
        return None

    result = stats.linregress(valid["year"], valid[col])

    return {
        "slope": result.slope,
        "p_value": result.pvalue,
        "r_squared": result.rvalue ** 2,
        "significant": result.pvalue < 0.05,
    }


def all_trend_stats(yearly):
    rows = []

    for metric in METRICS:
        result = calculate_trend(yearly, metric)

        if result is None:
            continue

        rows.append(
            {
                "Metric": metric,
                "Trend per year": result["slope"],
                "p-value": result["p_value"],
                "Significant": "Yes" if result["significant"] else "No",
            }
        )

    return pd.DataFrame(rows)


def plot_yearly_trend(yearly, metric):
    cfg = METRICS[metric]

    plot_df = yearly.dropna(subset=[cfg["smooth"]]).copy()

    fig = px.line(
        plot_df,
        x="year",
        y=cfg["smooth"],
        markers=False,
        title=cfg["title"],
    )

    fig.update_traces(
        line=dict(width=3),
        hovertemplate="Year %{x}<br>%{y:.2f}<extra></extra>",
    )

    fig.update_layout(
        height=500,
        xaxis_title="Year",
        yaxis_title=cfg["y"],
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    fig.update_xaxes(
        dtick=5,
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        gridcolor="rgba(100,100,100,0.15)",
        zeroline=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_city_comparison(df, metric):
    if metric == "Frequency":
        city_df = (
            df.groupby("city")
            .size()
            .reset_index(name="value")
            .sort_values("value", ascending=False)
        )
        y_title = "Detected heatwaves, 1980–2025"

    else:
        source_col = {
            "Peak temperature": "max_temp",
            "Average temperature": "avg_temp",
            "Duration": "duration_days",
        }[metric]

        city_df = (
            df.groupby("city")[source_col]
            .mean()
            .reset_index(name="value")
            .sort_values("value", ascending=False)
        )
        y_title = METRICS[metric]["y"]

    top = city_df.head(15)

    fig = px.bar(
        top,
        x="city",
        y="value",
        text="value",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_layout(
        height=500,
        xaxis_title="City",
        yaxis_title=y_title,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
    )

    fig.update_yaxes(
        gridcolor="rgba(100,100,100,0.15)",
        zeroline=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def render_trend_statistics(yearly):
    stats_df = all_trend_stats(yearly)

    if stats_df.empty:
        st.info("Not enough data to calculate trend statistics.")
        return

    display = stats_df.copy()

    display["Trend per year"] = display["Trend per year"].map(
        lambda x: f"{x:+.4f}"
    )

    display["p-value"] = display["p-value"].map(
        lambda x: "<0.0001" if x < 0.0001 else f"{x:.4f}"
    )

    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
    )

    

def render_summary_cards(df):
    n_cities = df["city"].nunique()
    n_events = len(df)

    first_year = int(df["year"].min())
    last_year = int(df["year"].max())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Cities with events", f"{n_cities}")
    c2.metric("Detected heatwaves", f"{n_events:,}")
    c3.metric("Analysis period", f"{first_year}–{last_year}")
    c4.metric("Heatwave definition", "≥3 days")


def render_method():
    left, right = st.columns(2)

    with left:
        st.markdown(
            f"""
            **Study design**

            - German major cities with population ≥150,000
            - Analysis period: **{ANALYSIS_START}–{ANALYSIS_END}**
            - Reference period: **{REFERENCE_PERIOD}**
            """
        )

    with right:
        st.markdown(
            """
            **Heatwave definition**

            A heatwave consists of at least **3 consecutive days**
            where daily maximum temperature is:

            - above the city-specific **98th percentile** based on 1961-1990, and
            - above **28°C**.
            """
        )



def _render_rq1_content():
    st.markdown(
        '<div class="eyebrow">RQ1 · HEATWAVES · GERMANY</div>',
        unsafe_allow_html=True,
    )

    st.title("Are heatwaves in Germany really becoming more common?")

    st.markdown(
        f"**Research question:** {RQ_META['rq1']['title']}"
)
    
    st.subheader("How the analysis works")
    render_method()

    df = load_events()

    if df is None:
        st.error(
            "Missing data file: `data/RQ1_heatwaves_events.csv`"
        )
        st.info(
            "Export `data/processed/heatwaves.csv` from the RQ1 notebook "
            "as `RQ1_heatwaves_events.csv` and place it in the website's "
            "`data/` folder."
        )
        return

    missing = validate_events(df)

    if missing:
        st.error(
            "The CSV is missing these required columns: "
            + ", ".join(sorted(missing))
        )
        return

    df = df[
        df["year"].between(ANALYSIS_START, ANALYSIS_END, inclusive="both")
    ].copy()



    st.write("")

    yearly = build_yearly(df)
    trend_frequency = calculate_trend(yearly, "Frequency")
    trend_duration = calculate_trend(yearly, "Duration")
    trend_peak = calculate_trend(yearly, "Peak temperature")
    trend_average = calculate_trend(yearly, "Average temperature")

    finding_parts = []

    if trend_frequency and trend_frequency["significant"]:
        finding_parts.append("heatwave frequency increased significantly")

    if trend_duration and trend_duration["significant"]:
        finding_parts.append("average heatwave duration increased significantly")

    if finding_parts:
        finding = (
            "Since 1980, "
            + " and ".join(finding_parts)
            + " across German major cities."
        )
    else:
        finding = (
            "The long-term results are calculated directly from the "
            "RQ1 heatwave event table."
        )



    st.write("")
    st.subheader("Explore the results")

    metric = st.segmented_control(
        "Metric",
        options=[
            "Frequency",
            "Peak temperature",
            "Average temperature",
            "Duration",
        ],
        default="Frequency",
        key="rq1_metric",
    )

    if metric is None:
        metric = "Frequency"

    tab1, tab2 = st.tabs(
        [
            "Long-term trend",
            "City comparison",
        ]
    )

    with tab1:
        st.markdown("#### Development from 1980 to 2025")
        plot_yearly_trend(yearly, metric)
        
        if metric == "Frequency":
            st.caption(
                "Every year, we count how many heatwaves occurred across all 57 cities and track that number from 1980 to 2025, smoothed with a five-year moving average to see past ordinary weather noise. After three decades holding fairly steady around 10–30 heatwaves a year, frequency breaks sharply upward from the mid-2010s onward, reaching over 100 a year by the end of the decade, a rise confirmed statistically (p < 0.0001) rather than just a visual impression. Ranking cities by their total heatwave count shows the increase isn't concentrated in one region: Münster, Ludwigshafen am Rhein, Munich, and Berlin all sit near the top despite very different climates, suggesting a nationwide pattern rather than a local anomaly."
                )
        if metric == "Peak temperature":
            st.caption(
                "For each detected heatwave we record its hottest single day, then average those peaks per year across all cities, testing whether individual events are getting more extreme over time. The yearly average oscillates between roughly 31°C and 33°C across four decades without settling into a direction, and the regression confirms no statistically reliable trend (p = 0.110). Ranking cities by their average peak instead reveals a geographic rather than temporal pattern: Ludwigshafen am Rhein, Karlsruhe, Mainz, and other Rhine valley cities dominate regardless of how often they experience heatwaves, pointing to climate zone, not long-term warming, as the main driver of intensity."
                )
        if metric == "Average temperature":
            st.caption(
                "This metric takes the mean temperature across each heatwave's full duration, not just its hottest moment, guarding against a single extreme afternoon skewing the intensity picture. Like peak temperature, it shows no meaningful long-term trend (p = 0.253). Heatwaves aren't measurably hotter on average today than in 1980, despite occurring far more often. The city ranking reinforces this: it's led by essentially the same Rhine valley cities as the peak-temperature list (Ludwigshafen, Karlsruhe, Mainz, Frankfurt), evidence that heatwave intensity is shaped mainly by regional climate rather than a warming trend over time."
                )
        if metric == "Duration":
            st.caption(
                "Duration averages the length in days of every detected heatwave per year, again smoothed over a five-year window. Unlike the two temperature metrics, this one shows a real upward trend, confirmed at p = 0.0107: after hovering close to the 3-day minimum for two decades, average duration climbs steadily from around 2010 onward, passing 4.3 days by 2025. That matters beyond the statistics too, since prolonged heat exposure, not a single hot day, drives most heat-related health risk, connecting this result directly to the project's later public-health questions. The cities with the longest-lasting heatwaves (Bremen, Hamburg, Hannover) cluster in the north, a different group from the Rhine valley cities dominating the temperature rankings, suggesting duration is governed by different regional factors than intensity."
                )



    with tab2:
        st.markdown("#### Comparison between cities")
        plot_city_comparison(df, metric)
        
        if metric == "Frequency":
            st.caption(
                "Every year, we count how many heatwaves occurred across all 57 cities and track that number from 1980 to 2025, smoothed with a five-year moving average to see past ordinary weather noise. After three decades holding fairly steady around 10-30 heatwaves a year, frequency breaks sharply upward from the mid-2010s onward, reaching over 100 a year by the end of the decade, a rise confirmed statistically (p < 0.0001) rather than just a visual impression. Ranking cities by their total heatwave count shows the increase isn't concentrated in one region: Münster, Ludwigshafen am Rhein, Munich, and Berlin all sit near the top despite very different climates, suggesting a nationwide pattern rather than a local anomaly."
                )
        if metric == "Peak temperature":
            st.caption(
                "For each detected heatwave we record its hottest single day, then average those peaks per year across all cities, testing whether individual events are getting more extreme over time. The yearly average oscillates between roughly 31°C and 33°C across four decades without settling into a direction, and the regression confirms no statistically reliable trend (p = 0.110). Ranking cities by their average peak instead reveals a geographic rather than temporal pattern: Ludwigshafen am Rhein, Karlsruhe, Mainz, and other Rhine valley cities dominate regardless of how often they experience heatwaves, pointing to climate zone, not long-term warming, as the main driver of intensity."
                )
        if metric == "Average temperature":
            st.caption(
                "This metric takes the mean temperature across each heatwave's full duration, not just its hottest moment, guarding against a single extreme afternoon skewing the intensity picture. Like peak temperature, it shows no meaningful long-term trend (p = 0.253). Heatwaves aren't measurably hotter on average today than in 1980, despite occurring far more often. The city ranking reinforces this: it's led by essentially the same Rhine valley cities as the peak-temperature list (Ludwigshafen, Karlsruhe, Mainz, Frankfurt), evidence that heatwave intensity is shaped mainly by regional climate rather than a warming trend over time."
                )
        if metric == "Duration":
            st.caption(
                "Duration averages the length in days of every detected heatwave per year, again smoothed over a five-year window. Unlike the two temperature metrics, this one shows a real upward trend, confirmed at p = 0.0107: after hovering close to the 3-day minimum for two decades, average duration climbs steadily from around 2010 onward, passing 4.3 days by 2025. That matters beyond the statistics too, since prolonged heat exposure, not a single hot day, drives most heat-related health risk, connecting this result directly to the project's later public-health questions. The cities with the longest-lasting heatwaves (Bremen, Hamburg, Hannover) cluster in the north, a different group from the Rhine valley cities dominating the temperature rankings, suggesting duration is governed by different regional factors than intensity."
                )
        


    st.divider()

    

    st.subheader("Conclusion")

    st.markdown(
        """
        The long-term trend analysis shows that **heatwave frequency** and
        **heatwave duration** increased significantly across German major cities
        between 1980 and 2025.

        No statistically significant increase was observed for **peak temperature**
        or **average heatwave temperature**.
        """
)

    render_trend_statistics(yearly)
    
    st.markdown(
    "**Sensitivity check: 1991–2025**"
    )

    sensitivity = RQ1_TRENDS_1991.copy()

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
    st.caption(
            "A trend is considered statistically significant when p < 0.05."
        )

def render():
    with st.container(key="rq1_page_shell"):
        _render_rq1_content()
