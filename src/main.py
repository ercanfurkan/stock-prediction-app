from data_fetcher import fetch_stock_data
from data_utils import preprocess_data
from visualization import plot_moving_averages

def main():
    
    ticker = "aapl"
    df = fetch_stock_data(ticker)
    df = preprocess_data(df)
    fig = plot_moving_averages(df)
    fig.show()

if __name__ == "__main__":
    main()
