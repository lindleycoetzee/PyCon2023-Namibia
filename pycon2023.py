import dash
import dash.html as html
import dash_bootstrap_components as dbc
import dash.dcc as dcc
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Output, Input

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
app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

# create layout
app.layout = html.Div([

    html.Center(html.H1("PyCon2023 Namibia")),
    html.Center(html.H2("IPL batting stats")),

    dbc.Row([

        dbc.Col([

            html.Center("Most runs in the IPL"),
            html.Center("Select the number of batsman"),

            dcc.Slider(0,50,5,
                       value=15,
                       id="most_runs_slider"),

            dcc.Graph(id="most_runs_graph"),

        ]),

        dbc.Col([

            html.Center("Dropdown"),

            dcc.Dropdown(options=[{"label" : year, "value": year} for year in range(2015,2024)],
                         value=2021)

        ]),

    ]),

])

# create callback function
@app.callback(Output(component_id="most_runs_graph", component_property="figure"),
              Input(component_id="most_runs_slider", component_property="value"))
def plot_most_runs_graph(n_batsmen):
    graph_layout = go.Layout(
        height = 400,
    )
    fig = go.Figure(layout=graph_layout)
    dff = top_scorers_ovr[:n_batsmen]
    fig.add_bar(x = dff["batsman"],
                y = dff["runs"])

    return fig


# run app
app.run(debug=True)
