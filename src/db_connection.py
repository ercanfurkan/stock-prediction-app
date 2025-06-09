import psycopg2
from psycopg2.extras import execute_values
import config
import pandas as pd 

DB_PARAMS = {
    "host" : config.HOST,
    "dbname" :config.DATABASE,
    "user" :config.USER,
    "password" :config.PASSWORD,
    "port":5432,
    "sslmode" :"require"
}

# Clean column names to match SQL schema
def standardize_columns(df):
    return df.rename(columns={col: col.replace("-", "_") for col in df.columns})


def get_data_from_db(ticker: str, start_date: str, end_date: str):
    conn = psycopg2.connect(**DB_PARAMS)
    query = """
        SELECT * FROM stock_prices
        WHERE ticker = %s AND date BETWEEN %s AND %s
        ORDER BY date ASC
    """
    df = pd.read_sql(query, conn, params=(ticker, start_date, end_date), parse_dates=["date"])
    conn.close()
    return df.set_index("date")


def insert_stock_data(df: pd.DataFrame,ticker:str):
    conn =  psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    df = df.copy()
    df["ticker"] = ticker
    #Change names so that they are sql compatible - to _
    df = standardize_columns(df)




    # List of tuples (rows)
    records = [
        (
            row["ticker"], row["date"],
            row.get("open"), row.get("high"), row.get("low"), row.get("close"), row.get("volume"),
            row.get("adjClose"), row.get("adjHigh"), row.get("adjLow"), row.get("adjOpen"), row.get("adjVolume"),
            row.get("divCash"), row.get("splitFactor"),
            row.get("MA_5"), row.get("MA_15"), row.get("MA_30"), row.get("MA_60"), row.get("MA_90"),
            row.get("MA_120"), row.get("MA_150"),
            row.get("RSI"), row.get("MACD"), row.get("MACD_signal"),
            row.get("BOLL_UP"), row.get("BOLL_DOWN"), row.get("BOLL_MID")
        )
        for _, row in df.iterrows()
    ]

    insert_sql = """
        INSERT INTO stock_prices (
            ticker, date, open, high, low, close, volume,
            adjClose, adjHigh, adjLow, adjOpen, adjVolume,
            divCash, splitFactor,
            MA_5, MA_15, MA_30, MA_60, MA_90, MA_120, MA_150,
            RSI, MACD, MACD_signal,
            BOLL_UP, BOLL_DOWN, BOLL_MID
        ) VALUES %s
        ON CONFLICT (ticker, date) DO NOTHING
    """

    execute_values(cur, insert_sql, records)
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Bulk inserted {len(records)} rows for {ticker}")

                    



