import plotly.graph_objects as Go
import pandas as pd

def plot_moving_averages(df: pd.DataFrame, window_sizes=[50, 100, 150]) -> Go.Figure:
    fig = Go.Figure()
    fig.add_trace(Go.Scatter(x=df["date"], y=df["adjClose"], name="Adj Close"))

    for window in window_sizes:
        ma = df["adjClose"].rolling(window).mean()
        fig.add_trace(Go.Scatter(x=df["date"], y=ma, name=f"MA {window}"))

    fig.update_layout(title="Moving Averages on Adjusted Close", xaxis_title="Date", yaxis_title="Price")
    return fig
