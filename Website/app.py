from functools import partial
from pathlib import Path
import base64

import streamlit as st

from content import RQ_META
from theme import inject_theme, nav_icon
from views import about, home, rq1, rq2, rq3, rq4, rq5, rq6

st.set_page_config(
    page_title="Heatwaves & UV in Europe",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

BASE_DIR = Path(__file__).parent
logo_path = BASE_DIR / "assets" / "logo.png"

_rq_renderers = {
    "rq1": rq1.render,
    "rq2": rq2.render,
    "rq3": rq3.render,
    "rq4": rq4.render,
    "rq5": rq5.render,
    "rq6": rq6.render,
}

rq_pages = {
    key: st.Page(
        _rq_renderers[key],
        title=f"{meta['code']}  {meta['short']}",
        url_path=key,
    )
    for key, meta in RQ_META.items()
}

country_pages = {
    "germany": st.Page(
        rq2.render,
        title="Germany",
        icon="",
        url_path="germany",
    ),
    "italy": st.Page(
        rq4.render,
        title="Italy",
        icon="",
        url_path="italy",
    ),
}

about_pages = {
    "methods": st.Page(
        about.render_methods,
        title="Data and methods",
        icon=nav_icon("database"),
        url_path="about-methods",
    ),
    "info": st.Page(
        about.render_info,
        title="Project information",
        icon=nav_icon("info"),
        url_path="about-info",
    ),
}

home_page = st.Page(
    partial(home.render, pages=rq_pages),
    title="Home",
    icon=nav_icon("home"),
    url_path="home",
    default=True,
)

# Keep Streamlit's multipage router, but hide its default navigation.
# We render our own sidebar below, which gives us much more control over the design.
nav = st.navigation(
    {
        "": [home_page],
        "Heatwaves": [rq_pages["rq1"], rq_pages["rq2"], rq_pages["rq3"], rq_pages["rq4"]],
        "UV": [rq_pages["rq5"], rq_pages["rq6"]],
        "Countries": list(country_pages.values()),
        "About": list(about_pages.values()),
    },
    position="hidden",
)

# ---------------- Custom sidebar ----------------
with st.sidebar:
    if logo_path.exists():
        # Render the logo inside ONE HTML element. Using separate st.markdown()
        # calls around st.image() creates an empty div and was the source of
        # the large blank space above the logo.
        logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        st.markdown(
            f'<div class="sidebar-brand">'
            f'<img src="data:image/png;base64,{logo_b64}" alt="Heatwaves & UV in Europe">'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="sidebar-brand-text">☀️ <span>Heatwaves & UV<br>in Europe</span></div>',
            unsafe_allow_html=True,
        )

    st.page_link(
        home_page,
        label="Home",
        icon=nav_icon("home"),
        use_container_width=True,
    )

    st.markdown('<div class="sidebar-section-title">Research Questions</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-subsection-title">Heatwaves</div>', unsafe_allow_html=True)
    for key in ["rq1", "rq2", "rq3", "rq4"]:
        meta = RQ_META[key]
        st.page_link(
            rq_pages[key],
            label=f"{meta['code']}   {meta['short']}",
                use_container_width=True,
        )

    st.markdown('<div class="sidebar-subsection-title sidebar-subsection-uv">UV</div>', unsafe_allow_html=True)
    for key in ["rq5", "rq6"]:
        meta = RQ_META[key]
        st.page_link(
            rq_pages[key],
            label=f"{meta['code']}   {meta['short']}",
                use_container_width=True,
        )


    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">About</div>', unsafe_allow_html=True)
    st.page_link(
        about_pages["methods"],
        label="Data and methods",
        icon=nav_icon("database"),
        use_container_width=True,
    )
    st.page_link(
        about_pages["info"],
        label="Project information",
        icon=nav_icon("info"),
        use_container_width=True,
    )

nav.run()
