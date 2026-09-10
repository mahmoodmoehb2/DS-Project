from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px





DATA_DIR = Path(__file__).resolve().parents[1] / "data"

COUNTRY_TRENDS_FILE = DATA_DIR / "RQ3_country_trends.csv"
EVENT_FILE = DATA_DIR / "RQ3_heatwaves_events.csv"

ANALYSIS_START = 1980
ANALYSIS_END = 2025




EUROPE_TRENDS = pd.DataFrame(
    [
        ("Frequency", 3.995, 0.0000, True),
        ("Peak temperature", 0.016, 0.1854, False),
        ("Average temperature", 0.004, 0.6896, False),
        ("Duration", 0.039, 0.0000, True),
    ],
    columns=["metric", "slope", "p_value", "significant"],
)

EUROPE_TRENDS_1991 = pd.DataFrame(
    [
        ("Frequency", 5.015, 0.0000, True),
        ("Peak temperature", 0.032, 0.0566, False),
        ("Average temperature", 0.015, 0.3058, False),
        ("Duration", 0.046, 0.0000, True),
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



def build_yearly(events):
    if events is None or events.empty:
        return None

    required = {"year", "max_temp", "avg_temp", "duration_days"}

    if not required.issubset(events.columns):
        return None

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
        {"year": range(ANALYSIS_START, ANALYSIS_END + 1)}
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
            "Average peak temperature (°C)",
            "Average peak temperature of detected heatwaves",
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

    st.caption(
        "Centered 5-year moving average."
    )


def render_europe_trend_summary(metric):
    row = EUROPE_TRENDS[
        EUROPE_TRENDS["metric"] == metric
    ].iloc[0]

    unit = {
        "Frequency": "heatwaves/year",
        "Peak temperature": "°C/year",
        "Average temperature": "°C/year",
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
        "Duration": (
            "duration_slope",
            "n_cities_duration",
            "Median duration change (days/year)",
        ),
    }

    if metric == "Peak temperature":
        st.info(
            "The notebook's country-level comparison uses average "
            "heatwave temperature rather than peak temperature. "
            "The frequency ranking is shown here instead."
        )

        metric = "Frequency"

    value_col, n_col, y_label = config[metric]

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

    if metric == "Frequency":
        st.caption(
            "Italy shows the strongest median city-level increase "
            "in heatwave frequency, followed by Ukraine and Spain."
        )

    elif metric in {
        "Duration",
        "Average temperature",
    }:
        st.caption(
            "For duration and temperature, cities with fewer than "
            "10 years containing heatwaves were excluded from the "
            "city-level regression."
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

**Analysis period.** 1980–2025.

**Reference period.** 1961–1990.

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
        """
**Research question:** How have the frequency, intensity, and duration
of heatwaves in major European cities (≥500,000 inhabitants or national
capitals) changed between 1980 and today — and which country is most
strongly affected?
        """
    )

    


    st.markdown("---")

    metric = st.segmented_control(
        "Metric",
        [
            "Frequency",
            "Peak temperature",
            "Average temperature",
            "Duration",
        ],
        default="Frequency",
        key="rq3_metric",
    )

    if metric is None:
        metric = "Frequency"

    events = load_events()
    yearly = build_yearly(events)

    country_df = load_country_trends()

    tab1, tab2, tab3 = st.tabs(
        [
            "Long-term trend",
            "Country comparison",
            "Trend statistics",
        ]
    )

    with tab1:
        render_yearly_chart(
            yearly,
            metric,
        )

    with tab2:
        render_country_comparison(
            country_df,
            metric,
        )

    with tab3:
        render_trend_statistics()

    st.markdown("---")

    st.subheader(
        "Conclusion"
    )

    st.markdown(
        """
The European analysis shows a clear change in **how often heatwaves
occur and how long they last**, rather than a statistically reliable
increase in the temperature of already-detected heatwaves.

Italy ranks first for the median increase in heatwave frequency across
its studied cities, with Ukraine and Spain following behind.

This result motivates RQ4, which examines whether Italy's increasing
heatwave trends are concentrated in large cities or are also present in
medium-sized, small and rural places.
        """
    )

    with st.expander(
        "Methods and data"
    ):
        render_method()

        st.caption(
            "Website summary values and country trends are based on "
            "the executed `RQ3 FINAL.ipynb` notebook."
        )

        st.caption(
            f"Event file: `{EVENT_FILE.name}`"
        )

        st.caption(
            f"Country trend file: `{COUNTRY_TRENDS_FILE.name}`"
        )



def render():
    with st.container(
        key="rq3_page_shell"
    ):
        _render_rq3_content()
