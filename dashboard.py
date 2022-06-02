from dataclasses import dataclass
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

import plotly.figure_factory as ff
import plotly.express as px

from data_scraper import DataScraper


@dataclass
class DashBoard():
    layout: str = "centered"

    def __post_init__(self):
        st.set_page_config(layout=self.layout)

        self.load_data()
        return

    #@st.cache
    def load_data(self):
        data_scraper = DataScraper()
        self.data = data_scraper.load_data()

    def generate_dashboard(self):
        self.side_bar()
        self.main_page()


    def side_bar(self):
        '''
        Create side bar elements
        '''

        st.sidebar.markdown("## Sidebar")
        self.train_test_split_date = st.sidebar.date_input(label = 'Train/test split', value=datetime(2020, 1, 1))
        self.train_test_split_date = pd.to_datetime(self.train_test_split_date)


        st.sidebar.markdown("#")
        self.resolution = st.sidebar.selectbox(label = 'Resolution', options=['YS','H', 'D','MS'])

        st.sidebar.markdown("#")
        if st.sidebar.button(label='Run model'):
            st.sidebar.write('Run')




    def main_page(self):
        '''
        Create main page
        '''

        self.title('Aurora Borealis', background_color='aquamarine')

        st.markdown('#')
        self.train_test_split()

        self._display_plot_timeseries()


    def _preprocess(self):
        '''Format data according to input params'''
        self.data = self.data.resample(self.resolution).mean()


    def train_test_split(self):
        self._preprocess()
        self.X_train = self.data.loc[self.data.index < self.train_test_split_date, ['Kp']]
        self.X_test = self.data.loc[self.data.index >= self.train_test_split_date, ['Kp']]


    def _display_plot_timeseries(self):
        # Generate plot
        fig = px.line(self.data, y=['Kp'])
        fig.update_xaxes(rangeslider_visible=True)

        # display
        st.plotly_chart(fig, use_container_width=True)



    def title(self, text: str, background_color: str = 'tomato', text_color: str = 'white') -> None:
        st.markdown(f"<h1 style='text-align: center; color: {text_color}; background-color: {background_color}'>{text}</h1>", unsafe_allow_html=True)






if __name__ == '__main__':

    dashboard = DashBoard(layout = "wide")
    dashboard.generate_dashboard()

