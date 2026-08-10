# Import required libraries

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the SpaceX data into pandas dataframe

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a Dash application

app = dash.Dash(__name__)


# Create an app layout

app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Dropdown for Launch Site selection

    html.Br(),

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart

    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # TASK 3: Payload range slider

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=100,
        marks={
            int(min_payload): str(int(min_payload)),
            int(max_payload): str(int(max_payload))
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter chart

    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )
])


# TASK 2:
# Callback for site-dropdown -> success-pie-chart

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(entered_site):

    # If ALL sites are selected
    if entered_site == 'ALL':

        pie_df = spacex_df.copy()

        pie_df['Outcome'] = pie_df['class'].map({
            0: 'Failure',
            1: 'Success'
        })

        fig = px.pie(
            pie_df,
            names='Outcome',
            title='Total Launch Outcomes'
        )

    # If a specific site is selected
    else:

        pie_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ].copy()

        pie_df['Outcome'] = pie_df['class'].map({
            0: 'Failure',
            1: 'Success'
        })

        fig = px.pie(
            pie_df,
            names='Outcome',
            title=f'Launch Outcomes for {entered_site}'
        )

    return fig


# TASK 4:
# Callback for site-dropdown + payload-slider
# -> success-payload-scatter-chart

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_chart(entered_site, payload_range):

    # If ALL sites are selected
    if entered_site == 'ALL':

        filtered_df = spacex_df

    # If a specific site is selected
    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

    # Filter by payload range

    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    # Create scatter plot

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs. Launch Success'
    )

    return fig


# Run the app

if __name__ == '__main__':
    print("Starting Dash app...")
    app.run(debug=True)