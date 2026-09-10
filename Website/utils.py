

from pathlib import Path

import pandas as pd
import streamlit as st

from theme import material_icon, nav_icon

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
DATA_DIR = BASE_DIR / "data"


def show_image(filename: str, caption: str = ""):
    """Show an image from images/. If it doesn't exist yet (e.g. the notebook
    hasn't been run/exported locally), show a friendly placeholder instead of
    crashing the app."""
    path = IMAGES_DIR / filename
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(
            f" Chart not available yet: `{filename}`\n\n"
            f"Run the notebook and copy the exported file to `images/{filename}`."
        )


def show_csv_table(filename: str, index_col=None, caption: str = ""):
    """Show a CSV file (produced by the notebook) as a table. Shows a
    placeholder if the file hasn't been added yet."""
    path = DATA_DIR / filename
    if path.exists():
        df = pd.read_csv(path, index_col=index_col)
        if caption:
            st.caption(caption)
        st.dataframe(df, use_container_width=True)
    else:
        st.info(
            f" Table not available yet: `data/{filename}`\n\n"
            f"Run the notebook and copy the exported CSV to `data/{filename}`."
        )


def stats_table_with_download(filename: str, caption: str = ""):
    """Like show_csv_table, but also renders a 'Download data' button next
    to it, matching the mockup's trend-statistics panel."""
    path = DATA_DIR / filename
    if not path.exists():
        st.info(
            f" Table not available yet: `data/{filename}`\n\n"
            f"Export it from the notebook (e.g. the per-size-class regression "
            f"results) and place it in `data/{filename}`."
        )
        return

    df = pd.read_csv(path)
    top = st.columns([5, 1])
    with top[0]:
        if caption:
            st.caption(caption)
    with top[1]:
        st.download_button(
            "⬇️ Download data",
            data=path.read_bytes(),
            file_name=filename,
            mime="text/csv",
            use_container_width=True,
        )
    st.dataframe(df, use_container_width=True, hide_index=True)


def metric_pills(options, state_key: str, default_index: int = 0):
    """Render a row of pill-style buttons (one per metric) and return the
    key of the currently selected one. `options` is a list of dicts with at
    least "key" and "label"."""
    if state_key not in st.session_state:
        st.session_state[state_key] = options[default_index]["key"]

    cols = st.columns(len(options))
    for col, opt in zip(cols, options):
        active = st.session_state[state_key] == opt["key"]
        if col.button(
            opt["label"],
            key=f"{state_key}_{opt['key']}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state[state_key] = opt["key"]
            st.rerun()
    return st.session_state[state_key]


def rq_card(page, icon: str, code: str, short: str, status: str = "ready"):
    """One card in the 'Our Research Questions' grid on the home page."""
    with st.container(border=True):
        is_material_name = icon.isascii() and icon.replace("_", "").isalnum()
        glyph = material_icon(icon, size=26) if is_material_name else icon
        st.markdown(f"#### {glyph} {code}", unsafe_allow_html=True)
        st.caption(short)
        if status == "planned":
            st.markdown('<span class="status-pill-pending">coming soon</span>', unsafe_allow_html=True)
        st.page_link(page, label="Open", icon=nav_icon("arrow_forward"))
