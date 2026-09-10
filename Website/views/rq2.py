from pathlib import Path

import pandas as pd
import streamlit as st



try:
    import plotly.express as px
except ImportError:
    px = None


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

CLASS_ORDER = ["large", "medium", "small", "rural"]

CLASS_LABELS = {
    "large": "Large city (≥150,000)",
    "medium": "Medium-sized city (20,000–149,999)",
    "small": "Small town (5,000–19,999)",
    "rural": "Rural municipality (1–4,999)",
}


CLASS_COLORS = {
    CLASS_LABELS["large"]: "#2a78d6",
    CLASS_LABELS["medium"]: "#eb6834",
    CLASS_LABELS["small"]: "#1baf7a",
    CLASS_LABELS["rural"]: "#eda100",
}

N_PLACES = {
    "large": 56,
    "medium": 53,
    "small": 44,
    "rural": 42,
}

SUMMARY = pd.DataFrame(
    {
        "size_class": ["large", "medium", "small", "rural"],
        "n_places": [56, 53, 44, 42],
        "total_heatwaves": [1570, 1443, 1138, 1095],
        "heatwaves_per_place_year": [0.609, 0.592, 0.562, 0.567],
        "mean_peak_temp": [32.959, 32.857, 32.716, 32.587],
        "mean_avg_temp": [31.522, 31.420, 31.352, 31.241],
        "mean_duration": [4.018, 3.999, 3.977, 3.986],
    }
)

TREND_STATS = pd.DataFrame(
    [
        ("large", "Frequency", 0.0326, 0.0000, True),
        ("large", "Peak temperature", 0.0394, 0.1100, False),
        ("large", "Average temperature", 0.0214, 0.2532, False),
        ("large", "Duration", 0.0280, 0.0107, True),

        ("medium", "Frequency", 0.0320, 0.0000, True),
        ("medium", "Peak temperature", 0.0359, 0.1637, False),
        ("medium", "Average temperature", 0.0190, 0.3333, False),
        ("medium", "Duration", 0.0246, 0.0329, True),

        ("small", "Frequency", 0.0288, 0.0000, True),
        ("small", "Peak temperature", 0.0249, 0.2983, False),
        ("small", "Average temperature", 0.0148, 0.4318, False),
        ("small", "Duration", 0.0205, 0.0784, False),

        ("rural", "Frequency", 0.0304, 0.0000, True),
        ("rural", "Peak temperature", 0.0298, 0.2014, False),
        ("rural", "Average temperature", 0.0197, 0.2848, False),
        ("rural", "Duration", 0.0153, 0.1922, False),
    ],
    columns=["size_class", "metric", "slope", "p_value", "significant"],
)


@st.cache_data
def load_events():
    """Load the event-level CSV exported by RQ2_final.ipynb (section 18)."""
    path = DATA_DIR / "RQ2_heatwaves_events.csv"
    if not path.exists():
        return None

    df = pd.read_csv(path)

    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"], errors="coerce")
        if "year" not in df.columns:
            df["year"] = df["start"].dt.year

    return df


def build_yearly(events):
    """
    Recreate the yearly city-size series from the exported event table.

    The notebook uses the number of places with weather data as denominator.
    For the website we use the known number of unique places per class.
    """
    if events is None or events.empty:
        return None

    required = {"year", "size_class", "max_temp", "avg_temp", "duration_days"}
    if not required.issubset(events.columns):
        return None

    yearly = (
        events.groupby(["year", "size_class"], observed=False)
        .agg(
            n_heatwaves=("year", "size"),
            mean_max_temp=("max_temp", "mean"),
            mean_avg_temp=("avg_temp", "mean"),
            mean_duration=("duration_days", "mean"),
        )
        .reset_index()
    )

    all_years = pd.MultiIndex.from_product(
        [range(1980, 2026), CLASS_ORDER],
        names=["year", "size_class"],
    ).to_frame(index=False)

    yearly = all_years.merge(yearly, on=["year", "size_class"], how="left")

    yearly["n_heatwaves"] = yearly["n_heatwaves"].fillna(0)
    yearly["heatwaves_per_place"] = yearly.apply(
        lambda row: row["n_heatwaves"] / N_PLACES[row["size_class"]],
        axis=1,
    )

    for column in ["heatwaves_per_place", "mean_max_temp", "mean_avg_temp", "mean_duration"]:
        yearly[f"{column}_smooth"] = yearly.groupby("size_class", observed=False)[column].transform(
            lambda s: s.rolling(5, min_periods=1, center=True).mean()
        )

    return yearly


