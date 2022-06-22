from dataclasses import dataclass
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import matplotlib.pyplot as plt

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
        self.raw_data = self.data.copy()

    def generate_dashboard(self):
        self.side_bar()
        self.main_page()


    def side_bar(self):
        '''
        Create side bar elements
        '''

        st.sidebar.markdown("## Sidebar")

        st.sidebar.markdown("#")
        self.resolution = st.sidebar.selectbox(label = 'Resolution', options=['YS','H', 'D','MS'], index=0)

        # Dwonload data
        st.sidebar.download_button(label='Download data', key='download', data=self.convert_df(self.data), file_name='AuroraBoralis.csv', mime='text/csv')



    def main_page(self):
        '''
        Create main page
        '''

        # self.title('Aurora Borealis', background_color='aquamarine')
        st.markdown('# Aurora borealis')

        self._preprocess_data()

        st.markdown('#')
        self._display_plot_timeseries()

        self._display_plot_scatter()
        self._display_plot_monthly_seasonality()
        self._display_plot_yearly_acf_pacf()


    def _preprocess_data(self):
        '''Format data according to input params'''
        self.data = self.data.resample(self.resolution).mean()


    def _display_plot_timeseries(self):
        '''
        Plot timeseries Kp, Ap
        '''

        fig = make_subplots(rows=2, cols=1, subplot_titles=['Kp', 'Ap'], shared_xaxes=True)

        fig.add_trace(
            go.Scattergl(x=self.data.index, y=self.data['Kp'],
                       mode='lines',
                       name='Kp',
                       line={'color': 'blue'}),
            row=1, col=1
        )

        fig.add_trace(
            go.Scattergl(x=self.data.index, y=self.data['ap'],
                       mode='lines',
                       name='Ap',
                       line={'color': 'red'}),
            row=2, col=1
        )

        # display
        st.plotly_chart(fig, use_container_width=True)




    def _display_plot_scatter(self):
        '''Plot scatter Kp/Ap'''
        fig = px.scatter(self.data, x='Kp', y='ap', title='Kp-Ap scatter')
        st.plotly_chart(fig, use_container_width=True, render_mode='webgl')

    def _display_plot_monthly_seasonality(self):
        '''Plot monthly seasonality'''

        data_month = self.raw_data.copy()
        data_month['month'] = data_month.index.month
        data_month = data_month.groupby('month').mean()

        fig = make_subplots(specs=[[{'secondary_y': True}]], subplot_titles=['Monthly seasonality'])
        fig.add_trace(
            go.Scatter(x=data_month.index, y=data_month['Kp'], name='Kp', line={'color': 'blue'}),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(x=data_month.index, y=data_month['ap'], name='Ap', line={'color': 'red'}),
            secondary_y=True
        )

        # x axis label
        fig.update_xaxes(title_text='Month')

        # y axis label
        fig.update_yaxes(title_text='Kp', secondary_y=False)
        fig.update_yaxes(title_text='Ap', secondary_y=True)

        # Render
        st.plotly_chart(fig, use_container_width=True)


    def _display_plot_yearly_acf_pacf(self):
        '''Plot yearly pacf'''

        data_year = self.raw_data.resample('Y').mean()

        # Plot
        fig, ax = plt.subplots(2, 1, sharex=True)
        plot_pacf(x=data_year['Kp'], ax=ax[0])
        ax[0].set_title('PACF Kp', fontweight='bold')
        ax[0].grid(linestyle=':')

        plot_acf(x=data_year['Kp'], ax=ax[1])
        ax[1].set_title('ACF Kp', fontweight='bold')
        ax[1].grid(linestyle=':')

        # Render
        st.pyplot(fig=fig)



    def title(self, text: str, background_color: str = 'tomato', text_color: str = 'white') -> None:
        st.markdown(f"<h1 style='text-align: center; color: {text_color}; background-color: {background_color}'>{text}</h1>", unsafe_allow_html=True)

    @st.cache
    def convert_df(self, df: pd.DataFrame):
        return df.to_csv().encode('utf-8')



if __name__ == '__main__':

    dashboard = DashBoard(layout = "wide")
    dashboard.generate_dashboard()

