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
# id = item's name
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
    #Graph component with name stock-graph-1
    #This is for adjusted close high and low prices
    dcc.Graph(id="stock-graph-1"),

    #This is for volume graph
    dcc.Graph(id="stock-graph-2")



])

#Add the app a callback
#When Input X changes update output Y
#Input is whether we click the load button
#Output is the updated graph

#Calback for first graph
@app.callback(
    #output will be id = stock-graph- the property of item with
    #given id
    #2 Outputs, first is price graph second is volume graph
    [Output("stock-graph-1","figure"),Output("stock-graph-2","figure")],
    #Take input from item load-button, and use the property of
    # n_clicks
    Input("load-button", "n_clicks"),
    #Take the input (ticker name)
    State("ticker-input", "value"),
    #Do not work at the start
    prevent_initial_call=True
)
def update_graphs(n_clicks, ticker):
    if not ticker:
        return go.Figure()  # return empty figure if input is empty
    
    # Fetch stock data
    df = fetch_stock_data(ticker)

    #If wrong ticker name or df is empty for some reason
    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data found", xaxis_title="", yaxis_title="")
        #Return empty figures for both
        return fig,fig

    # Create line chart
    price_fig = go.Figure()
    #Add Prices
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["adjClose"], mode='lines', name=ticker.upper()+" Adj Close" ))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["adjHigh"], mode='lines', name=ticker.upper() +" Adj High"))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["adjLow"], mode='lines', name=ticker.upper() +" Adj Low"))
    price_fig.update_layout(title=f"{ticker.upper()} Stock Prices", xaxis_title="Date", yaxis_title="Price (USD)")

    vol_fig = go.Figure()
    #Add Volume
    vol_fig.add_trace(go.Scatter(x=df["date"],y=df["adjVolume"],mode="lines",name=ticker.upper() +" Adj Volume"))
    vol_fig.update_layout(title=f"{ticker.upper()} Stock Volume", xaxis_title="Date", yaxis_title="Price (USD)")

    return price_fig,vol_fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
