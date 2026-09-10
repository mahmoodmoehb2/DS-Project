import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import linregress, pearsonr
from pathlib import Path

from content import RQ_META


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
HEALTH_FILE = DATA_DIR / "sunburn_heatstroke_2000_2024.csv"
UV_FILE = DATA_DIR / "bundesland_uv_2000_2024.csv"


@st.cache_data
def load_data():
    if not HEALTH_FILE.exists():
        raise FileNotFoundError(
            f"Missing file: {HEALTH_FILE.name}. Place it in Website/data."
        )

    if not UV_FILE.exists():
        raise FileNotFoundError(
            f"Missing file: {UV_FILE.name}. Place it in Website/data."
        )

    health = pd.read_csv(HEALTH_FILE)
    uv = pd.read_csv(UV_FILE)

    health["year"] = pd.to_numeric(health["year"], errors="coerce")
    health["cases"] = pd.to_numeric(health["cases"], errors="coerce")
    uv["year"] = pd.to_numeric(uv["year"], errors="coerce")
    uv["mean_uvi"] = pd.to_numeric(uv["mean_uvi"], errors="coerce")

    health = health.dropna(subset=["year", "state", "icd10_code", "cases"]).copy()
    uv = uv.dropna(subset=["year", "bundesland", "mean_uvi"]).copy()

    health["year"] = health["year"].astype(int)
    uv["year"] = uv["year"].astype(int)

    return health, uv


def trend_stats(df, x_col, y_col):
    data = df[[x_col, y_col]].dropna()
    if len(data) < 3 or data[x_col].nunique() < 2:
        return None

    result = linregress(data[x_col], data[y_col])
    return {
        "slope": result.slope,
        "p_value": result.pvalue,
        "r2": result.rvalue ** 2,
        "significant": result.pvalue < 0.05,
    }


def render_method():
    st.markdown(
        """
The analysis combines two datasets for **2000–2024**.

**1. UV exposure by federal state**  
For each German federal state, selected cities are used to estimate annual UV
exposure. City-level UV values are combined into a **population-weighted mean
UV Index** for each state and year.

**2. Health outcomes**  
Hospital diagnosis data are used for **sunburn (ICD-10 L55)** and
**effect of heat and light (ICD-10 T67)**, aggregated by federal
state and year.

**3. Temporal trends**  
Annual UV Index and diagnosis counts are visualised over time. Linear
regression is used to describe long-term trends.

**4. UV–health relationship**  
UV Index values are matched with diagnosis counts by **federal state and year**
to examine whether higher UV exposure is associated with more recorded sunburn
cases.

The analysis describes associations and **does not establish causality**.
        """
    )


