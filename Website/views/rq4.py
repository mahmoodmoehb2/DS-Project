from pathlib import Path

import pandas as pd
import streamlit as st

from theme import key_finding

try:
    import plotly.express as px
except ImportError:
    px = None


# -------------------------------------------------------------------
# RQ4 – Italy: city-size comparison
# -------------------------------------------------------------------

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
    "large": 25,
    "medium": 24,
    "small": 24,
    "rural": 25,
}

SUMMARY = pd.DataFrame(
    {
        "size_class": ["large", "medium", "small", "rural"],
        "n_places": [25, 24, 24, 25],
        "total_heatwaves": [1719, 1701, 1688, 1646],
        "heatwaves_per_place_year": [1.495, 1.541, 1.529, 1.431],
        "mean_peak_temp": [34.388, 34.328, 34.389, 33.925],
        "mean_avg_temp": [33.200, 33.133, 33.202, 32.776],
        "mean_duration": [5.156, 5.300, 5.205, 5.147],
    }
)

TREND_STATS = pd.DataFrame(
    [
        ("large", "Frequency", 0.0716, 0.0000, True),
        ("large", "Peak temperature", 0.0336, 0.0451, True),
        ("large", "Average temperature", 0.0192, 0.1694, False),
        ("large", "Duration", 0.0561, 0.0001, True),

        ("medium", "Frequency", 0.0783, 0.0000, True),
        ("medium", "Peak temperature", 0.0117, 0.4856, False),
        ("medium", "Average temperature", 0.0008, 0.9547, False),
        ("medium", "Duration", 0.0598, 0.0000, True),

        ("small", "Frequency", 0.0750, 0.0000, True),
        ("small", "Peak temperature", 0.0188, 0.2538, False),
        ("small", "Average temperature", 0.0069, 0.6152, False),
        ("small", "Duration", 0.0558, 0.0001, True),

        ("rural", "Frequency", 0.0676, 0.0000, True),
        ("rural", "Peak temperature", -0.0070, 0.6644, False),
        ("rural", "Average temperature", -0.0149, 0.3023, False),
        ("rural", "Duration", 0.0554, 0.0002, True),
    ],
    columns=["size_class", "metric", "slope", "p_value", "significant"],
)


@st.cache_data
def load_events():
    """Load the event-level CSV exported by the Italy notebook."""
    path = DATA_DIR / "RQ4_Italy_heatwaves_events.csv"
    if not path.exists():
        return None

    df = pd.read_csv(path)

    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"], errors="coerce")
        if "year" not in df.columns:
            df["year"] = df["start"].dt.year

    return df


def build_yearly(events):
    if events is None or events.empty:
        return None

    required = {
        "year",
        "size_class",
        "max_temp",
        "avg_temp",
        "duration_days",
    }
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

    yearly = all_years.merge(
        yearly,
        on=["year", "size_class"],
        how="left",
    )

    yearly["n_heatwaves"] = yearly["n_heatwaves"].fillna(0)
    yearly["heatwaves_per_place"] = yearly.apply(
        lambda row: row["n_heatwaves"] / N_PLACES[row["size_class"]],
        axis=1,
    )

    for column in [
        "heatwaves_per_place",
        "mean_max_temp",
        "mean_avg_temp",
        "mean_duration",
    ]:
        yearly[f"{column}_smooth"] = (
            yearly.groupby("size_class", observed=False)[column]
            .transform(
                lambda s: s.rolling(
                    5,
                    min_periods=1,
                    center=True,
                ).mean()
            )
        )

    return yearly


def _themed_layout(fig, height, y_title, x_title=""):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="-apple-system, Segoe UI, Roboto, sans-serif",
            color="#1F2937",
            size=13,
        ),
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend=dict(
            title="City size",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#EDE9FE", zeroline=False)
    return fig


def render_summary_cards():
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Places analysed", "98")
    c2.metric("Analysis period", "1980–2025")
    c3.metric("City-size classes", "4")
    c4.metric("Heatwave definition", "≥ 3 days")


def render_overview_chart(metric):
    metric_config = {
        "Frequency": (
            "heatwaves_per_place_year",
            "Average heatwaves per place per year",
        ),
        "Peak temperature": (
            "mean_peak_temp",
            "Average peak temperature (°C)",
        ),
        "Average temperature": (
            "mean_avg_temp",
            "Average heatwave temperature (°C)",
        ),
        "Duration": (
            "mean_duration",
            "Average heatwave duration (days)",
        ),
    }

    column, y_title = metric_config[metric]

    chart_df = SUMMARY.copy()
    chart_df["City size"] = chart_df["size_class"].map(CLASS_LABELS)

    if px is None:
        st.bar_chart(
            chart_df.set_index("City size")[column],
            use_container_width=True,
        )
        return

    fig = px.bar(
        chart_df,
        x="City size",
        y=column,
        text=column,
        color="City size",
        color_discrete_map=CLASS_COLORS,
        category_orders={
            "City size": [CLASS_LABELS[c] for c in CLASS_ORDER]
        },
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont=dict(color="#1F2937"),
        cliponaxis=False,
        marker_line_width=0,
    )

    _themed_layout(fig, height=430, y_title=y_title)
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)


