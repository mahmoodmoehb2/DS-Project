from pathlib import Path
import pandas as pd
import streamlit as st
from content import RQ_META


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


def build_yearly(events, start_year=1980, end_year=2025, selected_classes=None):
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

    active_classes = selected_classes if selected_classes else CLASS_ORDER

    events = events[
        events["year"].between(start_year, end_year, inclusive="both")
        & events["size_class"].isin(active_classes)
    ].copy()

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
        [range(start_year, end_year + 1), active_classes],
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


def render_overview_chart(metric, events=None, start_year=1980, end_year=2025, selected_classes=None):
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

    active_classes = selected_classes if selected_classes else CLASS_ORDER

    if events is not None and not events.empty:
        filtered = events[
            events["year"].between(start_year, end_year, inclusive="both")
            & events["size_class"].isin(active_classes)
        ].copy()

        if filtered.empty:
            st.info("No heatwave events are available for the current selection.")
            return

        chart_df = (
            filtered.groupby("size_class", observed=False)
            .agg(
                total_heatwaves=("year", "size"),
                mean_peak_temp=("max_temp", "mean"),
                mean_avg_temp=("avg_temp", "mean"),
                mean_duration=("duration_days", "mean"),
            )
            .reset_index()
        )

        n_years = end_year - start_year + 1
        chart_df["heatwaves_per_place_year"] = chart_df.apply(
            lambda row: row["total_heatwaves"]
            / (N_PLACES[row["size_class"]] * n_years),
            axis=1,
        )
    else:
        chart_df = SUMMARY[
            SUMMARY["size_class"].isin(active_classes)
        ].copy()

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


def render_trend_chart(yearly, metric, selected_classes=None):
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

    active_classes = selected_classes if selected_classes else CLASS_ORDER
    plot_df = yearly[
        yearly["size_class"].isin(active_classes)
    ].copy()
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
        f"**Research question:** {RQ_META['rq4']['title']}"
        )
    
    st.markdown(
        """
        **Why Italy?**  
        Italy was identified in **RQ3** as the European country with the strongest
        median increase in heatwave frequency among countries with sufficient
        city-level data. RQ4 therefore examines whether this increase is concentrated
        in large cities or also occurs in smaller cities and rural municipalities.
        """
)

    st.subheader("How the analysis works")
    
    method_left, method_right = st.columns(2)
    
    with method_left:
        st.markdown(
            """
            **City-size classes**
        
            - Large city: ≥150,000 inhabitants
            - Medium-sized city: 20,000-149,999
            - Small town: 5,000-19,999
            - Rural municipality: 1-4,999 and ≥15 km from a large-city
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

    st.write("")
    st.subheader("Explore the results")

    st.markdown(
        "Change the analysis period, select city-size classes, and switch "
        "between heatwave metrics. The charts update automatically."
    )

    events = load_events()

    selected_years = st.slider(
        "Select analysis period",
        min_value=1980,
        max_value=2025,
        value=(1980, 2025),
        step=1,
        key="rq4_year_range",
    )
    start_year, end_year = selected_years

    selected_classes = st.multiselect(
        "Select city-size classes",
        options=CLASS_ORDER,
        default=CLASS_ORDER,
        format_func=lambda x: CLASS_LABELS[x],
        key="rq4_class_filter",
    )

    if not selected_classes:
        selected_classes = CLASS_ORDER

    metric = st.segmented_control(
        "Select heatwave metric",
        options=[
            "Frequency",
            "Duration",
        ],
        default="Frequency",
        key="rq4_metric",
    )

    if metric is None:
        metric = "Frequency"

    yearly_filtered = build_yearly(
        events,
        start_year=start_year,
        end_year=end_year,
        selected_classes=selected_classes,
    )

    st.caption(
        f"Current selection: {start_year}–{end_year} · "
        f"{len(selected_classes)} city-size class"
        + ("" if len(selected_classes) == 1 else "es")
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Long-term trend",
            "Overall comparison",
            "Trend statistics",
        ]
    )

    with tab1:
        st.markdown(
            f"#### Development from {start_year} to {end_year}"
        )

        if yearly_filtered is not None:
            render_trend_chart(
                yearly_filtered,
                metric,
                selected_classes=selected_classes,
            )
        else:
            st.info(
                "Add `RQ4_Italy_heatwaves_events.csv` to the `data/` folder "
                "to display the interactive yearly trend chart."
            )

        

    with tab2:
        st.markdown(
            f"#### Average values for {start_year}–{end_year}"
        )

        render_overview_chart(
            metric,
            events=events,
            start_year=start_year,
            end_year=end_year,
            selected_classes=selected_classes,
        )

    with tab3:
        st.markdown(
            "#### Published full-period trend statistics, 1980–2025"
        )
        render_trend_table(metric)

    st.divider()

    
    st.subheader("Conclusion")

    st.markdown(
        """
        In Italy, **heatwave frequency increased significantly across all city-size
        classes** between 1980 and 2025, with similar trends in large cities,
        medium-sized cities, small towns, and rural municipalities.

        **Heatwave duration also increased significantly across all four city-size
        classes**. In contrast, heatwave intensity showed less consistent changes:
        peak temperature increased significantly only in **large cities**, while
        average heatwave temperature showed no significant increase in any city-size
        class.

        Overall, the results show that rising heatwave trends in Italy are **not
        concentrated in large cities**. Smaller cities and rural municipalities
        experienced comparable increases in heatwave frequency and duration.
        """
    )


def render():
    with st.container(key="rq4_page_shell"):
        _render_rq4_content()
