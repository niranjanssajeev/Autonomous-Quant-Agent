import pandas as pd
import plotly.express as px
import os

CSV_FILE = "railway_stocks_daily.csv"
OUTPUT_HTML = "railway_dashboard.html"

def generate_dashboard():
    print("Waking up Agent 2: The Visualizer...")
    
    # 1. Check if data exists
    if not os.path.exists(CSV_FILE):
        print(f"[-] Error: {CSV_FILE} not found. Has Agent 1 run yet?")
        return

    # 2. Load the data
    try:
        df = pd.read_csv(CSV_FILE)
        # Ensure Date is recognized as a datetime object for proper plotting
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception as e:
        print(f"[-] Error reading data: {e}")
        return

    # 3. Create the Interactive Chart
    print("  [+] Generating interactive chart...")
    
    # We plot Date on the X-axis, Close price on the Y-axis, and color code by Ticker
    fig = px.line(df, x='Date', y='Close', color='Ticker', markers=True,
                  title='Indian Railway PSUs: Daily Closing Prices',
                  labels={'Close': 'Closing Price (₹)', 'Date': 'Trading Day'},
                  template='plotly_dark') # Use 'plotly_white' if you prefer a light theme

    # Add a hover template to show Volume and High/Low
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Close: ₹%{y}<br>')

    # 4. Save to an HTML file
    fig.write_html(OUTPUT_HTML)
    print(f"[SUCCESS] Dashboard updated! Open '{OUTPUT_HTML}' in your web browser.")

if __name__ == "__main__":
    generate_dashboard()