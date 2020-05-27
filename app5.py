import sqlite3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# c = conn.cursor()
# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# Save (commit) the changes
# conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
# conn.close()

# fig = go.Figure()  # or any Plotly Express function e.g. px.bar(...)
# # fig.add_trace( ... )
# # fig.update_layout( ... )
# df = px.data.gapminder().query("continent=='Oceania'")
# fig = px.line(df, x="year", y="lifeExp", color='country')
# fig.show()

id_of_line_chart = "the_single_line_chart"
id_of_radio_items = "id_time_scale"

radio_items_list = [{'label': 'Last 60s', 'value': 'last_minute'},
                    {'label': 'Last 1h', 'value': 'last_hour'},
                    {'label': 'Last 24h', 'value': 'last_day'},
                    {'label': 'Last week', 'value': 'last_week'},
                    {'label': 'Last month', 'value': 'last_month'}]
radio_items = {i['value'] for i in radio_items_list}

external_stylesheets = ["/assets/bWLwgP.css"]
app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Label('Time scale'),
    dcc.RadioItems(options=radio_items_list,
                   value='last_hour',
                   id=id_of_radio_items,
                   labelStyle={'display': 'inline-block'}
                   # style = {"padding": "10px", "max-width": "800px", "margin": "auto"}
                   ),
    html.Div([
        dcc.Graph(id=id_of_line_chart),
    ], style={'display': 'inline-block', 'width': '80%'}),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
])


@app.callback(dash.dependencies.Output(id_of_line_chart, 'figure'),
              [dash.dependencies.Input(id_of_radio_items, 'value')])
def make_pie_chart(value):
    assert value in radio_items  # {'last_month', 'last_minute', 'last_day', 'last_hour', 'last_week'}
    if value == 'last_hour':
        conn = sqlite3.connect('../sync_daemon/points.db')
        df = pd.read_sql_query(
            "SELECT  * FROM point WHERE datetime(timestamp) "
            " >= datetime('now', '{}')".format(
                "-3 hours"), conn)
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = df['timestamp'].dt.tz_localize('utc').dt.tz_convert('Asia/Hong_Kong')

        fig = px.line(df, x='timestamp', y='point')
        fig.update_layout({
            'xaxis': {'type': 'date',
                      # 'tick0': df['timestamp'][0],
                      # 'tickmode': 'linear',
                      # 'dtick': 86400000.0 * 14,
                      'showgrid': True}
            # 'height': 225,
            # 'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            # 'annotations': [{
            #     'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
            #     'xref': 'paper', 'yref': 'paper', 'showarrow': False,
            #     'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
            #     'text': "last 1 hour"
            # }],
            # 'yaxis': {'type': 'linear'}
        })

        return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=30001, host="0.0.0.0")  # Turn off reloader if inside Jupyter
