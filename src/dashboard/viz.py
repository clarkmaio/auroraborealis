

import altair as alt
alt.data_transformers.enable("vegafusion")






def plot_timeseries_heatmap(df):
    '''
    Crea chart altair to visualize monthly average Kp and time series
    df must have 'valuedate', 'Kp' columns
    '''

    df_agg = df.groupby(['year', 'month']).mean().reset_index()

    hover_selection = alt.selection_point(fields=['year', 'month'], nearest=True, on='mouseover', empty='none')

    ts_chart = alt.Chart(df).mark_line().transform_filter(
        hover_selection
    ).encode(
        x=alt.X('valuedate:T', title=''),
        y=alt.Y('Kp:Q', title='Kp'),
        tooltip=['valuedate', 'Kp', 'ap']
    ).properties(
        height=400,
        width='container',
    )


    heatmap_chart = alt.Chart(df_agg).mark_rect(stroke='white').encode(
        x=alt.X('year:O', title=''),
        y=alt.Y('month:O', title=''),
        color=alt.Color('Kp:Q', scale=alt.Scale(scheme='redblue'), legend=None),
        tooltip=['year', 'month', 'Kp']
    ).add_params(
        hover_selection,
    ).properties(
        title='Average Kp'
    )

    chart = ts_chart & heatmap_chart
    return chart