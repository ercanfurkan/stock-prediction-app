import requests
import pandas as pd
from config import API_KEY, BASE_URL, START_DATE, END_DATE
from datetime import datetime,timedelta
from data_utils import preprocess_data,add_mov_avgs,add_technical_indicators
from db_connection import insert_stock_data 

def build_tiingo_url(ticker: str, fmt="csv") -> str:
    return f"{BASE_URL}{ticker}/prices?startDate={START_DATE}&endDate={END_DATE}&format={fmt}&token={API_KEY}"






def fetch_stock_data(ticker) -> pd.DataFrame:
    url = build_tiingo_url(ticker)
    print(f"Fetching data from: {url}")
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    fetched_data = preprocess_data(pd.read_csv(url))

    fetched_data = add_mov_avgs(fetched_data)
    fetched_data = add_technical_indicators(fetched_data)

    insert_stock_data(fetched_data,ticker)


    #return fetched_data



def filter_date_data(fetched_data,range_code):

    #I will take the whole data nonetheless then filter out by the date
    #So that I will call the api to get data once but as the filter changes
    #by the user, this function will update with already taken data
    if range_code == "1w":
        filter = datetime.now() - timedelta(days=8)
        fetched_data = fetched_data.loc[fetched_data["date"]>=filter,:]
    elif range_code =="1m":
        filter = str(datetime.now() - timedelta(days=31))
        fetched_data = fetched_data.loc[fetched_data["date"]>=filter,:]
    elif range_code == "3m":
        filter = str(datetime.now().date() - timedelta(days=91))
        fetched_data = fetched_data.loc[fetched_data["date"]>=filter,:]
    elif range_code == "6m":
        filter = str(datetime.now().date() - timedelta(days=181))
        fetched_data = fetched_data.loc[fetched_data["date"]>=filter,:]
    elif range_code == "1y":
        filter = str(datetime.now().date() - timedelta(days=6))
        fetched_data = fetched_data.loc[fetched_data["date"]>=filter,:]
    else :
        #max meaning no filter
        pass

    return fetched_data

    
    
    
