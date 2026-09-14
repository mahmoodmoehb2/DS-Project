"""RQ1 page: are heatwaves in German cities becoming more common?
Loads the heatwave event data, computes yearly trends, and renders
the charts and tables for the Streamlit page."""

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

# Column names and chart labels for each heatwave metric.
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


# Pre-computed trend stats for the 1991-2025 sensitivity check.
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
    """Load the heatwave event table from the CSV file.
    Also parses the date columns and adds a year column if missing.
    Returns None if the file does not exist."""
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
    """Check that the event table has all the columns we need.
    Returns the set of missing column names, empty if nothing is missing."""
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


def build_yearly(df, start_year=ANALYSIS_START, end_year=ANALYSIS_END):
    """Group the events by year and compute yearly averages.
    Fills in missing years and adds a smoothed 5-year rolling average
    for each metric, so the trend lines look less noisy."""
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
        {"year": range(start_year, end_year + 1)}
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
    """Run a linear regression on one metric over the years.
    Returns the slope, p-value, and whether the trend is significant.
    Returns None if there are fewer than 3 valid data points."""
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
    """Calculate the trend for every metric in METRICS.
    Returns a table with one row per metric, ready to display."""
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
    """Draw a line chart of the smoothed metric over time.
    Plots the yearly trend for one metric, like frequency or duration."""
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


def plot_city_comparison(df, metric, start_year=None, end_year=None):
    """Draw a bar chart comparing cities on one metric.
    Shows the top 15 cities, sorted from highest to lowest value."""
    if metric == "Frequency":
        city_df = (
            df.groupby("city")
            .size()
            .reset_index(name="value")
            .sort_values("value", ascending=False)
        )
        if start_year is not None and end_year is not None:
            y_title = f"Detected heatwaves, {start_year}–{end_year}"
        else:
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
    """Show the trend statistics as a table on the page.
    Formats the numbers nicely before displaying them."""
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
    """Show four quick summary numbers at the top of the page.
    These are the city count, event count, year range, and definition."""
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
    """Show the study design and heatwave definition side by side."""
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
    """Build the whole RQ1 page.
    Loads the data, shows the filters, and draws the charts and tables."""
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

    yearly = build_yearly(
        df,
        start_year=ANALYSIS_START,
        end_year=ANALYSIS_END,
    )
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

    st.markdown(
        "Change the analysis period, select individual cities, and switch "
        "between heatwave metrics. The charts update automatically."
    )

    selected_years = st.slider(
        "Select analysis period",
        min_value=ANALYSIS_START,
        max_value=ANALYSIS_END,
        value=(ANALYSIS_START, ANALYSIS_END),
        step=1,
        key="rq1_year_range",
    )
    start_year, end_year = selected_years

    all_cities = sorted(df["city"].dropna().unique().tolist())

    selected_cities = st.multiselect(
        "Select cities",
        options=all_cities,
        default=[],
        placeholder="Leave empty to include all cities",
        key="rq1_city_filter",
    )

    active_cities = selected_cities if selected_cities else all_cities

    metric = st.segmented_control(
        "Select heatwave metric",
        options=[
            "Frequency",
            "Duration",
        ],
        default="Frequency",
        key="rq1_metric",
    )

    if metric is None:
        metric = "Frequency"

    df_filtered = df[
        df["year"].between(start_year, end_year, inclusive="both")
        & df["city"].isin(active_cities)
    ].copy()

    yearly_filtered = build_yearly(
        df_filtered,
        start_year=start_year,
        end_year=end_year,
    )

    if selected_cities:
        if len(active_cities) == 1:
            scope_label = "1 selected city"
        else:
            scope_label = f"{len(active_cities)} selected cities"
    else:
        scope_label = f"all {len(all_cities)} cities"

    st.caption(
        f"Current selection: {start_year}-{end_year} · {scope_label}"
    )

    tab1, tab2 = st.tabs(
        [
            "Long-term trend",
            "City comparison",
        ]
    )

    with tab1:
        st.markdown(f"#### Development from {start_year} to {end_year}")
        plot_yearly_trend(yearly_filtered, metric)

        trend = calculate_trend(yearly_filtered, metric)

        if trend is not None:
            p_text = (
                "<0.0001"
                if trend["p_value"] < 0.0001
                else f"{trend['p_value']:.4f}"
            )
            significance_text = (
                "statistically significant"
                if trend["significant"]
                else "not statistically significant"
            )

            
        else:
            st.caption(
                "Not enough annual observations are available to calculate "
                "a reliable trend for the current selection."
            )

    with tab2:
        st.markdown("#### Comparison between cities")
        plot_city_comparison(
            df_filtered,
            metric,
            start_year=start_year,
            end_year=end_year,
        )

        if df_filtered.empty:
            st.caption(
                "No heatwave events are available for the current selection."
            )


    st.divider()

    

    st.subheader("Conclusion")

    st.markdown(
        """
        We also checked if these results hold up when we remove the years that overlap with the reference period, leaving only 1991–2025. Frequency and duration stay significant either way, so these are solid findings. Peak temperature is different: it's not significant over the full 45 years, but it is significant in the shorter window. This points to a real warming trend that's just harder to detect when the noisier early years are included. Average temperature stays non-significant in both cases.
        """
)

    render_trend_statistics(yearly)
    
    st.markdown(
    "**Sensitivity check: 1991-2025**"
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
    """Entry point for the RQ1 page, called by the main app."""
    with st.container(key="rq1_page_shell"):
        _render_rq1_content()
