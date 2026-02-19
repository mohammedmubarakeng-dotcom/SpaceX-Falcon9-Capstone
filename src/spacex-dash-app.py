# SpaceX Launch Dashboard Application
# Complete solution for Python 3.11

# Import required libraries
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import os

# Check if dataset exists, if not download it
if not os.path.exists('spacex_launch_dash.csv'):
    import urllib.request
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
    urllib.request.urlretrieve(url, "spacex_launch_dash.csv")
    print("Dataset downloaded successfully!")

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    html.Div([
        html.Label('Select Launch Site:'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
        ),
    ]),
    html.Br(),

    # TASK 2: Add a pie chart
    html.Div([
        html.H3('Launch Success Distribution'),
        dcc.Graph(id='success-pie-chart')
    ]),
    html.Br(),

    # TASK 3: Add a slider to select payload range
    html.Div([
        html.Label('Payload Range (Kg):'),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[int(min_payload), int(max_payload)],
            marks={i: f'{i}' for i in range(0, 10001, 2000)}
        ),
    ]),
    html.Br(),

    # TASK 4: Add a scatter chart
    html.Div([
        html.H3('Payload vs Launch Outcome'),
        dcc.Graph(id='success-payload-scatter-chart')
    ]),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # For all sites, show total success launches count by site
        site_success = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='count')
        fig = px.pie(
            site_success, 
            values='count', 
            names='Launch Site',
            title='Total Successful Launches By Site',
            hole=0.3
        )
        return fig
    else:
        # For specific site, show success vs failed counts
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = site_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        success_counts['outcome'] = success_counts['class'].map({1: 'Success', 0: 'Failed'})
        
        fig = px.pie(
            success_counts,
            values='count',
            names='outcome',
            title=f'Success vs Failed Launches for {entered_site}',
            color='outcome',
            color_discrete_map={'Success': 'green', 'Failed': 'red'},
            hole=0.3
        )
        return fig

# TASK 4: Callback for scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    
    # Filter by payload range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[mask]
        title = 'Correlation between Payload and Success for all Sites'
    else:
        site_mask = mask & (spacex_df['Launch Site'] == entered_site)
        filtered_df = spacex_df[site_mask]
        title = f'Correlation between Payload and Success for {entered_site}'
    
    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title,
        labels={'class': 'Launch Outcome (1=Success, 0=Failure)'},
        hover_data=['Launch Site'],
        opacity=0.7
    )
    
    # Add some styling
    fig.update_traces(marker=dict(size=10))
    fig.update_yaxis(tickmode='array', tickvals=[0, 1], ticktext=['Failure', 'Success'])
    
    return fig

# Run the app
if __name__ == '__main__':
    print("\n" + "="*50)
    print("Starting SpaceX Dashboard...")
    print("The dashboard will be available at: http://127.0.0.1:8050/")
    print("="*50)
    print("\nTo access the dashboard:")
    print("1. Look for 'Dash is running on http://127.0.0.1:8050/' in the output")
    print("2. Click that link or copy it to a new browser tab")
    print("3. In the lab interface, click 'Others' → 'Launch Application' → Enter port 8050")
    print("\n" + "="*50)
    
    app.run_server(port=8050, debug=False, host='0.0.0.0')