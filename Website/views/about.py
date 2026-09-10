import streamlit as st

from theme import material_icon, page_header


def _card_title(icon_name: str, text: str):
    st.markdown(
        f"##### {material_icon(icon_name, size=18)} {text}",
        unsafe_allow_html=True,
    )




def render_methods():
    with st.container(key="about_methods_page_shell"):

        page_header("About", "Data and methods")

        st.markdown(
            """
            This project investigates long-term changes in **heatwaves and UV
            exposure across Germany and Europe**. The analyses compare temporal
            trends, different location sizes and European regions, and explore
            potential links between UV exposure and public health.
            """
        )

        st.write("")


        c1, c2, c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                _card_title("calendar_month", "Analysis periods")

                st.markdown(
                    """
                    **Heatwave analyses:**  
                    1980–2025

                    **Heatwave reference period:**  
                    1961–1990

                    **UV and health analyses:**  
                    2000–2024
                    """
                )

        with c2:
            with st.container(border=True):
                _card_title("Heatwave","definition")

                st.markdown(
                    """
                    A heatwave requires at least **3 consecutive days** above:

                    - the location-specific **98th-percentile temperature threshold**
                    - an absolute threshold of **28 °C**

                    The percentile threshold is based on the **1961–1990**
                    reference period.
                    """
                )

        with c3:
            with st.container(border=True):
                _card_title("science", "Statistical methods")

                st.markdown(
                    """
                    - Linear regression for long-term trends
                    - 5-year moving averages for visualisation
                    - Kruskal–Wallis tests for selected group comparisons
                    - Statistical significance: **p < 0.05**
                    """
                )

        st.write("")



        st.subheader("Heatwave analysis")

        st.markdown(
            """
            Four main characteristics of heatwaves are analysed throughout the
            project:

            - **Frequency** — how often heatwave events occur
            - **Peak temperature** — the highest temperature reached during a heatwave
            - **Average temperature** — the average temperature during a heatwave
            - **Duration** — the number of consecutive days in a heatwave

            Annual trends are estimated using **linear regression**. The regression
            slope describes the estimated annual change in a metric, while the
            p-value is used to assess whether the observed temporal trend is
            statistically significant.
            """
        )


        st.subheader("Spatial analysis")

        st.markdown(
            """
            The heatwave analyses use different spatial scales to examine whether
            long-term trends depend on location and settlement size.

            **Germany**  
            Major German cities are analysed to identify long-term national heatwave
            trends. A second analysis compares large cities, medium-sized cities,
            small towns and rural municipalities within Germany.

            **Europe**  
            Major European cities are compared to identify broader regional and
            country-level differences in heatwave trends.

            **Italy**  
            Italy is examined in greater detail because it showed the strongest median
            increase in heatwave frequency in the European country comparison.
            Locations of different population sizes are compared to determine whether
            this trend is limited to large cities or also occurs in smaller and rural
            municipalities.
            """
)





        st.subheader("European city selection")

        st.markdown(
            """
            For the European analysis in **RQ3**, cities with at least
            **500,000 inhabitants** were included. National capitals were also
            included when their population was below this threshold.

            Country-level heatwave-frequency trends were calculated from the
            median of the corresponding city-level trends. Countries represented
            by fewer than **3 analysed cities** were excluded from the frequency
            ranking.
            """
        )


        st.subheader("UV and health analysis")

        st.markdown(
            """
            The second part of the project focuses on changes in **UV exposure**
            and their potential public-health relevance.

            UV data are analysed over the period **2000–2024**. For the German
            regional analysis, UV values from selected cities are aggregated to
            the federal-state level using population-weighted averages.

            Health data are used to investigate whether regional patterns in UV
            exposure correspond with selected health outcomes. These analyses
            should be interpreted as associations and do not by themselves
            establish a causal relationship.
            """
        )



        st.subheader("Data sources")

        d1, d2 = st.columns(2)

        with d1:
            with st.container(border=True):
                _card_title("database", "Climate and geographic data")

                st.markdown(
                    """
                    - **Wikidata** — city and population metadata used in city
                      selection
                    - **GeoNames** — geographic and population information used
                      in the German UV analysis
                    - **TEMIS** — UV Index data used for the UV analysis
                    """
                )

        with d2:
            with st.container(border=True):
                _card_title("health_and_safety", "Health data")

                st.markdown(
                    """
                    - **Destatis GENESIS** — German health statistics used in the
                      health-related analysis

                    Detailed preprocessing steps, selection criteria and
                    analysis-specific limitations are described on the
                    corresponding research-question pages and in the project
                    notebooks.
                    """
                )



        st.subheader("Interpreting the results")

        st.markdown(
            """
            A result is treated as **statistically significant when p < 0.05**.

            The 5-year moving averages shown in several visualisations are used
            to make long-term patterns easier to see. Statistical trend tests,
            however, are based on the underlying annual data rather than on the
            smoothed visualisation alone.

            Results should also be interpreted within the scope of the selected
            cities, time periods and heatwave definition. More detailed
            methodological notes are provided within each research question.
            """
        )




