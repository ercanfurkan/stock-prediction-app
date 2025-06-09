import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from data_fetcher import fetch_stock_data,filter_date_data
import plotly.graph_objects as go
from dash.dependencies import Input,Output,State
import time


# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Viewer"

# Layout
# id = item's name
app.layout = dbc.Container([
    html.H1("📈 Stock Price Viewer", className="text-center mt-4"),
    #Row for controls and buttons
    dbc.Row([
        dbc.Col(
            [
                dcc.Dropdown(options = [
                    {"label":"Apple","value":"appl"},
                    {"label":"Tesla","value":"tsla"},
                    {"label":"Nvidia","value":"nvda"},
                    {"label":"Microsoft","value":"msft"},
                    {"label":"Google","value":"googl"},
                    {"label":"S&P 500","value":"spy"},
                    {"label":"QQQ","value":"qqq"}
                                        
                                        
                                        ],
                    value="spy", #default value
                    id="ticker-input",
                    className ="form-select"

                )
            ], width=12
                ),

        dbc.Col([
              dcc.Dropdown(
                  id="date-range-input",
                  options = [
                  #label--> what user sees
                  #value --> what functions passes to callback as 
                  #add a dictionary for each option in a list
                  {"label":"1 Week","value":"1w"},
                  {"label":"1 Month","value":"1m"},
                  {"label":"3 Months","value":"3m"},
                  {"label":"6 Months","value":"6m"},
                  {"label":"1 Year","value":"1y"},
                  {"label":"All","value":"max"}

              ],

              value = "1m", #default,
              className = "form-select"
              )],width = 6 ),  

        dbc.Col(
            [
                dbc.Button("Load",
                           id="load-button",
                           color="primary",
                           class_name="mb-4"
                           
                           )
            ],width=4,align="center"
        )
        
        ]),

        
    #Graphs wrapped in rows and columns inside those rows
    #All those taken into dcc.Loading so that it gives a loading spinner
    #kind of a loading screen
    dcc.Loading(id="loading-spinner",
                type="circle",
                children = [

                
    #Analysis graphs, price and Mas and volumes
    
    dbc.Row([
    dbc.Col([dcc.Graph(id="stock-graph-1")],width = 12
            ),

    #This is for volume graph
    dbc.Col([dcc.Graph(id="stock-graph-2")],width = 12
            )
    ]
    ),

    #Prediction Graphs
    #Technical indicators and finally predictions
    dbc.Row([
    dbc.Col([dcc.Graph(id="stock-graph-3")],width = 12
            ),

    #This is for volume graph
    dbc.Col([dcc.Graph(id="stock-graph-4")],width = 12
            )
    ]
    )
    

])
],fluid=True)



#Add the app a callback
#When Input X changes update output Y
#Input is whether we click the load button
#Output is the updated graph

#Calback for first graph
@app.callback(
    #output will be id = stock-graph- the property of item with
    #given id
    #2 Outputs, first is price graph second is volume graph
    [Output("stock-graph-1","figure"),Output("stock-graph-2","figure"),
     Output("stock-graph-3","figure"),Output("stock-graph-4","figure")],
    #Take input from item load-button, and use the property of
    # n_clicks
    Input("load-button", "n_clicks"),
    #Take the input (ticker name)
    State("ticker-input", "value"),
    #Take the input daterange
    State("date-range-input","value"),
    #Do not work at the start
    prevent_initial_call=True
)
def update_graphs(n_clicks, ticker,date_range):
    #To simulate a loading effect!!
    #It can be removed
    time.sleep(2)
    if not ticker:
        return go.Figure()  # return empty figure if input is empty
    
    # Fetch stock data
    #The method below was to decrease api calls but every time
    #function is called df gets resetted so it didnot work yet
    #I will work on this
    """
    if n_clicks == 1:
        df = fetch_stock_data(ticker)
        print("YASY")
        df = filter_date_data(df,date_range)
    else:
        df = filter_date_data(df,date_range)
    """
    df = filter_date_data(fetch_stock_data(ticker),date_range)

    #If wrong ticker name or df is empty for some reason
    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data found", xaxis_title="", yaxis_title="")
        #Return empty figures for all graphs
        return fig,fig,fig,fig

    # Create line chart
    price_fig = go.Figure()
    #Add Prices
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["adjClose"], mode='lines', name=ticker.upper()+" Adj Close" ))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["adjHigh"], mode='lines', name=ticker.upper() +" Adj High"))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["adjLow"], mode='lines', name=ticker.upper() +" Adj Low"))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["MA-5"], mode='lines', name=ticker.upper() +" MA-5"))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["MA-15"], mode='lines', name=ticker.upper() +" MA-15"))
    price_fig.add_trace(go.Scatter(x=df["date"], y=df["MA-30"], mode='lines', name=ticker.upper() +" MA-30"))
    price_fig.update_layout(title=f"{ticker.upper()} Stock Prices", xaxis_title="Date", yaxis_title="Price (USD)")

    vol_fig = go.Figure()
    #Add Volume
    vol_fig.add_trace(go.Scatter(x=df["date"],y=df["adjVolume"],mode="lines",name=ticker.upper() +" Adj Volume"))
    vol_fig.update_layout(title=f"{ticker.upper()} Stock Volume", xaxis_title="Date", yaxis_title="Price (USD)")

    # Graph 3: Technical Indicators
    tech_fig = go.Figure()
    tech_fig.add_trace(go.Scatter(x=df["date"], y=df["RSI"], name="RSI"))
    tech_fig.add_trace(go.Scatter(x=df["date"], y=df["MACD"], name="MACD"))
    tech_fig.add_trace(go.Scatter(x=df["date"], y=df["MACD_signal"], name="MACD Signal"))
    tech_fig.update_layout(title="Technical Indicators", yaxis_title="Value")

    #Graph 4: Predictions - Place Holder for now!!
    pred_fig = go.Figure()
    pred_fig.add_trace(go.Scatter(x=df["date"], y=df["adjClose"], name="Actual"))
    pred_fig.add_trace(go.Scatter(x=df["date"], y=df["adjClose"].shift(-1), name="Predicted", line=dict(dash='dot')))
    pred_fig.update_layout(title="Placeholder Prediction")


    return price_fig,vol_fig,tech_fig,pred_fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
