"""Shared page layout for a finished research question (currently RQ2 and
RQ4): eyebrow + title, metric pill selector, one big chart, key-finding
callout, trend-statistics table with a download button, and a methodology
expander. RQ2 and RQ4 are otherwise identical except for their content, so
both pages just call render() with their own key from content.RQ_META.
"""

import streamlit as st

from content import METRICS, RQ_META
from theme import key_finding, page_header
from utils import metric_pills, show_image, stats_table_with_download


def render(rq_key: str):
    meta = RQ_META[rq_key]

    page_header(meta["code"], meta["title"], meta.get("description", ""))
    st.write("")

    st.caption("Select metric")
    selected = metric_pills(METRICS, state_key=f"{rq_key}_metric")
    metric = next(m for m in METRICS if m["key"] == selected)

    filename = f"{meta['image_prefix']}_{metric['suffix']}.png"
    show_image(filename, caption=f"{metric['chart_title']} ({meta['country']})")

    key_finding(meta["key_findings"][selected])

    st.markdown("##### Trend statistics (1980–2025)")
    stats_table_with_download(
        meta["trend_csv"],
        caption="Linear regression per size class and metric (slope per year, p-value, r², significant, n).",
    )

    st.divider()
    with st.expander("Data and methods for this page"):
        st.markdown(meta["methodology"])