def _themed_layout(fig, height, y_title, x_title=""):
    """Shared Plotly styling so every chart on this page reads as one
    system: transparent surface (blends into the page), muted gridlines,
    the app's sans-serif font, legend without its own box."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="-apple-system, Segoe UI, Roboto, sans-serif", color="#1F2937", size=13),
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend=dict(title="City size", orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#EDE9FE", zeroline=False)
    return fig


def render_summary_cards():
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Places analysed", "195")
    c2.metric("Analysis period", "1980–2025")
    c3.metric("City-size classes", "4")
    c4.metric("Heatwave definition", "≥ 3 days")


def render_overview_chart(metric):
    metric_config = {
        "Frequency": ("heatwaves_per_place_year", "Average heatwaves per place per year"),
        "Peak temperature": ("mean_peak_temp", "Average peak temperature (°C)"),
        "Average temperature": ("mean_avg_temp", "Average heatwave temperature (°C)"),
        "Duration": ("mean_duration", "Average heatwave duration (days)"),
    }

    column, y_title = metric_config[metric]

    chart_df = SUMMARY.copy()
    chart_df["City size"] = chart_df["size_class"].map(CLASS_LABELS)

    if px is None:
        st.bar_chart(chart_df.set_index("City size")[column], use_container_width=True)
        return

    fig = px.bar(
        chart_df,
        x="City size",
        y=column,
        text=column,
        color="City size",
        color_discrete_map=CLASS_COLORS,
        category_orders={"City size": [CLASS_LABELS[c] for c in CLASS_ORDER]},
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont=dict(color="#1F2937"),
        cliponaxis=False,
        marker_line_width=0,
    )

    _themed_layout(fig, height=430, y_title=y_title)
    fig.update_layout(showlegend=False)  # single bar per class already labeled on the x-axis

    st.plotly_chart(fig, use_container_width=True)


def render_trend_chart(yearly, metric):
    metric_config = {
        "Frequency": ("heatwaves_per_place_smooth", "Average heatwaves per place per year"),
        "Peak temperature": ("mean_max_temp_smooth", "Average peak temperature (°C)"),
        "Average temperature": ("mean_avg_temp_smooth", "Average heatwave temperature (°C)"),
        "Duration": ("mean_duration_smooth", "Average heatwave duration (days)"),
    }

    column, y_title = metric_config[metric]

    plot_df = yearly.copy()
    plot_df["City size"] = plot_df["size_class"].map(CLASS_LABELS)

    if px is None:
        pivot = plot_df.pivot(index="year", columns="City size", values=column)
        st.line_chart(pivot, use_container_width=True)
        return

    fig = px.line(
        plot_df,
        x="year",
        y=column,
        color="City size",
        color_discrete_map=CLASS_COLORS,
        category_orders={"City size": [CLASS_LABELS[c] for c in CLASS_ORDER]},
    )

    fig.update_traces(line=dict(width=3), hovertemplate="%{y:.2f}<extra>%{fullData.name}</extra>")

    _themed_layout(fig, height=500, y_title=y_title, x_title="Year")
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(dtick=5)

    st.plotly_chart(fig, use_container_width=True)


def render_trend_table(metric):
    table = TREND_STATS[TREND_STATS["metric"] == metric].copy()

    table["City size"] = table["size_class"].map(CLASS_LABELS)
    table["Trend per year"] = table["slope"].map(lambda x: f"{x:+.4f}")
    table["p-value"] = table["p_value"].map(lambda x: "<0.0001" if x == 0 else f"{x:.4f}")
    table["Significant"] = table["significant"].map({True: "Yes", False: "No"})

    top = st.columns([5, 1])
    with top[1]:
        st.download_button(
            "⬇️ Download data",
            data=TREND_STATS.to_csv(index=False).encode("utf-8"),
            file_name="RQ2_trend_statistics.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(
        table[["City size", "Trend per year", "p-value", "Significant"]],
        hide_index=True,
        use_container_width=True,
    )


def _render_rq2_content():
    st.markdown('<div class="eyebrow">RQ2 · HEATWAVES · GERMANY</div>', unsafe_allow_html=True)

    st.title("Do heatwaves differ by city size in Germany?")

    st.markdown(
        """
        **Research question:** How do heatwave frequency, intensity
        (peak and average temperature), and duration differ across city sizes,
        from large cities to rural municipalities, within the same region
        in Germany?
        """
    )

    



    st.write("")
    st.subheader("Explore the results")

    metric = st.segmented_control(
        "Metric",
        options=["Frequency", "Peak temperature", "Average temperature", "Duration"],
        default="Frequency",
        key="rq2_metric",
    )

    if metric is None:
        metric = "Frequency"

    tab1, tab2, tab3 = st.tabs(["Long-term trend", "Overall comparison", "Trend statistics"])

    events = load_events()
    yearly = build_yearly(events)

    with tab1:
        st.markdown("#### Development from 1980 to 2025")
        st.caption("Lines show a centered 5-year moving average for each city-size class.")

        if yearly is not None:
            render_trend_chart(yearly, metric)
        else:
            st.info(
                "Add `RQ2_heatwaves_events.csv` to the `data/` folder "
                "to display the interactive yearly trend chart."
            )

        if metric == "Frequency":
            st.markdown(
                "**Interpretation:** The increase in heatwave frequency is "
                "statistically significant in all four city-size classes."
            )
        elif metric == "Duration":
            st.markdown(
                "**Interpretation:** Heatwave duration increased significantly "
                "in large and medium-sized cities, but not in small towns or "
                "rural municipalities."
            )
        else:
            st.markdown(
                "**Interpretation:** The observed long-term increase is not "
                "statistically significant at the 5% level."
            )

    with tab2:
        st.markdown("#### Average values across the full analysis period")
        st.caption(
            "The comparison uses unique places so that municipalities shared by "
            "multiple large-city regions are not counted more than once."
        )
        render_overview_chart(metric)

    with tab3:
        st.markdown("#### Linear trend statistics, 1980–2025")
        st.caption("A result is treated as statistically significant when p < 0.05.")
        render_trend_table(metric)

    st.divider()

    st.subheader("How the comparison works")

    method_left, method_right = st.columns(2)

    with method_left:
        st.markdown(
            """
            **City-size classes**

            - Large city: ≥150,000 inhabitants
            - Medium-sized city: 20,000–149,999
            - Small town: 5,000–19,999
            - Rural municipality: 1,000–4,999
            """
        )

    with method_right:
        st.markdown(
            """
            **Heatwave definition**

            At least **3 consecutive days** above the location-specific
            **98th-percentile temperature threshold** and above **28°C**.

            Reference period: **1961–1990**
            Analysis period: **1980–2025**
            """
        )

    with st.expander("Statistical note"):
        st.markdown(
            """
            The notebook also compares the four city-size classes using
            Kruskal–Wallis tests. Across the full 1980–2025 period, the
            differences between size classes were **not statistically
            significant** for frequency (p=0.4444), peak temperature
            (p=0.0513), average temperature (p=0.1935), or duration
            (p=0.6640).

            This means the strongest result is the **change over time**:
            heatwaves are becoming more frequent across all city sizes,
            rather than the overall averages being dramatically different
            between the four classes.
            """
        )


def render():
    with st.container(key="rq2_page_shell"):
        _render_rq2_content()
