import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import warnings

warnings.filterwarnings('ignore') # Keeps the terminal output clean

# --- Configuration ---
TRAINING_DATA_FILE = "real_historical_sentiment.csv"

def get_prediction(ticker_name, ticker_symbol, todays_sentiment_score):
    """Trains on history and predicts tomorrow based on today's live sentiment."""
    
    # 1. Load the historical textbook (The CSV)
    try:
        sentiment_df = pd.read_csv(TRAINING_DATA_FILE)
        ticker_sentiment = sentiment_df[sentiment_df['Ticker'] == ticker_name]
    except FileNotFoundError:
        print(f"[-] CRITICAL ERROR: {TRAINING_DATA_FILE} not found. Train the model first!")
        return None

    # 2. Download matching historical stock prices
    ticker = yf.Ticker(ticker_symbol)
    price_df = ticker.history(period="1y").reset_index()
    price_df['Date'] = price_df['Date'].dt.strftime('%Y-%m-%d')
    
    # 3. Create the Mathematical Features
    price_df['SMA_5'] = price_df['Close'].rolling(window=5).mean()
    price_df['Daily_Return'] = price_df['Close'].pct_change()
    
    # The Target: Did it go UP (1) or DOWN (0) the next day?
    price_df['Target'] = (price_df['Close'].shift(-1) > price_df['Close']).astype(int)
    
    # 4. Merge Math and Sentiment, then Train the Brain
    merged_df = pd.merge(price_df, ticker_sentiment, on='Date', how='inner').dropna()
    
    if merged_df.empty:
        print(f"[-] Not enough data to train {ticker_name}.")
        return None

    features = ['Close', 'SMA_5', 'Daily_Return', 'Sentiment_Score']
    X_train = merged_df[features]
    y_train = merged_df['Target']
    
    # The Algorithm: Random Forest
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Make Tomorrow's Prediction using TODAY'S data
    todays_data = price_df.iloc[-1:].copy()
    todays_data['Sentiment_Score'] = todays_sentiment_score # Inject today's news score
    
    X_today = todays_data[features]
    
    # Predict and calculate confidence
    prediction_val = model.predict(X_today)[0]
    probability = model.predict_proba(X_today)[0]
    
    prediction_text = "UP 🟢" if prediction_val == 1 else "DOWN 🔴"
    confidence = max(probability) * 100
    
    return {
        "close": todays_data['Close'].values[0],
        "prediction": prediction_text,
        "confidence": confidence
    }
    
# --- Add this to the VERY BOTTOM of predictive_agent.py ---

if __name__ == "__main__":
    print("Testing Agent 4 Standalone...\n")
    
    # We use these placeholder stocks and scores just to test the math
    TEST_TICKERS = {"IRFC": "IRFC.NS", "RVNL": "RVNL.NS", "IRCTC": "IRCTC.NS"}
    simulated_live_scores = {"IRFC": 2, "RVNL": -4, "IRCTC": 1}
    
    for name, symbol in TEST_TICKERS.items():
        score = simulated_live_scores[name]
        print(f"[*] Analyzing {name}...")
        
        result = get_prediction(name, symbol, score)
        
        if result:
            print(f"  -> Today's Close:     ₹{result['close']:.2f}")
            print(f"  -> Today's News:      {score} / 5")
            print(f"  -> FINAL PREDICTION:  {result['prediction']} (Confidence: {result['confidence']:.1f}%)\n")