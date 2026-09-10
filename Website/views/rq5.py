from views import rq_placeholder
import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import linregress
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _render_rq5_content():
    st.markdown('<div class="eyebrow">RQ5 · UV Index · Europe</div>', unsafe_allow_html=True)

    st.title("Do heatwaves differ by city size in Germany?")

    st.markdown(
        """
        **Research question:** How has the UV Index across Europe changed over the past 20
        years, and are there significant temporal and regional trends?
        """
    )
    st.subheader("UV Index in the European cities")
    df = pd.read_csv(DATA_DIR / "RQ5_uvIndex.csv")
   
    result = [] 
    
    cointainer_visualisation = st.empty()
   
    information_about_uv_box = st.empty()
    with information_about_uv_box:
         st.subheader(f"Information on the UV-Index in 2000")
    with cointainer_visualisation:
       for _, row in df.iterrows():
            if row["year"]==2000:
                result.append(row)
       render_new_container(cointainer_visualisation, 2000,result,information_about_uv_box)
    
    #creates ten columnes
    col0,col1,col2,col3,col4,col5,col6,col7,col8,col9= st.columns(10)
    #buttons for the years with ending 0
    with col0:
            if st.button("2000"):
                
                result=[]
                for _, row in df.iterrows():
                    if row["year"]==2000:
                        result.append(row)
                render_new_container(cointainer_visualisation, 2000,result,information_about_uv_box)

            if st.button("2010"):
                
                result=[]
                for _, row in df.iterrows():
                    if row["year"]==2010:
                        result.append(row)
                render_new_container(cointainer_visualisation, 2010,result,information_about_uv_box)
            if st.button("2020"):
                 result=[]
                 for _, row in df.iterrows():
                    if row["year"]==2020:
                        result.append(row)
                 render_new_container(cointainer_visualisation, 2020,result,information_about_uv_box)
    #buttons for the years with ending 1
    with col1:
        if st.button("2001"):
            result=[]
            for _, row in df.iterrows():
                if row["year"]==2001:
                    result.append(row)
            render_new_container(cointainer_visualisation, 2001,result,information_about_uv_box)
        if st.button("2011"):
             result=[]
             for _, row in df.iterrows():
              if row["year"]==2011:
                result.append(row)
             render_new_container(cointainer_visualisation, 2011,result,information_about_uv_box)           
        if st.button("2021"):
             result=[]
             for _, row in df.iterrows():
              if row["year"]==2021:
                result.append(row)
             render_new_container(cointainer_visualisation, 2021,result,information_about_uv_box)
    #buttons for the years with ending 2
    with col2:
        if st.button("2002"):
            result=[]
            for _, row in df.iterrows():
                if row["year"]==2002:
                    result.append(row)
            render_new_container(cointainer_visualisation, 2002,result,information_about_uv_box)
        if st.button("2012"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2012:
                 result.append(row)
             render_new_container(cointainer_visualisation, 2012,result,information_about_uv_box)
        if st.button("2022"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2022:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2022,result,information_about_uv_box)
   #buttons for the years with ending 3
    with col3:
        if st.button("2003"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2003:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2003,result,information_about_uv_box)
        if st.button("2013"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2013:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2013,result,information_about_uv_box)
        if st.button("2023"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2023:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2023,result,information_about_uv_box)
    #buttons for the years with ending 4
    with col4:
        if st.button("2004"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2004:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2004,result,information_about_uv_box)
        if st.button("2014"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2014:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2014,result,information_about_uv_box)
        if st.button("2024"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2024:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2024,result,information_about_uv_box)
    #buttons for the years with ending 5
    with col5:
        if st.button("2005"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2005:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2005,result,information_about_uv_box)
        if  st.button("2015"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2015:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2015,result,information_about_uv_box)
        if st.button("2025"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2025:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2025,result,information_about_uv_box)
    #buttons for the years with ending 6            
    with col6:
            if st.button("2006"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2006:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2006,result,information_about_uv_box)
            if st.button("2016"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2016:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2016,result,information_about_uv_box)
            
    #buttons for the years with ending 7        
    with col7:
            if st.button("2007"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2007:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2007,result,information_about_uv_box)
            if st.button("2017"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2017:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2017,result,information_about_uv_box)
    #buttons for the years with ending 8    
    with col8:
        if  st.button("2008"):
            result=[]
            for _, row in df.iterrows():
                if row["year"]==2008:
                    result.append(row)
            render_new_container(cointainer_visualisation, 2008,result,information_about_uv_box)
        if st.button("2018"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2018:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2018,result,information_about_uv_box)       
    #buttons for the years with ending 9        
    with col9:
            if st.button("2009"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2009:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2009,result,information_about_uv_box)
            if st.button("2019"):
             result=[]
             for _, row in df.iterrows():
                if row["year"]==2019:
                    result.append(row)
             render_new_container(cointainer_visualisation, 2019,result,information_about_uv_box)
    st.subheader("Trend UV")
    
    df_trends = pd.read_csv(DATA_DIR / "RQ5_trends.csv")
    regional = df.groupby(["region", "year"])["mean_uvi"].mean().reset_index()
    europe_data = df.groupby("year")["mean_uvi"].mean().reset_index()

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = "Europe"

    with st.container():
        st.markdown("### Select region")

        # Region buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Europe", key="trend_europe"):
                st.session_state.selected_region = "Europe"

        with col2:
            if st.button("East Europe", key="trend_east"):
                st.session_state.selected_region = "Eastern Europe"

        with col3:
            if st.button("South Europe", key="trend_south"):
                st.session_state.selected_region = "Southern Europe"

        with col4:
            if st.button("West Europe", key="trend_west"):
                st.session_state.selected_region = "Western Europe"

        selected_region = st.session_state.selected_region

        # Select data
        if selected_region == "Europe":
            plot_data = europe_data
            plot_title = "UV Index Trend in Europe"

        else:
            plot_data = regional[regional["region"] == selected_region]
            plot_title = f"UV Index Trend in {selected_region}"

        # Trend plot
        fig = px.line(plot_data, x="year", y="mean_uvi", markers=True, title=plot_title)

        st.plotly_chart(fig, use_container_width=True, key="rq5_trend_plot")

        

        st.markdown(
            """
            <div style="
                background-color: #ffebee;
                border: 2px solid #d32f2f;
                border-radius: 12px;
                padding: 20px;
                margin-top: 25px;
            ">
                <strong style="color: #b71c1c;">
                    Statistical Significance
                </strong>
                <p style="margin-bottom: 0;">
                    The observed trend is not statistically significant.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

     

        st.markdown(
            """
            <div style="
                background-color: #f5f5f5;
                border: 1px solid #cccccc;
                border-radius: 12px;
                padding: 20px;
                margin-top: 15px;
            ">
                <strong>
                    Interpretation
                </strong>
                <p style="margin-bottom: 0;">
                    The charts illustrate the temporal and regional development of the UV Index across European cities.
                The Mean UV Index represents the average UV Index for a city over the respective year. It provides an overall measure of typical UV exposure rather than showing individual daily peaks.
                For the Europe-wide chart, these city-level mean UV Index values were averaged across all included European cities for each year. For the regional charts, they were averaged across all cities belonging to the selected region for each year.
                The UV Index data were obtained from TEMIS, while GeoNames was used to identify European cities and provide their geographic information.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
   
        
    
        
    
    
    
    
    
  
        
            
        
    
        
        
        
# This Function creates a Container and render the context of the page inside of it 
def render():
    with st.container(key="rq5_page_shell"):
        _render_rq5_content()

def render_new_container(container, year,dataframe,information_box):
    with container.container():
        st.write(f"Informatiion on UV Index in {year}")
        data= pd.DataFrame(dataframe)
        
        st.bar_chart(data,x="city",y="mean_uvi")
    with information_box.container():
        st.subheader(f"UV Index {year}")
        title,information=st.columns(2)
        
        
        with title:
            st.write("MEAN UV:")
            st.write("MAX MEAN UV: ")
            st.write("MIN MEAN UV: ")
        with information:
            
            data= pd.DataFrame(dataframe)
            st.write(f"{data['mean_uvi'].mean():.2f}")
            st.write(f"{data['mean_uvi'].max():.2f}")
            st.write(f"{data['mean_uvi'].min():.2f}")
            
            
        
        
        

    
        

    