import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
TICKERS = {"IRFC": "IRFC.NS", "RVNL": "RVNL.NS", "IRCTC": "IRCTC.NS"}
DATABASE_FILE = "railway_stocks_master.csv"

def main():
    print("Waking up Agent 1: The Data Harvester...")
    
    # Grab today's exact date
    today_date = datetime.now().strftime('%Y-%m-%d')
    new_data = []

    for name, symbol in TICKERS.items():
        print(f"  [+] Fetching today's market data for {name}...")
        ticker = yf.Ticker(symbol)
        
        # Pull the last 1 day of trading data
        df = ticker.history(period="1d")

        if not df.empty:
            # --- FOOLPROOF DATE FIX ---
            # Don't trust the yfinance index. Forcefully create the Date column.
            df['Date'] = today_date
            df['Ticker'] = name

            # Keep only the columns we actually care about
            columns_to_keep = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = df[columns_to_keep]

            # Round the prices for a cleaner database
            df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].round(2)
            
            new_data.append(df)
        else:
            print(f"  [-] Warning: Failed to fetch data for {name}. The market might be closed.")

    if new_data:
        # Combine the 3 stocks into one clean DataFrame
        todays_df = pd.concat(new_data, ignore_index=True)

        # --- The ETL Storage Logic ---
        if os.path.exists(DATABASE_FILE):
            todays_df.to_csv(DATABASE_FILE, mode='a', header=False, index=False)
            print(f"  [SUCCESS] Appended today's data ({today_date}) to {DATABASE_FILE}")
        else:
            todays_df.to_csv(DATABASE_FILE, index=False)
            print(f"  [SUCCESS] Created new master database {DATABASE_FILE} with today's data.")
    else:
        raise Exception("Zero data harvested today. API connection failure or holiday.")

if __name__ == "__main__":
    main()