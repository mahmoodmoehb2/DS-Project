"""Shared layout for research questions that don't have a finished analysis
behind them yet (RQ1, RQ3, RQ5, RQ6). Deliberately shows no numbers, charts
or "key findings" — that content doesn't exist yet, and this project should
not display invented results.
"""

import streamlit as st

from content import RQ_META
from theme import page_header


def render(rq_key: str):
    meta = RQ_META[rq_key]

    page_header(meta["code"], meta["title"])
    st.write("")
    st.info(
        "🚧 **Analysis not available yet.** This page is a placeholder that matches the "
        "site's navigation structure — the underlying analysis for this research question "
        "hasn't been run in this project so far. Once a notebook exists for it, build this "
        "page the same way as `views/rq_detail.py` (RQ2/RQ4): add the metric selector, "
        "exported charts, key finding and trend-statistics table."
    )