def render_info():
    with st.container(key="about_info_page_shell"):

        page_header("About", "Project information")

        st.markdown(
            """
            This interactive website was developed as part of a **Data Science
            project** investigating climate-related changes across Germany and
            Europe.

            The project combines climate, geographic and health-related data with
            statistical analysis and interactive visualisations. The aim is to
            make the results of the six research questions accessible beyond the
            underlying notebooks and code.
            """
        )

        st.write("")


        st.subheader("Project focus")

        st.markdown(
            """
            The project is divided into two main themes:

            **Heatwaves**  
            RQ1–RQ4 investigate how the frequency, intensity and duration of
            heatwaves have changed over time and whether these developments differ
            between cities, rural municipalities and European countries.

            **UV exposure and health**  
            RQ5–RQ6 investigate temporal and regional UV trends and explore their
            potential relevance for public health.
            """
        )



        st.subheader("Research questions")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("##### Heatwaves")

                st.markdown(
                    """
                    **RQ1**  
                    How have the frequency, intensity (peak and average temperature), and duration of heatwaves in major German cities (≥100,000 inhabitants) changed between 1980 and today?

                    **RQ2**  
                    How do heatwave frequency, intensity (peak and average temperature), and duration differ across City sizes, from large cities to rural municipalities, within the same region in Germany?

                    **RQ3**  
                    How have the frequency, intensity (peak and average temperature), and duration of heatwaves in major european cities (≥500,000 inhabitants) changed between 1980 and today?

                    **RQ4**  
                    In the European country most strongly affected by rising heatwave trends, does this effect concentrate in large cities, or is it equally present in smaller cities and rural municipalities?
                    """
                )

        with col2:
            with st.container(border=True):
                st.markdown("##### Heatwaves")

                st.markdown(
                    """
                    **RQ5**  
                    How has the UV Index across Europe changed over the past 20 years, and are there significant temporal and regional trends?

                    **RQ6**  
                    What are the public health implications of rising UV Index trends in highly affected European regions, particularly regarding sunburn risk?
                    """
                )



        st.subheader("How to use this website")

        st.markdown(
            """
            Each research-question page presents the corresponding analysis using
            interactive visualisations, statistical results and a short conclusion.

            Use the navigation menu to move between the six research questions.
            Controls above the charts allow you to explore different metrics such
            as heatwave frequency, temperature and duration.

            The **Data and methods** section provides an overview of the common
            methodology and data sources used throughout the project.
            """
        )



        st.subheader("Project team")

        with st.container(border=True):
            st.markdown("##### Team members")

            st.markdown(
                """
                1. Ahmad-Masih Soltany<br>
                2. Paul Clausen<br>
                3. Timo Stalschus<br>
                4. Mahmood Gutschmidt<br>

        <strong>Course:</strong> Data Science Projekt SS 2026<br>
        <strong>Programme:</strong> BSc Data Science
        """,
        unsafe_allow_html=True,
    )



        st.subheader("Course supervisors")

        with st.container(border=True):
            _card_title("school", "Supervision")

            st.markdown(
                """
                Prof. Peer Kröger  
                Dr. Rükiye Altin  
                Sweety Mohanty  
                Mirjam Bayer

                **Project period:** 17.08.2026 – 11.09.2026
                """
            )

