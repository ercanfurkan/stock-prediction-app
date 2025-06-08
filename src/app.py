import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from data_fetcher import fetch_stock_data
import plotly.graph_objects as go
from dash.dependencies import Input,Output,State


# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Viewer"

# Layout
app.layout = dbc.Container([
    html.H1("📈 Stock Price Viewer", className="text-center mt-4"),
    dbc.Row([
        dbc.Col(
            [
                dcc.Input(
                    id="ticker-input",
                    type="text",
                    placeholder= "Enter stock ticker (e.g. AAPL)",
                    debounce=True,
                    className="form-control"

                )
            ], width=12
        ),

        dbc.Col(
            [
                dbc.Button("Load",
                           id="load-button",
                           color="primary",
                           class_name="ms-2"
                           
                           )
            ],width=4,align="center"
        )


    ]),
    dcc.Graph(id="stock-graph")



])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
