import panel as pn
import holoviews as hv
from src import DataScraper
import numpy as np

# Load data
print("Loading data...")
df = DataScraper().load_data().reset_index()

pn.extension(sizing_mode="stretch_width")

print("Building dashboard...")
plot = hv.Curve(df.reset_index(), 'valuedate', 'Kp')
module_plot = pn.panel(plot, sizing_mode="stretch_both")

# ------------------------------ DISTRIBUTION PLOT ------------------------------
years = sorted(df['valuedate'].dt.year.unique())
year_select = pn.widgets.Select(name='Select Year', options=years, value=years[-])

@pn.depends(year_select.param.value)
def plot_distribution(selected_year):
    df_year = df[df['valuedate'].dt.year == selected_year]
    plot = hv.Histogram(np.histogram(df_year['Kp'], bins=30), kdims='Kp')
    plot_all_history = hv.Histogram(np.histogram(df['Kp'], bins=30), kdims='Kp')

    # Plot both plots
    plot_all_history.opts(alpha=0.5, color='blue', title='All history')
    plot.opts(alpha=0.5, color='red', title=f'Year {selected_year}')
    plot_all_history = plot_all_history.opts(alpha=0.5, color='blue', title='All history')
    plot = plot.opts(alpha=0.5, color='red', title=f'Year {selected_year}')
    plot = (plot_all_history * plot).opts(title=f'Kp Distribution for year {selected_year}')

    # In the tile set year select and plot
    tile = pn.Column(year_select, plot)
    return plot


template = pn.template.FastGridTemplate(site="Panel", title="App", prevent_collision=True)
template.sidebar.append(year_select)
template.main[0:2,0:12]=module_plot
template.main[2:4,0:6] = plot_distribution
template.servable()