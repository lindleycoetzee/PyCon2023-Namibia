import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash_table import DataTable

df = pd.read_csv("all_matches_2012-2021.csv")
df = df.rename(columns={"striker": "batsman", "runs_off_bat" : "runs", "season": "year"})
df = df.loc[df["innings"] <= 2]

#Top run scorers overall
top_scorers_ovr = df[["year", "batsman", "runs"]]
top_scorers_ovr = top_scorers_ovr.groupby(by=["batsman"]).sum().\
    sort_values(by=["runs"], ascending=False)

#Top 10 run scorers overall
top_scorers_ovr = top_scorers_ovr.reset_index()
top_10_run_getters = top_scorers_ovr[["batsman","runs"]][:10]

# create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

app.layout = html.Div([
    html.Center([html.H1("My cricket dashboard webapp")]),
    html.Center([html.H2("IPL stats")]),
    html.Br(),

    dbc.Row([

        dbc.Col([
            html.Br(),
            html.Center(html.H5("Most runs overall")),
            html.Center("Select the number of batsman"),

            dcc.Slider(id='n_batsman_slider_ovr',
                       min=0,
                       max=50,
                       step=5,
                       value=10,
                       marks={year: {'label': str(year)} for year in range(0, 51, 5)},
                       included=False,
                       ),
            dcc.Graph(id='top_runs_chart_ovr'),

        ], lg=8, md=12),

        dbc.Col([
            html.Br(),

            html.Center("This section shows the all time IPL top runs scorers for the period 2008 - 2021"),
            html.Center("Top 10 run getters for the period 2008 - 2021"),

            DataTable(data=top_10_run_getters.to_dict("records"),
                      columns=[{"name": col, "id": col} for col in top_10_run_getters.columns],
                      style_cell={"textAlign": "left", },
                      style_cell_conditional=[{'if': {'column_id': 'batsman'}, 'width': '80px'},
                                              {'if': {'column_id': 'runs'}, 'width': '80px'}, ],
                      style_header={"backgroundColor": "rgb(99,110,250)"},
                      css=[{
                          'selector': '.dash-spreadsheet-container',
                          'rule': 'padding: 10px 30px 30px 30px; overflow: hidden;'
                      }],

                      ),

        ], lg=4, md=12),
    ])
])

@app.callback(Output('top_runs_chart_ovr', 'figure'),
              Input('n_batsman_slider_ovr', 'value'))
def plot_runs_by_batsman_chart_ovr(n_batsman):
    layout = go.Layout(
        height=400,
    )
    fig = go.Figure(layout=layout)
    dff = top_scorers_ovr[:n_batsman]
    fig.add_bar(x= dff["batsman"],
                y= dff["runs"])
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