def render_trend_chart(yearly, metric):
    metric_config = {
        "Frequency": (
            "heatwaves_per_place_smooth",
            "Average heatwaves per place per year",
        ),
        "Peak temperature": (
            "mean_max_temp_smooth",
            "Average peak temperature (°C)",
        ),
        "Average temperature": (
            "mean_avg_temp_smooth",
            "Average heatwave temperature (°C)",
        ),
        "Duration": (
            "mean_duration_smooth",
            "Average heatwave duration (days)",
        ),
    }

    column, y_title = metric_config[metric]

    plot_df = yearly.copy()
    plot_df["City size"] = plot_df["size_class"].map(CLASS_LABELS)

    if px is None:
        pivot = plot_df.pivot(
            index="year",
            columns="City size",
            values=column,
        )
        st.line_chart(pivot, use_container_width=True)
        return

    fig = px.line(
        plot_df,
        x="year",
        y=column,
        color="City size",
        color_discrete_map=CLASS_COLORS,
        category_orders={
            "City size": [CLASS_LABELS[c] for c in CLASS_ORDER]
        },
    )

    fig.update_traces(
        line=dict(width=3),
        hovertemplate="%{y:.2f}<extra>%{fullData.name}</extra>",
    )

    _themed_layout(
        fig,
        height=500,
        y_title=y_title,
        x_title="Year",
    )
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(dtick=5)

    st.plotly_chart(fig, use_container_width=True)


def render_trend_table(metric):
    table = TREND_STATS[TREND_STATS["metric"] == metric].copy()

    table["City size"] = table["size_class"].map(CLASS_LABELS)
    table["Trend per year"] = table["slope"].map(lambda x: f"{x:+.4f}")
    table["p-value"] = table["p_value"].map(
        lambda x: "<0.0001" if x == 0 else f"{x:.4f}"
    )
    table["Significant"] = table["significant"].map(
        {True: "Yes", False: "No"}
    )

    top = st.columns([5, 1])
    with top[1]:
        st.download_button(
            "⬇️ Download data",
            data=TREND_STATS.to_csv(index=False).encode("utf-8"),
            file_name="RQ4_italy_trend_statistics.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(
        table[
            [
                "City size",
                "Trend per year",
                "p-value",
                "Significant",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )


def _render_rq4_content():
    st.markdown(
        '<div class="eyebrow">RQ4 · HEATWAVES · ITALY</div>',
        unsafe_allow_html=True,
    )

    st.title("Are rising heatwave trends limited to large cities in Italy?")

    st.markdown(
        """
        **Research question:** In the European country most strongly affected by
        rising heatwave trends, does this effect concentrate in large cities,
        or is it equally present in smaller cities and rural municipalities?
        """
    )

    render_summary_cards()

    st.write("")
    key_finding(
        "Italy was identified as the European country most strongly affected by rising "
        "heatwave trends. Since 1980, heatwave frequency (~+0.07/year) and duration "
        "(~+0.06 days/year) have increased significantly across all city sizes. "
        "Thus, rising heatwave trends are not limited to large cities."
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
        key="rq4_metric",
    )

    if metric is None:
        metric = "Frequency"

    tab1, tab2, tab3 = st.tabs(
        [
            "Long-term trend",
            "Overall comparison",
            "Trend statistics",
        ]
    )

    events = load_events()
    yearly = build_yearly(events)

    with tab1:
        st.markdown("#### Development from 1980 to 2025")
        st.caption(
            "Lines show a centered 5-year moving average for each city-size class."
        )

        if yearly is not None:
            render_trend_chart(yearly, metric)
        else:
            st.info(
                "Add `RQ4_Italy_heatwaves_events.csv` to the `data/` folder "
                "to display the interactive yearly trend chart."
            )

        if metric == "Frequency":
            st.markdown(
                "**Interpretation:** Heatwave frequency increased significantly "
                "in all four city-size classes."
            )
        elif metric == "Duration":
            st.markdown(
                "**Interpretation:** Heatwave duration increased significantly "
                "in all four city-size classes."
            )
        elif metric == "Peak temperature":
            st.markdown(
                "**Interpretation:** Peak temperature increased significantly "
                "only in large cities over 1980–2025."
            )
        else:
            st.markdown(
                "**Interpretation:** The long-term trend in average heatwave "
                "temperature was not statistically significant in any city-size class."
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
        st.caption(
            "A result is treated as statistically significant when p < 0.05."
        )
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
            Across the full 1980–2025 period, Kruskal–Wallis tests found no
            statistically significant overall differences between the four
            city-size classes for frequency (p=0.8203), peak temperature
            (p=0.4404), average temperature (p=0.6116), or duration (p=0.8606).

            The strongest result is therefore the **shared long-term change**:
            heatwave frequency and duration rise significantly across all city sizes,
            rather than the increase being concentrated only in large cities.
            """
        )

    with st.expander("Methodological note for Italy"):
        st.markdown(
            """
            Italy does not use the same legal city-status distinction as Germany.
            Therefore, the Italian size classes are defined **only by population**,
            while keeping the same population thresholds as the Germany analysis.

            The heatwave definition is intentionally unchanged so that Germany and
            Italy remain methodologically comparable.
            """
        )


def render():
    # Same schema as RQ2: a dedicated page wrapper with a stable Streamlit key.
    # The theme can target this page specifically via `.st-key-rq4_page_shell`.
    with st.container(key="rq4_page_shell"):
        _render_rq4_content()
