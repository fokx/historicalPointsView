import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sqlite3

conn = sqlite3.connect('../sync_daemon/points.db')
c = conn.cursor()
# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

# fig = go.Figure()  # or any Plotly Express function e.g. px.bar(...)
# # fig.add_trace( ... )
# # fig.update_layout( ... )
# df = px.data.gapminder().query("continent=='Oceania'")
# fig = px.line(df, x="year", y="lifeExp", color='country')
# fig.show()


# Create traces
fig = go.Figure()
N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                    mode='lines',
                    name='lines'))

external_stylesheets = ["/assets/bWLwgP.css"]
app = dash.Dash( external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Label('Time scale'),
    dcc.RadioItems(options=[
            {'label': 'Last 1h', 'value': 'last_hour'},
            {'label': 'Last 24h', 'value': 'last_day'},
            {'label': 'Last week', 'value': 'last_week'},
            {'label': 'Last month', 'value': 'last_month'}],
            value='last_hour',
            id = "time_scale",
labelStyle={'display': 'inline-block'}
         # style = {"padding": "10px", "max-width": "800px", "margin": "auto"}
),
    dcc.Graph(figure=fig),

html.Div([
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '80%'}),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
])



@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('time_scale', 'value')     ])
def update_x_timeseries(time_scale):
    if time_scale == "last_hour":
        time.datetime
    elif time_scale=='last_day':
        pass
    elif time_scale=='last_week':
        pass
    elif time_scale=="last_month":
        xdata=list(range(1,))
        ydata=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
               350, 430, 474, 526, 488, 537, 500, 439][:12]
        title="a month"
        return create_time_series(xdata,ydata,title)


def create_time_series(xdata, ydata, title):
    return {
        'data': [dict(
            x=xdata,
            y=ydata,
            name='temperature',
            marker=dict(
                color='rgb(55, 83, 109)'
            )
            # mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' },
            'xaxis': {'showgrid': False}
        }
    }

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False,port=30001, host="0.0.0.0")  # Turn off reloader if inside Jupyter
