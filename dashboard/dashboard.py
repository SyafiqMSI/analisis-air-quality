import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df

df = load_data()

def get_season(month):
    if month in [11, 12, 1, 2, 3]:
        return 'Rainy'
    else:
        return 'Dry'

df['season'] = df['month'].apply(get_season)

def categorize_pollution(row):
    if row['PM2.5'] < 12 and row['PM10'] < 20:
        return 'Low'
    elif (12 <= row['PM2.5'] < 35) and (20 <= row['PM10'] < 50):
        return 'Medium'
    else:
        return 'High'

df['Pollution_Level'] = df.apply(categorize_pollution, axis=1)

st.title("Stations Air Quality Analysis Dashboard")

with st.sidebar:
    st.header("Main Filters")
    selected_years = st.multiselect(
        "Select Years",
        options=sorted(df['year'].unique()),
        default=sorted(df['year'].unique())
    )
    
    selected_stations = st.multiselect(
        "Select Stations",
        options=df['station'].unique(),
        default=df['station'].unique()
    )

filtered_df = df[(df['station'].isin(selected_stations)) & (df['year'].isin(selected_years))]

if len(filtered_df) == 0:
    st.warning("Tidak ada data yang ditampilkan, silahkan pilih stasiun dan tahun terlebih dahulu.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average PM2.5", f"{filtered_df['PM2.5'].mean():.2f} µg/m³")
    with col2:
        st.metric("Average PM10", f"{filtered_df['PM10'].mean():.2f} µg/m³")
    with col3:
        st.metric("Average Temperature", f"{filtered_df['TEMP'].mean():.2f}°C")
    with col4:
        st.metric("Average Wind Speed", f"{filtered_df['WSPM'].mean():.2f} m/s")

    tab1, tab2, tab3, tab4 = st.tabs(["PM Analysis", "Seasonal Analysis", "Temperature Analysis", "Wind Analysis"])

    with tab1:
        st.header("PM2.5 and PM10 Analysis")
        
        with st.sidebar:
            st.header("PM Filters")
            pm_aggregation = st.selectbox(
                "Select Aggregation",
                options=['Mean', 'Median', 'Max', 'Min'],
                key='pm_agg'
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            if pm_aggregation == 'Mean':
                sns.barplot(x='station', y='PM2.5', data=filtered_df, ax=ax)
            elif pm_aggregation == 'Median':
                sns.boxplot(x='station', y='PM2.5', data=filtered_df, ax=ax)
            elif pm_aggregation == 'Max':
                sns.barplot(x='station', y='PM2.5', data=filtered_df, estimator=max, ax=ax)
            else:
                sns.barplot(x='station', y='PM2.5', data=filtered_df, estimator=min, ax=ax)
            plt.xticks(rotation=45)
            plt.title(f'PM2.5 by Station ({pm_aggregation})')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            if pm_aggregation == 'Mean':
                sns.barplot(x='station', y='PM10', data=filtered_df, ax=ax)
            elif pm_aggregation == 'Median':
                sns.boxplot(x='station', y='PM10', data=filtered_df, ax=ax)
            elif pm_aggregation == 'Max':
                sns.barplot(x='station', y='PM10', data=filtered_df, estimator=max, ax=ax)
            else:
                sns.barplot(x='station', y='PM10', data=filtered_df, estimator=min, ax=ax)
            plt.xticks(rotation=45)
            plt.title(f'PM10 by Station ({pm_aggregation})')
            st.pyplot(fig)

    with tab2:
        st.header("Seasonal Analysis")
        
        with st.sidebar:
            st.header("Seasonal Filters")
            selected_season = st.selectbox(
                "Select Season",
                options=['All', 'Rainy', 'Dry']
            )
        
        season_df = filtered_df if selected_season == 'All' else filtered_df[filtered_df['season'] == selected_season]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='season', y='PM2.5', data=season_df, ax=ax)
            plt.title('PM2.5 Distribution by Season')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='season', y='PM10', data=season_df, ax=ax)
            plt.title('PM10 Distribution by Season')
            st.pyplot(fig)

    with tab3:
        st.header("Temperature Analysis")
        
        if not filtered_df.empty:
            with st.sidebar:
                st.header("Temperature Filters")
                temp_min = float(filtered_df['TEMP'].min())
                temp_max = float(filtered_df['TEMP'].max())
                if temp_min != temp_max:
                    temp_range = st.slider(
                        "Select Temperature Range",
                        temp_min, temp_max,
                        (temp_min, temp_max)
                    )
                    temp_df = filtered_df[(filtered_df['TEMP'] >= temp_range[0]) & 
                                         (filtered_df['TEMP'] <= temp_range[1])]
                else:
                    st.warning(f"Hanya satu nilai suhu ({temp_min}°C) yang tersedia untuk stasiun yang dipilih.")
                    temp_df = filtered_df
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='TEMP', y='PM2.5', data=temp_df, ax=ax)
                plt.title('Temperature vs PM2.5')
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='TEMP', y='PM10', data=temp_df, ax=ax)
                plt.title('Temperature vs PM10')
                st.pyplot(fig)

    with tab4:
        st.header("Wind Analysis")
        
        if not filtered_df.empty:
            with st.sidebar:
                st.header("Wind Filters")
                wind_min = float(filtered_df['WSPM'].min())
                wind_max = float(filtered_df['WSPM'].max())
                if wind_min != wind_max:
                    wind_range = st.slider(
                        "Select Wind Speed Range",
                        wind_min, wind_max,
                        (wind_min, wind_max)
                    )
                    wind_df = filtered_df[(filtered_df['WSPM'] >= wind_range[0]) & 
                                         (filtered_df['WSPM'] <= wind_range[1])]
                else:
                    st.warning(f"Hanya satu nilai kecepatan angin ({wind_min} m/s) yang tersedia untuk stasiun yang dipilih.")
                    wind_df = filtered_df
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='WSPM', y='PM2.5', data=wind_df, ax=ax)
                plt.title('Wind Speed vs PM2.5')
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='WSPM', y='PM10', data=wind_df, ax=ax)
                plt.title('Wind Speed vs PM10')
                st.pyplot(fig)

    if st.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.dataframe(filtered_df)

st.markdown("---")
st.markdown("Dashboard created with Streamlit by Muhammad Syafiq Ibrahim")