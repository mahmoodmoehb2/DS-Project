import streamlit as st

from content import RQ_META
from theme import stat_cards
from utils import rq_card


def render(pages):
    # ---------- Hero ----------
    st.markdown(
        """
        <div class="hero">
            <h1>Climate Change<br>in Europe</h1>
            <p>
                Exploring heatwave trends, UV exposure, regional differences
                and potential public-health impacts across Europe.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two clear entry points into the project.
    c1, c2, _ = st.columns([1.15, 1.0, 3.2])

    with c1:
        if st.button(
            "Explore Heatwaves →",
            type="primary",
            use_container_width=True,
            key="home_heatwaves",
        ):
            st.switch_page(pages["rq2"])

    with c2:
        if st.button(
            "Explore UV →",
            use_container_width=True,
            key="home_uv",
        ):
            st.switch_page(pages["rq5"])

    # ---------- Project snapshot ----------
    st.write("")
    stat_cards(
        [
            ("bar_chart", "6", "Research questions"),
            ("public", "2", "Focus countries: Germany & Italy"),
            ("calendar_month", "1980–2025", "Long-term climate trends"),
            ("diversity_1", "2", "Climate & public-health perspectives"),
        ]
    )

    # ---------- Research questions ----------
    st.write("")
    st.markdown("## Our Research Questions")
    st.caption(
        "The project combines heatwave analysis with UV and health-related research."
    )

    # Heatwave section
    st.markdown("### Heatwaves")
    st.caption(
        "How heatwave frequency, intensity and duration are changing across cities, "
        "city sizes and European regions."
    )

    heatwave_row_1 = st.columns(2)
    heatwave_row_2 = st.columns(2)

    for col, key in zip(
        heatwave_row_1 + heatwave_row_2,
        ["rq1", "rq2", "rq3", "rq4"],
    ):
        meta = RQ_META[key]
        with col:
            rq_card(
                pages[key],
                meta["icon"],
                meta["code"],
                meta["short"],
                meta["status"],
            )

    st.write("")

    # UV section
    st.markdown("### UV")
    st.caption(
        "How UV exposure is changing over time and what these trends may mean "
        "for public health."
    )

    uv_row = st.columns(2)

    for col, key in zip(uv_row, ["rq5", "rq6"]):
        meta = RQ_META[key]
        with col:
            rq_card(
                pages[key],
                meta["icon"],
                meta["code"],
                meta["short"],
                meta["status"],
            )

    # ---------- Closing banner ----------
    st.write("")
    st.markdown(
        '<div class="quote-banner">'
        '"Hotter days. Brighter risks. A cooler future through knowledge."'
        "</div>",
        unsafe_allow_html=True,
    )
