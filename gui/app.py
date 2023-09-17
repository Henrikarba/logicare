# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from background_processes.analysis import read_file, get_trajectories


# Incorporate mock data and specify data viz


def generate_individual_viz(df, x='hours_of_the_day', y='overall_fatigue_values',
                            x_label='hour of the day', y_label='fatigue level (0-10)',
                            title='Fatigue level during the day'):
    fig = px.area(x=df[x], y=df[y], title=title,
                  labels={x: x_label, y: y_label})
    return fig


def generate_overall_viz(df):
    fig = go.Figure([
        go.Scatter(
            name='Overall well-being',
            x=df['hours_of_the_day'],
            y=df['overall_fatigue_values'],
            mode='lines',
            marker=dict(color='#FF8658', size=2),
            line=dict(width=3),
            showlegend=True
        ),
        go.Scatter(
            name='Inference from mouse movement',
            x=df['hours_of_the_day'],
            y=df['mouse_fatigue_values'],
            mode='lines',
            marker=dict(color="#9FC131"),
            line=dict(width=1),
            showlegend=True
        ),
        go.Scatter(
            name='Inference from blinking frequency',
            x=df['hours_of_the_day'],
            y=df['blinking_fatigue_values'],
            marker=dict(color="#77F2FF"),
            line=dict(width=1),
            mode='lines',
            showlegend=True
        ),
        go.Scatter(
            name='Inference from yawning frequency',
            x=df['hours_of_the_day'],
            y=df['yawning_fatigue_values'],
            marker=dict(color="#4B7CCC"),
            line=dict(width=1),
            mode='lines',
            showlegend=True
        )
    ])
    fig.update_layout(
        yaxis_title='Well-being level',
        title='Overall well-being level during the day',
        hovermode="x"
    )
    fig.add_hrect(y0=8, y1=10, line_width=0, fillcolor="red", opacity=0.2,
                  showlegend=True, name='unhealthy status')
    return fig


df = read_file()
df = get_trajectories(df)

time_s = df.groupby(pd.Grouper(key='start', freq='60S')).mean()['stress'].rolling(10, min_periods=3).mean()

data_overall = pd.read_feather('./gui/mock_data/data_overall.feather')
data_mouse = pd.read_feather('./gui/mock_data/data_mouse.feather')
data_blinking = pd.read_feather('./gui/mock_data/data_blinking.feather')
data_yawning = pd.read_feather('./gui/mock_data/data_yawning.feather')
df_merged = data_overall.merge(data_mouse, on='hours_of_the_day', how='inner') \
    .merge(data_blinking, on='hours_of_the_day', how='inner') \
    .merge(data_yawning, on='hours_of_the_day', how='inner')

fig_overall = generate_overall_viz(df_merged)
fig_mouse = generate_individual_viz(time_s, x='start', y='stress',
                                    x_label='hour of the day', y_label='stressed inferred from mouse movement',
                                    title='Fatigue inferred from mouse movement')
fig_blinking = generate_individual_viz(data_blinking, x='hours_of_the_day', y='blinking_fatigue_values',
                                       x_label='hour of the day', y_label='fatigue inferred from blinking frequency',
                                       title='Fatigue inferred from blinking frequency')
fig_yawning = generate_individual_viz(data_yawning, x='hours_of_the_day', y='yawning_fatigue_values',
                                      x_label='hour of the day', y_label='fatigue inferred from yawning frequency',
                                      title='Fatigue inferred from yawning frequency')

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    html.H1(children='LogiCare', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.Tabs(id="tabs-graph", value='overall', children=[
        dcc.Tab(label='Overall fatigue', value='overall'),
        dcc.Tab(label='Inference from mouse movement', value='mouse'),
        dcc.Tab(label='Inference from blinking frequency', value='blinking'),
        dcc.Tab(label='Inference from yawning frequency', value='yawning'),
    ]),
    html.Div(id='tabs-content-example-graph'),
    html.Hr(),
    html.H3(children='Info: what data do we collect?'),
    html.H3(children='Info: where to process & store data?'),
])


@callback(Output('tabs-content-example-graph', 'children'),
          Input('tabs-graph', 'value'))
def render_content(tab):
    if tab == 'overall':
        return html.Div([
            dcc.Graph(figure=fig_overall)
        ])
    elif tab == 'mouse':
        return html.Div([
            dcc.Graph(figure=fig_mouse)
        ])
    elif tab == 'blinking':
        return html.Div([
            dcc.Graph(figure=fig_blinking)
        ])
    elif tab == 'yawning':
        return html.Div([
            dcc.Graph(figure=fig_yawning)
        ])


if __name__ == '__main__':
    app.run(debug=True, port=8050)
