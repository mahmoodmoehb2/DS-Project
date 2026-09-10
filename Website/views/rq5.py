from views import rq_placeholder
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import linregress

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
    regional = (df.groupby(["region", "year"])["mean_uvi"].mean().reset_index())
    europe_data = (df.groupby("year")["mean_uvi"].mean().reset_index())
    cointainer_visualisation_trends = st.empty()
    with cointainer_visualisation_trends: 
        fig = px.line(europe_data,x="year",y="mean_uvi",markers=True,title="UV Index Trend in Europe")
        st.plotly_chart(fig, use_container_width=True)
    
      
      
       
    
    europe,north_europe,east_europe,south_europe,west_europe=st.columns(5)
    with europe:
       if st.button("Europe"):
        europe_plot = px.line(europe_data,x="year",y="mean_uvi",markers=True,title="UV Index Trend in Europe")
        st.plotly_chart(europe_plot, use_container_width=True)
    with north_europe:
            if st.button("North-Europe"):
               north_europe_plot = px.line(regional[regional["region"] == "Northern Europe"],x="year",y="mean_uvi",markers=True,title="UV Index Trend in Northern Europe")
               st.plotly_chart(north_europe_plot,use_container_width=True)
                
    with east_europe:
            if st.button("East-Europe"):
                east_europe_plot = px.line(regional[regional["region"] == "Eastern Europe"],x="year",y="mean_uvi",markers=True,title="UV Index Trend in Eastern Europe")
                st.plotly_chart(east_europe_plot,use_container_width=True)
    with south_europe:
               if st.button("South-Europe"):
                    south_europe_plot = px.line(regional[regional["region"] == "Southernstern Europe"],x="year",y="mean_uvi",markers=True,title="UV Index Trend in Southern Europe")
                    st.plotly_chart(south_europe_plot,use_container_width=True)
    with west_europe:
            if st.button("West-Europe"):
                west_europe_plot = px.line(regional[regional["region"] == "Western Europe"],x="year",y="mean_uvi",markers=True,title="UV Index Trend in Western Europe")
                st.plotly_chart(west_europe_plot,use_container_width=True)
    
   
        
    
        
    
    
    
    
    
  
        
            
        
    
        
        
        
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
            
            
        
        
        

    
        

    