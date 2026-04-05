import schedule
import time
from datetime import datetime
import main # Imports your master orchestrator

def job():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Market Closed. Waking up AI Agents...")
    main.run_system()

# Schedule the system to run Monday through Friday at 16:00 (4:00 PM)
schedule.every().monday.at("16:00").do(job)
schedule.every().tuesday.at("16:00").do(job)
schedule.every().wednesday.at("16:00").do(job)
schedule.every().thursday.at("16:00").do(job)
schedule.every().friday.at("16:00").do(job)

print("=== AUTOPILOT ENGAGED ===")
print("The AI Quant System is now running in the background.")
print("It will automatically wake up and analyze the market at 4:00 PM IST on weekdays.")
print("You can minimize this window. Press Ctrl+C to stop.")

# The infinite loop that keeps the script alive and watching the clock
while True:
    schedule.run_pending()
    time.sleep(60) # Check the clock every 60 seconds