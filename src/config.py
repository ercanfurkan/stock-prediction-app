from datetime import datetime

#API connection to take stock data
API_KEY = "d4f97a94b2b3d47ecca77ecf4fba8202840835d7"
BASE_URL = "https://api.tiingo.com/tiingo/daily/"
START_DATE = "2000-01-01"
END_DATE = str(datetime.now().date())
#Connection to Database
HOST = "ep-flat-glade-a9m4pyfx-pooler.gwc.azure.neon.tech"
PORT = 5432
DATABASE = "neondb"
USER = "neondb_owner"
PASSWORD = "npg_7d4IcHCykbqS"


