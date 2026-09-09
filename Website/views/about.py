import streamlit as st

from theme import material_icon, page_header


def _card_title(icon_name: str, text: str):
    st.markdown(f"##### {material_icon(icon_name, size=18)} {text}", unsafe_allow_html=True)


def render_methods():
    page_header("About", "Data and methods")
    st.markdown(
        "This project explores long-term trends in heatwaves (and, where analysed, UV "
        "exposure) across Germany, Italy and Europe. We compare city sizes, regions and "
        "countries, and investigate potential health impacts."
    )
    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        _card_title("database", "Data sources")
        st.markdown(
            "- DWD Climate Data Center (Germany)\n"
            "- *(add Italy's climate data source here)*\n"
            "- Wikidata / ISTAT municipality metadata\n"
            "- *(add sources for RQ3, RQ5, RQ6 once available)*"
        )
    with c2, st.container(border=True):
        _card_title("calendar_month", "Time period")
        st.markdown("**1980–2025**\n\nReference period for the heatwave threshold: 1961–1990.")
    with c3, st.container(border=True):
        _card_title("science", "Methods")
        st.markdown(
            "- Heatwave detection: ≥3 consecutive days above the local 98th-percentile "
            "threshold **and** above 28 °C (DWD definition)\n"
            "- Trend analysis (5-year moving average, linear regression)\n"
            "- Statistical significance testing: Kruskal-Wallis test across size classes, "
            "`p < 0.05`"
        )


def render_info():
    page_header("About", "Project information")

    _card_title("group", "Project team")
    with st.container(border=True):
        st.markdown(
            "*(Add your team members' names here.)*\n\n"
            "Course: Data Science Projekt SS 2026 — BSc Data Science"
        )

    _card_title("school", "Course supervisors")
    with st.container(border=True):
        st.markdown(
            "Prof. Peer Kröger, Dr. Rükiye Altin, Sweety Mohanty, Mirjam Bayer\n\n"
            "Project period: 17.08.2026 – 11.09.2026"
        )

    _card_title("code", "Code and data")
    with st.container(border=True):
        st.markdown(
            "*(Add a link to your GitHub repository / project website here so people can "
            "find the full code, data and additional results.)*"
        )
