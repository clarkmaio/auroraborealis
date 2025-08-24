


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))


import streamlit as st
from src.data.scraper import DataScraper
from src.dashboard.viz import plot_timeseries_heatmap

st.title('Aurora Borealis Dashboard')



df = DataScraper().load_data()
df['year'] = df['valuedate'].dt.year
df['month'] = df['valuedate'].dt.month


chart = plot_timeseries_heatmap(df)
st.altair_chart(chart, use_container_width=True)