def render_uv_trend(uv):
    yearly = (
        uv.groupby("year", as_index=False)["mean_uvi"]
        .mean()
        .sort_values("year")
    )
    yearly["smooth"] = yearly["mean_uvi"].rolling(
        5, min_periods=1, center=True
    ).mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=yearly["year"],
            y=yearly["mean_uvi"],
            mode="markers",
            name="Annual mean",
            opacity=0.45,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=yearly["year"],
            y=yearly["smooth"],
            mode="lines",
            name="5-year moving average",
            line=dict(width=3),
        )
    )
    fig.update_layout(
        title="Average UV Index across German federal states",
        xaxis_title="Year",
        yaxis_title="Average UV Index",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=60, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_health_trend(health, diagnosis_code="ICD10-L55"):
    labels = {
        "ICD10-L55": "Sunburn (ICD-10 L55)",
        "ICD10-T67": "Effect of heat and light (ICD-10 T67)",
    }

    yearly = (
        health[health["icd10_code"] == diagnosis_code]
        .groupby("year", as_index=False)["cases"]
        .sum()
        .sort_values("year")
    )
    yearly["smooth"] = yearly["cases"].rolling(
        5, min_periods=1, center=True
    ).mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=yearly["year"],
            y=yearly["cases"],
            mode="markers",
            name="Annual cases",
            opacity=0.45,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=yearly["year"],
            y=yearly["smooth"],
            mode="lines",
            name="5-year moving average",
            line=dict(width=3),
        )
    )
    fig.update_layout(
        title=f"Recorded {labels[diagnosis_code]} cases in Germany",
        xaxis_title="Year",
        yaxis_title="Recorded cases",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=60, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_state_uv_comparison(uv, start_year=2000, end_year=2024):
    state_mean = (
        uv.groupby("bundesland", as_index=False)["mean_uvi"]
        .mean()
        .sort_values("mean_uvi", ascending=False)
    )

    fig = px.bar(
        state_mean,
        x="mean_uvi",
        y="bundesland",
        orientation="h",
        labels={
            "mean_uvi": f"Average UV Index, {start_year}–{end_year}",
            "bundesland": "Federal state",
        },
        title="Average UV Index by federal state",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=10, r=10, t=60, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_state_sunburn_comparison(health, start_year=2000, end_year=2024):
    sunburn = health[health["icd10_code"] == "ICD10-L55"].copy()
    state_totals = (
        sunburn.groupby("state", as_index=False)["cases"]
        .sum()
        .sort_values("cases", ascending=False)
    )

    fig = px.bar(
        state_totals,
        x="cases",
        y="state",
        orientation="h",
        labels={
            "cases": f"Recorded sunburn cases, {start_year}–{end_year}",
            "state": "Federal state",
        },
        title="Recorded sunburn cases by federal state",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=10, r=10, t=60, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_uv_health_relationship(health, uv):
    sunburn = (
        health[health["icd10_code"] == "ICD10-L55"]
        [["year", "state", "cases"]]
        .rename(columns={"state": "bundesland", "cases": "sunburn_cases"})
    )

    merged = uv.merge(
        sunburn,
        on=["year", "bundesland"],
        how="inner",
    ).dropna(subset=["mean_uvi", "sunburn_cases"])

    if merged.empty:
        st.warning(
            "No matching federal-state/year observations were found between "
            "the UV and health datasets."
        )
        return

    fig = px.scatter(
        merged,
        x="mean_uvi",
        y="sunburn_cases",
        hover_data=["bundesland", "year"],
        trendline="ols",
        labels={
            "mean_uvi": "Mean UV Index",
            "sunburn_cases": "Recorded sunburn cases",
        },
        title="UV Index and recorded sunburn cases",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig, use_container_width=True)

    if len(merged) >= 3:
        r, p = pearsonr(merged["mean_uvi"], merged["sunburn_cases"])
        if p < 0.05:
            st.info(
                f"Pearson correlation: r = {r:.2f}, p = {p:.4f}. "
                "The association is statistically significant, but it should "
                "not be interpreted as evidence of causality."
            )
        else:
            st.info(
                f"Pearson correlation: r = {r:.2f}, p = {p:.4f}. "
                "No statistically significant linear association was detected."
            )


def render_trend_statistics(uv, health):
    uv_yearly = (
        uv.groupby("year", as_index=False)["mean_uvi"]
        .mean()
        .rename(columns={"mean_uvi": "value"})
    )
    sunburn_yearly = (
        health[health["icd10_code"] == "ICD10-L55"]
        .groupby("year", as_index=False)["cases"]
        .sum()
        .rename(columns={"cases": "value"})
    )
    heat_yearly = (
        health[health["icd10_code"] == "ICD10-T67"]
        .groupby("year", as_index=False)["cases"]
        .sum()
        .rename(columns={"cases": "value"})
    )

    rows = []
    for label, df, unit in [
        ("Average UV Index", uv_yearly, "index units/year"),
        ("Sunburn cases", sunburn_yearly, "cases/year"),
        ("Heat-related cases", heat_yearly, "cases/year"),
    ]:
        result = trend_stats(df, "year", "value")
        if result is not None:
            rows.append(
                {
                    "Metric": label,
                    "Slope": result["slope"],
                    "Unit": unit,
                    "p-value": result["p_value"],
                    "Significant": "Yes" if result["significant"] else "No",
                }
            )

    stats = pd.DataFrame(rows)
    if stats.empty:
        st.info("Not enough data to calculate trend statistics.")
        return

    display = stats.copy()
    display["Slope"] = display["Slope"].map(lambda x: f"{x:+.4f}")
    display["p-value"] = display["p-value"].map(
        lambda x: "<0.0001" if x < 0.0001 else f"{x:.4f}"
    )

    st.dataframe(display, use_container_width=True, hide_index=True)


def render_conclusion(uv, health):
    uv_yearly = (
        uv.groupby("year", as_index=False)["mean_uvi"]
        .mean()
        .rename(columns={"mean_uvi": "value"})
    )
    sunburn_yearly = (
        health[health["icd10_code"] == "ICD10-L55"]
        .groupby("year", as_index=False)["cases"]
        .sum()
        .rename(columns={"cases": "value"})
    )

    uv_trend = trend_stats(uv_yearly, "year", "value")
    sunburn_trend = trend_stats(sunburn_yearly, "year", "value")

    uv_text = (
        "shows a statistically significant long-term change"
        if uv_trend and uv_trend["significant"]
        else "does not show a statistically significant long-term change"
    )
    sunburn_text = (
        "show a statistically significant long-term change"
        if sunburn_trend and sunburn_trend["significant"]
        else "do not show a statistically significant long-term change"
    )

    st.markdown(
        f"""
Across Germany, the average UV Index **{uv_text}** between 2000 and 2024.
Recorded sunburn cases **{sunburn_text}** over the same period.

The regional comparison helps identify whether federal states with higher
average UV exposure also tend to report more sunburn cases. However, these
results should be interpreted as **associations rather than causal effects**,
because hospital case counts can also be influenced by population size,
behaviour, reporting practices, healthcare use, and other factors.

Overall, the analysis provides an indication of the possible public-health
relevance of UV exposure, while showing that UV Index alone cannot fully
explain observed differences in sunburn diagnoses.
        """
    )


def _render_rq6_content():
    meta = RQ_META["rq6"]

    st.markdown(
        '<div class="eyebrow">RQ6 · UV · GERMANY · HEALTH</div>',
        unsafe_allow_html=True,
    )

    st.title("What does changing UV exposure mean for public health?")
    st.markdown(f"**Research question:** {meta['title']}")

    try:
        health, uv = load_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    st.subheader("How the analysis works")
    render_method()

    st.subheader("Explore the results")

    st.markdown(
        "Change the analysis period, select federal states, and switch "
        "between UV and health-related views. The charts update automatically."
    )

    selected_years = st.slider(
        "Select analysis period",
        min_value=2000,
        max_value=2024,
        value=(2000, 2024),
        step=1,
        key="rq6_year_range",
    )
    start_year, end_year = selected_years

    all_states = sorted(
        set(uv["bundesland"].dropna().astype(str))
        | set(health["state"].dropna().astype(str))
    )

    selected_states = st.multiselect(
        "Select federal states",
        options=all_states,
        default=[],
        placeholder="Leave empty to include all federal states",
        key="rq6_state_filter",
    )

    active_states = selected_states if selected_states else all_states

    uv_filtered = uv[
        uv["year"].between(start_year, end_year, inclusive="both")
        & uv["bundesland"].isin(active_states)
    ].copy()

    health_filtered = health[
        health["year"].between(start_year, end_year, inclusive="both")
        & health["state"].isin(active_states)
    ].copy()

    metric = st.segmented_control(
        "Select view",
        ["UV trend", "Sunburn trend", "Regional UV"],
        default="UV trend",
        key="rq6_metric",
    )

    if metric is None:
        metric = "UV trend"

    if selected_states:
        state_scope = (
            "1 selected federal state"
            if len(selected_states) == 1
            else f"{len(selected_states)} selected federal states"
        )
    else:
        state_scope = f"all {len(all_states)} federal states"

    st.caption(
        f"Current selection: {start_year}–{end_year} · {state_scope}"
    )

    if metric == "UV trend":
        if uv_filtered.empty:
            st.info("No UV observations are available for the current selection.")
        else:
            render_uv_trend(uv_filtered)
            

    elif metric == "Sunburn trend":
        diagnosis = st.radio(
            "Diagnosis",
            ["Sunburn", "Effect of heat and light"],
            horizontal=True,
            key="rq6_diagnosis",
        )
        code = "ICD10-L55" if diagnosis == "Sunburn" else "ICD10-T67"

        if health_filtered.empty:
            st.info(
                "No health observations are available for the current selection."
            )
        else:
            render_health_trend(health_filtered, code)
            

    elif metric == "Regional UV":
        tab1, tab2 = st.tabs(["UV exposure", "Sunburn cases"])

        with tab1:
            if uv_filtered.empty:
                st.info(
                    "No UV observations are available for the current selection."
                )
            else:
                render_state_uv_comparison(
                    uv_filtered,
                    start_year=start_year,
                    end_year=end_year,
                )

        with tab2:
            if health_filtered.empty:
                st.info(
                    "No health observations are available for the current selection."
                )
            else:
                render_state_sunburn_comparison(
                    health_filtered,
                    start_year=start_year,
                    end_year=end_year,
                )



    st.subheader("Conclusion")
    
    render_conclusion(uv, health)

    st.markdown("#### Trend statistics, 2000–2024")
    render_trend_statistics(uv, health)


def render():
    with st.container(key="rq6_page_shell"):
        _render_rq6_content()
