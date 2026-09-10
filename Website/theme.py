

import streamlit as st

PURPLE = "#7C3AED"
PURPLE_DARK = "#5B21B6"
PURPLE_SOFT_BG = "#F5EEFF"
PURPLE_BORDER = "#E4D9FB"
TEXT_MUTED = "#6B7280"


def inject_theme():
    """Apply the shared visual design for the Streamlit app."""
    st.markdown(
        f"""
        <style>
        :root {{
            --purple: {PURPLE};
            --purple-dark: {PURPLE_DARK};
            --purple-soft: {PURPLE_SOFT_BG};
            --purple-border: {PURPLE_BORDER};
            --text: #172033;
            --muted: {TEXT_MUTED};
            --page: #FCFBFF;
        }}

        /* ---------- App shell ---------- */
        .stApp {{
            background: var(--page);
            color: var(--text);
        }}

        .block-container {{
            width: min(calc(100% - 3rem), 1450px);
            max-width: 1450px;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-top: 4.4rem !important;
            padding-bottom: 5rem !important;
            padding-left: 5.5rem !important;
            padding-right: 5.5rem !important;
            transform: translateX(0) !important;
            transition: transform 180ms ease;
        }}

        /* CLOSED SIDEBAR:
           the main content stays exactly centered in the available page width.
           This is the default state above: auto margins + translateX(0). */

        /* OPEN SIDEBAR:
           only then move the content a little to the right. */
        div[data-testid="stAppViewContainer"]:has(
            section[data-testid="stSidebar"][aria-expanded="true"]
        ) .block-container {{
            transform: translateX(18px) !important;
        }}

        /* Extra fallback for Streamlit versions where the collapsed sidebar
           remains in the DOM without aria-expanded="false". */
        div[data-testid="stAppViewContainer"]:not(:has(
            section[data-testid="stSidebar"][aria-expanded="true"]
        )) .block-container {{
            margin-left: auto !important;
            margin-right: auto !important;
            transform: translateX(0) !important;
        }}

        html, body, [class*="css"] {{
            font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
        }}

        h1, h2, h3, h4 {{
            color: var(--text);
            letter-spacing: -0.025em;
        }}

        h1 {{ font-weight: 800 !important; }}
        h2 {{ font-weight: 750 !important; }}
        h3 {{ font-weight: 700 !important; }}
        p {{ line-height: 1.55; }}

        /* ---------- Custom sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background: #F8F7FC !important;
            border-right: 1px solid #E6E0F2;
            width: 282px !important;
            min-width: 282px !important;
        }}

        section[data-testid="stSidebar"] > div {{
            width: 282px !important;
        }}

        /* Keep the whole sidebar visually as one continuous surface. */
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div,
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"],
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
            border-radius: 0 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
            padding: 0.45rem 0.85rem 1.5rem 0.85rem !important;
        }}

        /* Overlay the Streamlit header so it no longer reserves a large blank area. */
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{
            position: absolute !important;
            top: 0.45rem !important;
            right: 0.55rem !important;
            height: 2rem !important;
            min-height: 2rem !important;
            width: 2rem !important;
            padding: 0 !important;
            margin: 0 !important;
            z-index: 100 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"] button[data-testid="stSidebarCollapseButton"] {{
            position: relative !important;
            z-index: 101 !important;
            pointer-events: auto !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
            display: none !important;
        }}

        .sidebar-brand {{
            min-height: 0;
            padding: 0.35rem 2.35rem 0.8rem 0.2rem;
            margin: 0;
            display: flex;
            align-items: center;
        }}

        .sidebar-brand img {{
            display: block;
            max-width: 150px !important;
            width: 150px;
            height: auto !important;
            margin: 0;
            mix-blend-mode: multiply !important;

        }}

        .sidebar-brand-text {{
            display: flex;
            gap: 0.55rem;
            align-items: center;
            padding: 0.35rem 2.4rem 1.1rem 0.3rem;
            color: #172033;
            font-size: 0.87rem;
            font-weight: 800;
            line-height: 1.1;
        }}

        .sidebar-section-title {{
            color: #252B3A !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            margin: 0.92rem 0.45rem 0.28rem 0.45rem;
            letter-spacing: 0 !important;
        }}

        .sidebar-divider {{
            height: 1px;
            background: #E5E0EC;
            margin: 0.8rem 0.35rem 0.15rem 0.35rem;
        }}

        /* Subgroups inside Research Questions: Heatwaves / UV */
        .sidebar-subsection-title {{
            color: #6B7280 !important;
            font-size: 0.70rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.055em;
            margin: 0.48rem 0.45rem 0.14rem 0.45rem;
        }}

        .sidebar-subsection-uv {{
            margin-top: 0.72rem;
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] {{
            margin: 0.08rem 0 !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] a {{
            min-height: 36px !important;
            border-radius: 7px !important;
            padding: 0.42rem 0.55rem !important;
            color: #374151 !important;
            text-decoration: none !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            transition: background 120ms ease, color 120ms ease, transform 120ms ease;
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] a:hover {{
            background: #EEE9FA !important;
            color: var(--purple-dark) !important;
            transform: translateX(1px);
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] {{
            background: linear-gradient(90deg, #A51CB8 0%, #C319B5 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(158, 31, 181, 0.18);
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] *,
        section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] p,
        section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] span {{
            color: white !important;
            font-weight: 600 !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] svg {{
            width: 15px !important;
            height: 15px !important;
            flex: 0 0 15px !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stPageLink"] p,
        section[data-testid="stSidebar"] div[data-testid="stPageLink"] span {{
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            line-height: 1.2 !important;
            color: inherit !important;
        }}


        /* Prevent the global card styling from creating a white card inside the sidebar. */
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: transparent !important;
            border-color: transparent !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }}


        /* Reserve space for Streamlit's top bar without making headings too loose. */
        .block-container h1 {{
            margin-top: 0 !important;
            margin-bottom: 0.8rem !important;
        }}


        @media (max-width: 900px) {{
            .block-container {{
                width: calc(100% - 1.5rem) !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
                padding-top: 4rem !important;
            }}
        }}

        /* ---------- Hero ---------- */
        .hero {{
            position: relative;
            overflow: hidden;
            background:
                radial-gradient(circle at 82% 18%, rgba(255,255,255,0.18), transparent 28%),
                linear-gradient(120deg, #2D174F 0%, #6D28D9 52%, #C2410C 100%);
            border-radius: 24px;
            padding: 58px 48px;
            color: white;
            margin: 0 0 14px 0;
            box-shadow: 0 16px 38px rgba(67, 32, 128, 0.16);
        }}

        .hero::after {{
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            right: -130px;
            top: -180px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.20);
            box-shadow: 0 0 0 55px rgba(255,255,255,0.035),
                        0 0 0 110px rgba(255,255,255,0.025);
            pointer-events: none;
        }}

        .hero h1 {{
            color: white !important;
            font-size: clamp(2.35rem, 4vw, 4rem) !important;
            line-height: 1.04;
            margin: 0 0 1rem 0 !important;
            max-width: 760px;
        }}

        .hero p {{
            color: #F4F0FF;
            font-size: 1.12rem;
            max-width: 720px;
            margin-bottom: 0;
        }}

        /* ---------- Buttons ---------- */
        div[data-testid="stButton"] > button {{
            border-radius: 999px !important;
            font-weight: 700 !important;
            border: 1px solid var(--purple-border) !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        div[data-testid="stButton"] > button[kind="primary"] {{
            background: linear-gradient(90deg, var(--purple-dark), var(--purple)) !important;
            color: white !important;
            border-color: transparent !important;
        }}

        /* ---------- Cards ---------- */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border-color: #E8E3F1 !important;
            background: rgba(255,255,255,0.94);
            box-shadow: 0 6px 20px rgba(34, 24, 70, 0.045);
        }}

        .stat-row {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin: 18px 0 28px 0;
        }}

        .stat-card {{
            min-height: 100px;
            background: linear-gradient(145deg, #F8F4FF 0%, #F3ECFF 100%);
            border: 1px solid var(--purple-border);
            border-radius: 16px;
            padding: 17px 18px;
        }}

        .stat-number {{
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--purple-dark);
            line-height: 1.2;
            margin-bottom: 5px;
        }}

        .stat-label {{
            color: var(--muted);
            font-size: 0.87rem;
            line-height: 1.35;
        }}

        /* ---------- RQ pages ---------- */
        .eyebrow {{
            display: inline-flex;
            color: var(--purple);
            font-weight: 800;
            letter-spacing: 0.065em;
            font-size: 0.88rem;
            margin-bottom: -0.25rem;
            text-transform: uppercase;
        }}

        .kf-box {{
            background: linear-gradient(100deg, #F8EEFF 0%, #FFF4FA 100%);
            border: 1px solid #ECDDF8;
            border-left: 5px solid var(--purple);
            border-radius: 14px;
            padding: 16px 20px;
            margin: 18px 0;
        }}

        .kf-title {{
            color: var(--purple-dark);
            font-weight: 800;
            margin-bottom: 6px;
        }}

        .kf-text {{
            color: #374151;
            line-height: 1.55;
        }}

        .quote-banner {{
            background: linear-gradient(90deg, #F7F0FF, #FFF5FA);
            border: 1px solid #EDE3FA;
            border-radius: 14px;
            text-align: center;
            padding: 18px;
            font-style: italic;
            color: var(--purple-dark);
            margin-top: 18px;
        }}

        .status-pill-pending {{
            display: inline-block;
            background-color: #FEF3C7;
            color: #92400E;
            border-radius: 999px;
            padding: 3px 11px;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid #ECE7F4;
            border-radius: 14px;
            overflow: hidden;
        }}

        div[data-testid="stImage"] img {{
            border-radius: 12px;
        }}

        hr {{ border-color: #EEEAF5 !important; }}

        @media (max-width: 1050px) {{
            .stat-row {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .hero {{ padding: 42px 30px; }}
            .block-container {{
                padding-left: 1.25rem;
                padding-right: 1.25rem;
                transform: none !important;
            }}
        }}

        @media (max-width: 680px) {{
            .stat-row {{ grid-template-columns: 1fr; }}
            .hero {{ border-radius: 18px; padding: 34px 24px; }}
            .hero h1 {{ font-size: 2.15rem !important; }}
        }}

        /* FINAL main-content inset:
           target Streamlit's real main container, not only .block-container. */
        div[data-testid="stAppViewContainer"]
        section[data-testid="stMain"]
        div[data-testid="stMainBlockContainer"].block-container {{
            box-sizing: border-box !important;
            padding-left: 4.5rem !important;
            padding-right: 4.5rem !important;
            padding-top: 4.4rem !important;
            padding-bottom: 5rem !important;
        }}

        @media (max-width: 900px) {{
            div[data-testid="stAppViewContainer"]
            section[data-testid="stMain"]
            div[data-testid="stMainBlockContainer"].block-container {{
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
            }}
        }}


        /* ---------- RQ2 page shell ----------
           The outer white RQ2 surface stays where it is; all RQ2 content is
           inset inside it, matching the inner frame the user marked. */
        .st-key-home_page_shell,
        .st-key-rq1_page_shell,
        .st-key-rq2_page_shell,
        .st-key-rq3_page_shell,
        .st-key-rq4_page_shell,
        .st-key-rq5_page_shell,
        .st-key-rq6_page_shell {{
            background: #FFFFFF !important;
            border-radius: 18px !important;
            padding: 2.4rem 3.2rem 3.2rem 3.2rem !important;
            box-sizing: border-box !important;
            box-shadow: 0 6px 24px rgba(34, 24, 70, 0.04) !important;
        }}

        /* Keep the inner layout aligned inside Home and all RQ page shells. */
        .st-key-home_page_shell > div,
        .st-key-home_page_shell [data-testid="stVerticalBlock"],
        .st-key-rq1_page_shell > div,
        .st-key-rq1_page_shell [data-testid="stVerticalBlock"],
        .st-key-rq2_page_shell > div,
        .st-key-rq2_page_shell [data-testid="stVerticalBlock"],
        .st-key-rq3_page_shell > div,
        .st-key-rq3_page_shell [data-testid="stVerticalBlock"],
        .st-key-rq4_page_shell > div,
        .st-key-rq4_page_shell [data-testid="stVerticalBlock"],
        .st-key-rq5_page_shell > div,
        .st-key-rq5_page_shell [data-testid="stVerticalBlock"],
        .st-key-rq6_page_shell > div,
        .st-key-rq6_page_shell [data-testid="stVerticalBlock"] {{
            box-sizing: border-box !important;
        }}

        @media (max-width: 900px) {{
            .st-key-home_page_shell,
            .st-key-rq1_page_shell,
            .st-key-rq2_page_shell,
        .st-key-rq3_page_shell,
        .st-key-rq4_page_shell,
        .st-key-rq5_page_shell,
        .st-key-rq6_page_shell {{
                padding: 1.5rem 1.35rem 2rem 1.35rem !important;
                border-radius: 14px !important;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# Small hand-built line-icon set (24x24 viewBox, stroke-based) matching the
# mockup's flat, single-color purple icon style. Deliberately NOT loaded from
# an external icon font/CDN (e.g. Google Fonts Material Symbols) - in this
# sandbox that request is blocked by the network policy (confirmed: a plain
# curl to fonts.googleapis.com fails to connect), and relying on it would
# mean the icons silently degrade to literal text like "trending_up" instead
# of a glyph. Inline SVG has no such dependency and always renders.
_ICON_SVGS = {
    "home": '<polyline points="3 11 12 4 21 11"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
    "public": (
        '<circle cx="12" cy="12" r="9"/><line x1="3" y1="12" x2="21" y2="12"/>'
        '<path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/>'
    ),
    "calendar_month": (
        '<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/>'
        '<line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/>'
    ),
    "bar_chart": '<line x1="6" y1="20" x2="6" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="18" y1="20" x2="18" y2="14"/>',
    "diversity_1": (
        '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.3"/>'
        '<path d="M4 20c0-3 2.5-5 5-5s5 2 5 5"/><path d="M15 20c0-2.3 1.8-4 3.5-4s3.5 1.7 3.5 4" opacity="0.7"/>'
    ),
    "trending_up": '<polyline points="3 17 9 11 13 15 21 6"/><polyline points="15 6 21 6 21 12"/>',
    "location_city": (
        '<rect x="4" y="10" width="5" height="11"/><rect x="10" y="6" width="5" height="15"/>'
        '<rect x="16" y="13" width="4" height="8"/>'
    ),
    "wb_sunny": (
        '<circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="5"/>'
        '<line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/>'
        '<line x1="19" y1="12" x2="22" y2="12"/><line x1="4.9" y1="4.9" x2="7" y2="7"/>'
        '<line x1="17" y1="17" x2="19.1" y2="19.1"/><line x1="4.9" y1="19.1" x2="7" y2="17"/>'
        '<line x1="17" y1="7" x2="19.1" y2="4.9"/>'
    ),
    "monitor_heart": (
        '<path d="M12 21s-7.5-4.6-10-9.3C0.5 8 2 4 6 4c2 0 3.5 1.2 4 2.5C10.5 5.2 12 4 14 4'
        'c4 0 5.5 4 4 7.7C19.5 16.4 12 21 12 21z"/>'
    ),
    "database": (
        '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/>'
        '<path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>'
    ),
    "info": '<circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/><circle cx="12" cy="7.5" r="0.9" fill="currentColor" stroke="none"/>',
    "group": (
        '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.3"/>'
        '<path d="M4 20c0-3 2.5-5 5-5s5 2 5 5"/><path d="M15 20c0-2.3 1.8-4 3.5-4s3.5 1.7 3.5 4" opacity="0.7"/>'
    ),
    "school": (
        '<polygon points="12 4 22 9 12 14 2 9 12 4"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/>'
        '<line x1="22" y1="9" x2="22" y2="15"/>'
    ),
    "code": '<polyline points="8 6 2 12 8 18"/><polyline points="16 6 22 12 16 18"/>',
    "lightbulb": (
        '<path d="M9 18h6"/><path d="M10 21h4"/>'
        '<path d="M12 3a6 6 0 0 0-4 10.5c.6.6 1 1.5 1 2.5h6c0-1 .4-1.9 1-2.5A6 6 0 0 0 12 3z"/>'
    ),
    "arrow_forward": '<line x1="4" y1="12" x2="19" y2="12"/><polyline points="13 6 19 12 13 18"/>',
    "science": (
        '<path d="M9 3h6"/><path d="M10 3v5l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/>'
        '<line x1="7" y1="14" x2="17" y2="14"/>'
    ),
}


def material_icon(name: str, size: int = 22, color: str = PURPLE) -> str:
    """Return an inline SVG icon glyph matching the mockup's flat, single-
    color purple icon style (as opposed to multi-color emoji). Self-
    contained - no external font/CDN. Use inside raw HTML built for
    st.markdown(..., unsafe_allow_html=True)."""
    inner = _ICON_SVGS.get(name)
    if inner is None:
        return name  # unknown name: fall back to showing it as text
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:middle;">{inner}</svg>'
    )


def nav_icon(icon) -> str:
    """Icon value to pass to a Streamlit-native `icon=` parameter (st.Page,
    st.page_link, st.button, ...). `icon` is either a plain emoji (e.g. a
    flag) - returned as-is - or a Material Symbols name - wrapped as
    ":material/name:", Streamlit's built-in shortcode for its own bundled
    copy of the same icon font."""
    if icon.startswith(":material/"):
        return icon
    if icon.isascii() and icon.replace("_", "").isalnum():
        return f":material/{icon}:"
    return icon  # already an emoji


def page_header(code: str, title: str, description: str = ""):
    st.markdown(f'<div class="eyebrow">{code}</div>', unsafe_allow_html=True)
    st.markdown(f"## {title}")
    if description:
        st.markdown(description)


def key_finding(text: str, icon: str = "lightbulb", title: str = "Key finding"):
    # NOTE: kept as a single line with no embedded blank lines. Streamlit's
    # markdown parser treats an indented, blank-line-separated HTML fragment
    # as a code block instead of raw HTML - see stat_cards() below for the
    # same issue in a more visible form.
    glyph = material_icon(icon, size=20, color=PURPLE_DARK)
    st.markdown(
        f'<div class="kf-box"><div class="kf-title">{glyph} {title}</div>'
        f'<div class="kf-text">{text}</div></div>',
        unsafe_allow_html=True,
    )


def stat_cards(items):
    """items: list of (material_icon_name, number, label) tuples.

    Built as ONE single-line HTML string on purpose: joining multi-line,
    indented HTML fragments (each with its own leading/trailing newline)
    makes Streamlit's markdown renderer treat everything after the first
    blank line as an indented code block instead of raw HTML, which is why
    only the first card used to render correctly and the rest showed up as
    literal `<div>` text.
    """
    cards_html = "".join(
        f'<div class="stat-card"><div class="stat-number">'
        f'{material_icon(icon, size=20)} {number}</div>'
        f'<div class="stat-label">{label}</div></div>'
        for icon, number, label in items
    )
    st.markdown(f'<div class="stat-row">{cards_html}</div>', unsafe_allow_html=True)
