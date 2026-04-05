import feedparser
from google import genai  # <-- Using the brand new SDK
from datetime import datetime, timedelta

# --- Configuration ---
# Get your free API key from: https://aistudio.google.com/
GEMINI_API_KEY = "AIzaSyDo6TPLOgpEnIl5scVLf4eKU_22f8_Hx6U" 

TICKERS = {"IRFC": "Indian Railway Finance Corporation", 
           "RVNL": "Rail Vikas Nigam Limited", 
           "IRCTC": "Indian Railway Catering and Tourism Corporation"}

def fetch_recent_news(company_name, days_back=5):
    """Fetches news from Google News RSS for the past few days."""
    print(f"  [+] Scraping news for {company_name}...")
    
    # Format the query for Google News
    query = company_name.replace(" ", "%20") + "%20stock%20news"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    feed = feedparser.parse(rss_url)
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    headlines = []
    for entry in feed.entries:
        try:
             published_date = datetime.strptime(entry.published[5:25], "%d %b %Y %H:%M:%S")
             if published_date > cutoff_date:
                 headlines.append(f"- {entry.title} ({published_date.strftime('%Y-%m-%d')})")
        except:
             headlines.append(f"- {entry.title}")
             
        # Limit to top 8 recent headlines per stock
        if len(headlines) >= 8:
            break
            
    return "\n".join(headlines)

def analyze_catalysts(news_text):
    """Sends the compiled news to Gemini to extract the actual catalysts."""
    print("  [+] Sending data to Gemini for analysis...")
    
    # Initialize the new client with your API key
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert financial analyst focusing on Indian Railway infrastructure stocks.
    Review the following news headlines from the past week:
    
    {news_text}
    
    Task: Write a concise, bulleted 'Weekly Catalyst Report'. 
    Ignore generic market noise or opinion pieces. Only highlight concrete events that likely affected the stock prices, such as:
    - New order wins or contracts (specify the monetary value if present).
    - Government budget allocations or Ministry of Railways announcements.
    - Earnings reports or dividend announcements.
    
    Format the output with the stock ticker as a bold header, followed by the bullet points. If there was no significant news for a stock, explicitly state "No major catalysts reported."
    """
    
    # Use the new client.models.generate_content syntax
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Upgraded to the newest flash model as well
        contents=prompt
    )
    
    return response.text
def get_daily_sentiment_scores():
    """Fetches today's news and generates a -5 to +5 score for Agent 4."""
    print("  [+] Agent 3 is fetching live daily sentiment scores...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    scores = {}
    
    for ticker, name in TICKERS.items():
        # Fetch only the last 1 day of news
        news = fetch_recent_news(name, days_back=1) 
        
        if not news.strip():
            scores[ticker] = 0 # Neutral if no news today
            continue
            
        prompt = f"""
        Analyze these headlines for {name} from the past 24 hours:
        {news}
        Score the financial sentiment for the company's stock on a scale of -5 to 5.
        -5 is highly negative, 0 is neutral, 5 is highly positive.
        Respond with ONLY the integer.
        """
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            scores[ticker] = int(response.text.strip())
        except Exception as e:
            print(f"  [-] Failed to score {ticker}: {e}")
            scores[ticker] = 0
            
    return scores
def main():
    print("\nWaking up Agent 3: The News Correlator...")
    
    all_news = ""
    for ticker, name in TICKERS.items():
        news = fetch_recent_news(name)
        if news:
            all_news += f"\nNews for {ticker}:\n{news}\n"
        else:
            all_news += f"\nNews for {ticker}:\n- No recent news found.\n"
            
    if not all_news.strip():
        print("[-] No news found across any tickers.")
        return
        
    # Generate the report
    report = analyze_catalysts(all_news)
    
    # Save the report
    report_filename = f"Weekly_Report_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_filename, "w", encoding='utf-8') as f:
        f.write(report)
        
    print(f"\n[SUCCESS] Weekly Catalyst Report generated: {report_filename}")

if __name__ == "__main__":
    main()