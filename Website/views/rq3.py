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
        ("Average Peak Temperature", 0.016, 0.1854, False),
        ("Average Temperature", 0.004, 0.6896, False),
        ("Average Duration", 0.039, 0.0000, True),
    ],
    columns=["metric", "slope", "p_value", "significant"],
)

EUROPE_TRENDS_1991 = pd.DataFrame(
    [
        ("Frequency", 5.015, 0.0000, True),
        ("Average Peak Temperature", 0.032, 0.0566, False),
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
        "Average Peak temperature": (
            "avg_max_temp_smooth",
            "Average peak temperature (°C)",
            "Average peak temperature of detected heatwaves",
        ),
        "Average temperature": (
            "avg_avg_temp_smooth",
            "Average heatwave temperature (°C)",
            "Average temperature within detected heatwaves",
        ),
        "Average Duration": (
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
        "Average Peak Temperature": "°C/year",
        "Average Temperature": "°C/year",
        "Average Duration": "days/year",
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

    if metric == "Average Peak temperature":
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
        f"**Research question:** {RQ_META['rq3']['title']}"
        )
    
    st.subheader("How the analysis works")
    render_method()

    

    st.write("")
    st.subheader("Explore the results")

    metric = st.segmented_control(
        "Metric",
        [
            "Frequency",
            "Average Peak temperature",
            "Average temperature",
            "Average Duration",
        ],
        default="Frequency",
        key="rq3_metric",
    )

    if metric is None:
        metric = "Frequency"

    events = load_events()
    yearly = build_yearly(events)

    country_df = load_country_trends()

    tab1, tab2 = st.tabs(
        [
            "Long-term trend",
            "Country comparison",
        ]
    )

    with tab1:
        render_yearly_chart(
            yearly,
            metric,
        )
        
        if metric == "Frequency":
            st.caption(
                "This chart counts, year by year, how many heatwaves were detected across the 99 European cities, then applies a five-year moving average to make the underlying direction visible against normal fluctuation. What started in the low double digits in 1980 climbs past 200 a year by 2025, and the regression backs this up for both the full 1980–2025 window and the narrower 1991–2025 check (p < 0.0001 in each case). Identifying which country drove this hardest works differently from a simple ranking: each city gets its own frequency slope, and the country score is the median across its cities, with countries below 3 cities dropped as too thin to trust. Italy comes out on top at +0.068 additional heatwaves per city each year, narrowly ahead of Ukraine and Spain, while Germany and the UK sit noticeably lower."
                )
        if metric == "Average Peak temperature":
            st.caption(
                "Here the metric is the single hottest day within each detected heatwave, averaged per year and smoothed the same way as frequency. The line drifts between about 32.5°C and 34.5°C for most of the timeline with a late uptick after 2020, but neither regression comes back significant: not for the full period (p = 0.185), and not even for the shorter 1991–2025 window (p = 0.057, just missing the 0.05 cutoff). Because the notebook only builds a country-level trend for average temperature and not for peak temperature specifically, this tab falls back to showing the frequency ranking instead, with an explanatory note rather than silently substituting one metric for another."
                )
        if metric == "Average temperature":
            st.caption(
                "Instead of just the hottest day, this metric averages every day within a heatwave's full span, so a single spike can't distort how intense the event felt overall. It mirrors peak temperature in showing no statistically meaningful trend (p = 0.690). Building the country ranking here first drops cities with fewer than 10 years containing at least one heatwave, since a slope from a handful of points isn't trustworthy. The UK sits highest at +0.036°C/year, but that number comes from exactly one city and is marked gray to signal it shouldn't be read the same way as the others; among countries with real coverage, Germany edges out Italy and Ukraine."
                )
        if metric == "Average Duration":
            st.caption(
                "Duration tracks how many days each detected heatwave lasted, averaged per year and smoothed like the other three metrics. This is the one metric that does move in a clear direction, confirmed at p < 0.0001 in both the full-period and 1991–2025 checks, rising from under 4 days in the early record to past 5.5 days by 2025. Italy again sits at the top of the country ranking (+0.052 days/year), roughly three times the rate of France, Germany, and Spain just behind it. Ukraine and Poland actually post small negative slopes here, meaning their heatwaves multiplied without stretching out any longer."
                )
        
            
        

    with tab2:
        render_country_comparison(
            country_df,
            metric,
        )
        
        if metric == "Frequency":
            st.caption(
                "This chart counts, year by year, how many heatwaves were detected across the 99 European cities, then applies a five-year moving average to make the underlying direction visible against normal fluctuation. What started in the low double digits in 1980 climbs past 200 a year by 2025, and the regression backs this up for both the full 1980–2025 window and the narrower 1991–2025 check (p < 0.0001 in each case). Identifying which country drove this hardest works differently from a simple ranking: each city gets its own frequency slope, and the country score is the median across its cities, with countries below 3 cities dropped as too thin to trust. Italy comes out on top at +0.068 additional heatwaves per city each year, narrowly ahead of Ukraine and Spain, while Germany and the UK sit noticeably lower."
                )
        if metric == "Average Peak temperature":
            st.caption(
                "Here the metric is the single hottest day within each detected heatwave, averaged per year and smoothed the same way as frequency. The line drifts between about 32.5°C and 34.5°C for most of the timeline with a late uptick after 2020, but neither regression comes back significant: not for the full period (p = 0.185), and not even for the shorter 1991–2025 window (p = 0.057, just missing the 0.05 cutoff). Because the notebook only builds a country-level trend for average temperature and not for peak temperature specifically, this tab falls back to showing the frequency ranking instead, with an explanatory note rather than silently substituting one metric for another."
                )
        if metric == "Average temperature":
            st.caption(
                "Instead of just the hottest day, this metric averages every day within a heatwave's full span, so a single spike can't distort how intense the event felt overall. It mirrors peak temperature in showing no statistically meaningful trend (p = 0.690). Building the country ranking here first drops cities with fewer than 10 years containing at least one heatwave, since a slope from a handful of points isn't trustworthy. The UK sits highest at +0.036°C/year, but that number comes from exactly one city and is marked gray to signal it shouldn't be read the same way as the others; among countries with real coverage, Germany edges out Italy and Ukraine."
                )
        if metric == "Average Duration":
            st.caption(
                "Duration tracks how many days each detected heatwave lasted, averaged per year and smoothed like the other three metrics. This is the one metric that does move in a clear direction, confirmed at p < 0.0001 in both the full-period and 1991–2025 checks, rising from under 4 days in the early record to past 5.5 days by 2025. Italy again sits at the top of the country ranking (+0.052 days/year), roughly three times the rate of France, Germany, and Spain just behind it. Ukraine and Poland actually post small negative slopes here, meaning their heatwaves multiplied without stretching out any longer."
                )
            

    st.markdown("---")

    with st.expander("Statistical note"):
                st.markdown(
                    """
                    Das kommt...
                    """
                )
    
    st.subheader("Conclusion")

    st.markdown(
        """
        Across the studied European cities, **heatwave frequency increased
        significantly between 1980 and 2025**, with approximately four additional
        heatwave events per year across the analysed cities.

        **Heatwave duration also increased significantly**, while neither peak
        temperature nor average heatwave temperature showed a statistically
        significant long-term trend.

        At the country level, **Italy showed the strongest median increase in
        heatwave frequency** among countries with sufficient city-level data,
        followed by Ukraine and Spain.

        Overall, the results indicate that the clearest long-term changes across
        European cities are an increase in **how often heatwaves occur and how long
        they last**, rather than a significant increase in their average intensity.
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
        Heatwaves were identified for **1980–2025** using a city-specific
        **98th-percentile temperature threshold** based on the **1961–1990
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
