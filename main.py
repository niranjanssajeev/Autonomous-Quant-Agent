import daily_agent
import visualizer_agent
import news_agent
import predictive_agent
from datetime import datetime
import time
import csv
import os

# --- Configuration ---
TICKERS = {"IRFC": "IRFC.NS", "RVNL": "RVNL.NS", "IRCTC": "IRCTC.NS"}

def run_system():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"=== Initiating Autonomous Quant AI System at {current_time} ===\n")

    # ---------------------------------------------------------
    # PHASE 1: Data Harvesting & Memory (Agent 1)
    # ---------------------------------------------------------
    print(">>> PHASE 1: Data Harvesting")
    max_retries = 3
    retry_delay = 300 # 5 minutes
    data_harvested = False

    for attempt in range(1, max_retries + 1):
        try:
            daily_agent.main()
            data_harvested = True
            print("  [+] Phase 1 completed successfully.")
            break 
        except Exception as e:
            print(f"  [-] Agent 1 encountered an error: {e}")
            if attempt < max_retries:
                print(f"  [*] Self-Correcting: Waiting 5 minutes before retry {attempt + 1}/{max_retries}...")
                time.sleep(retry_delay)
            else:
                print("  [!] Critical Failure: Maximum retries reached.")
    print("-" * 40)

    # Circuit Breaker: Halt if we have no new data
    if not data_harvested:
        print(">>> System halted due to Phase 1 failure. Standing by until tomorrow.")
        return

    # ---------------------------------------------------------
    # PHASE 2: Visualizations & Dashboarding (Agent 2)
    # ---------------------------------------------------------
    print(">>> PHASE 2: Dashboard Update")
    try:
        visualizer_agent.generate_dashboard()
    except Exception as e:
        print(f"  [-] Agent 2 encountered an error: {e}")
    print("-" * 40)

    # ---------------------------------------------------------
    # PHASE 3: ML Predictions & Quant Overlay (Agent 3 + Agent 4)
    # ---------------------------------------------------------
    print(">>> PHASE 3: Machine Learning Forecasts & Logging")
    try:
        live_scores = news_agent.get_daily_sentiment_scores()
        print("\n  [+] Agent 4 is processing the quant overlay...")
        
        # Prepare the log file
        log_file = "prediction_history.csv"
        file_exists = os.path.exists(log_file)
        
        with open(log_file, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = ['Date', 'Ticker', 'Close_Price', 'Sentiment_Score', 'Prediction', 'Confidence']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader() # Write column headers if it's a new file
                
            for name, symbol in TICKERS.items():
                todays_score = live_scores.get(name, 0) 
                result = predictive_agent.get_prediction(name, symbol, todays_score)
                
                if result:
                    # 1. Print to the console (just in case you are watching)
                    print(f"\n--- {name} FORECAST ---")
                    print(f"  Today's Close:     ₹{result['close']:.2f}")
                    print(f"  Today's Sentiment: {todays_score} / 5")
                    print(f"  TOMORROW:          {result['prediction']} (Confidence: {result['confidence']:.1f}%)")
                    
                    # 2. Silently save it to the permanent log file
                    writer.writerow({
                        'Date': datetime.now().strftime('%Y-%m-%d'),
                        'Ticker': name,
                        'Close_Price': round(result['close'], 2),
                        'Sentiment_Score': todays_score,
                        'Prediction': result['prediction'],
                        'Confidence': round(result['confidence'], 1)
                    })
        print(f"\n  [SUCCESS] All predictions permanently saved to {log_file}")
                
    except Exception as e:
        print(f"  [-] Phase 3 encountered an error: {e}")
    print("-" * 40)
    # ---------------------------------------------------------
    # PHASE 4: LLM Weekly Catalyst Report (Agent 3)
    # ---------------------------------------------------------
    if datetime.today().weekday() == 4:
        print(">>> PHASE 4: Friday Market Close Detected - Initiating Weekly News Rollup")
        try:
            news_agent.main()
        except Exception as e:
            print(f"  [-] Agent 3 encountered an error: {e}")
    else:
        print(">>> PHASE 4: Skipped. (Weekly catalyst report only runs on Fridays).")
        
    print(f"\n=== All Agent Tasks Completed Successfully ===")

if __name__ == "__main__":
    run_system()