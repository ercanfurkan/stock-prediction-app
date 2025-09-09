import os
from datetime import date
from dotenv import load_dotenv, find_dotenv

# Find .env no matter where you run the script from (root, src/, etc.)
dotenv_path = find_dotenv(filename=".env", usecwd=True)

# load_dotenv returns True/False; useful for debugging
loaded = load_dotenv(dotenv_path=dotenv_path, override=False)


#Function to get env vars and if not exist throw error
def _require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing environment variable: {name}. See .env.example")
    return val

TIINGO_API_KEY = _require("TIINGO_API_KEY")
TIINGO_BASE_URL = os.getenv("TIINGO_BASE_URL", "https://api.tiingo.com/tiingo/daily/")

# Dates (overridable via env)
START_DATE = os.getenv("START_DATE", "2000-01-01")
END_DATE = os.getenv("END_DATE", str(date.today()))

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_HOST = _require("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = _require("DB_NAME")
    DB_USER = _require("DB_USER")
    DB_PASSWORD = _require("DB_PASSWORD")
    DB_SSLMODE = os.getenv("DB_SSLMODE", "require")
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?sslmode={DB_SSLMODE}"
    )