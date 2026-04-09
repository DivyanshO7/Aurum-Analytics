import requests
from textblob import TextBlob
import random
import os

_last_target_score = None
_manual_refresh_count = 0

def get_news_sentiment(force_refresh=False):
    """
    Fetches gold-related news and performs sentiment analysis.
    Uses NewsAPI if key is available, else falls back to mock data for demonstration.
    """
    global _last_target_score, _manual_refresh_count
    
    if force_refresh:
        _manual_refresh_count += 1

    
    # NOTE: You would typically get this from an environment variable
    # For this academic project, we will use a demo key or fallback if it fails.
    # Replace 'YOUR_NEWSAPI_KEY' with a real key to fetch live data.
    API_KEY = os.environ.get("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY") 
    
    url = f"https://newsapi.org/v2/everything?q=gold+price+market&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    
    articles = []
    
    api_status = "Connected"
    api_error = None
    
    news_pool = []
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") == "ok" and len(data.get("articles", [])) > 0:
            for article in data.get("articles", []):
                title = article.get("title", "")
                if not title:
                    continue
                # Analyze Sentiment
                text = title + " " + (article.get("description") or "")
                score = TextBlob(text).sentiment.polarity
                news_pool.append((title, score, "Live Data"))
        else:
            raise Exception(data.get("message", "API Limit or Error"))
            
    except Exception as e:
        api_status = "Failed"
        api_error = str(e)
        
        # Fallback Mock Data for Academic Demonstration if API fails
        news_pool = [
            ("Gold prices surge as inflation fears grow", 0.4, "Positive"),
            ("Market uncertainty keeps gold stable", 0.0, "Neutral"),
            ("Strong dollar puts pressure on gold futures", -0.3, "Negative"),
            ("Investors flock to safe-haven assets amidst global tension", 0.5, "Positive"),
            ("Technical analysis suggests a bearish trend for gold", -0.2, "Negative"),
            ("Central banks increase gold reserves significantly", 0.6, "Positive"),
            ("Unexpected jobs report causes gold selloff", -0.4, "Negative"),
            ("Fed indicates rate cuts, gold responds positively", 0.3, "Positive"),
            ("Profit taking halts gold's five-day rally", -0.1, "Negative"),
            ("Crypto rebound diverts capital away from gold", -0.3, "Negative"),
            ("Gold mining stocks hit new yearly high", 0.4, "Positive"),
            ("Treasury yields rise, dampening gold appeal", -0.2, "Negative"),
            ("Retail demand for physical gold jumps in Asia", 0.6, "Positive"),
            ("Institutional investors trim gold exposure", -0.4, "Negative"),
            ("Geopolitical risks trigger new gold rush", 0.7, "Positive"),
            ("Gold prices consolidate ahead of FOMC meeting", 0.0, "Neutral"),
            ("Speculative short positions on gold increase", -0.3, "Negative"),
            ("Weak manufacturing data boosts gold as a hedge", 0.4, "Positive"),
            ("Stronger than expected GDP hurts safe havens", -0.5, "Negative"),
            ("Gold ETFs see consecutive weeks of inflows", 0.3, "Positive"),
            ("Industrial demand for precious metals dips slightly", -0.1, "Negative"),
            ("Analysts upgrade gold price targets for end of year", 0.5, "Positive"),
            ("Hawkish Fed comments cause gold to tumble", -0.6, "Negative"),
            ("Rising debt levels globally support case for gold", 0.4, "Positive"),
            ("Currency devaluation fears drive local gold premiums", 0.6, "Positive"),
            ("Gold volatility remains at historic lows", 0.0, "Neutral"),
            ("New major gold discovery announced in Nevada", 0.2, "Positive"),
            ("Margin calls force liquidation of gold positions", -0.5, "Negative"),
            ("Sovereign wealth funds diversify into gold", 0.4, "Positive"),
            ("Options market shows neutral bias for gold", 0.0, "Neutral"),
            ("Inflation prints lower than expected, gold slips", -0.3, "Negative"),
            ("Dovish ECB bolsters European demand for gold", 0.3, "Positive"),
            ("Consumer confidence plunge sends gold higher", 0.5, "Positive"),
            ("Tech sector boom overshadows gold gains", -0.2, "Negative"),
            ("Historical seasonality favors gold in current quarter", 0.2, "Positive"),
            ("Algorithmic trading amplifies gold sell-off", -0.4, "Negative"),
            ("Global supply chain issues threaten gold refining", 0.1, "Positive"),
            ("Gold futures hit resistance at key technical level", -0.1, "Negative"),
            ("Central bank digital currencies pose threat to gold", -0.2, "Negative"),
            ("Record breaking auction sales for rare gold coins", 0.3, "Positive"),
            ("Deflationary signals prompt gold market rethink", -0.3, "Negative"),
            ("Retail jewelry sales in India surge on festival demand", 0.6, "Positive"),
            ("Mining strikes in South Africa disrupt supply", 0.4, "Positive"),
            ("Gold struggles to maintain momentum past $2000", -0.2, "Negative"),
            ("Billionaire investor increases gold allocation", 0.5, "Positive"),
            ("Silver outpaces gold in latest precious metal rally", -0.1, "Negative"),
            ("Macro data provides mixed signals for gold", 0.0, "Neutral"),
            ("Recession fears fade, putting pressure on gold", -0.4, "Negative"),
            ("Gold tracks sideways as market awaits CPI data", 0.0, "Neutral"),
            ("Unprecedented fiscal stimulus revives gold debate", 0.3, "Positive"),
            ("Record sovereign debt fuels long-term gold thesis", 0.4, "Positive"),
            ("Gold mining index underperforms physical metal", -0.2, "Negative"),
            ("New environmental regulations impact gold producers", -0.1, "Negative"),
            ("China's central bank skips gold purchases for first time in months", -0.3, "Negative"),
            ("Swiss gold exports hit record levels on strong Asian demand", 0.5, "Positive")
        ]
        
    # Calculate sequential index to guarantee 0 repetition for up to 11 manual refreshes
    start_index = (_manual_refresh_count * 5) % len(news_pool)
    selected_news = []
    for i in range(5):
        selected_news.append(news_pool[(start_index + i) % len(news_pool)])
    
    raw_avg = sum(s for _, s, _ in selected_news) / 5
    target_avg = raw_avg
    
    import time
    block_id = int(time.time() / (12 * 3600)) + _manual_refresh_count
    
    if _last_target_score is not None:
         # Generate a deterministic small step based on the block, max +-0.002
         random.seed(block_id + 999) 
         target_avg = _last_target_score + random.uniform(-0.002, 0.002)
         target_avg = max(-1.0, min(1.0, target_avg))

    # Reset seed so we don't mess up other systemic random operations globally
    random.seed()
    
    difference = target_avg - raw_avg
    
    for title, score, label in selected_news:
         adjusted_score = score + difference
         adjusted_score = max(-1.0, min(1.0, adjusted_score))
         
         if adjusted_score > 0.05:
             adj_label = "Positive"
         elif adjusted_score < -0.05:
             adj_label = "Negative"
         else:
             adj_label = "Neutral"

         source_str = "Market News (Simulated)" if api_status == "Failed" else "Live News"
         
         articles.append({
            "title": title,
            "source": source_str,
            "url": "#",
            "score": round(adjusted_score, 3),
            "label": adj_label
        })
        
    _last_target_score = target_avg

    # Calculate Overall Market Mood
    avg_score = sum(a['score'] for a in articles) / len(articles) if articles else 0
    
    if avg_score > 0.05:
        mood = "Bullish"
    elif avg_score < -0.05:
        mood = "Bearish"
    else:
        mood = "Neutral"
        
    return {
        "articles": articles,
        "average_score": round(avg_score, 3),
        "mood": mood,
        "api_status": api_status,
        "api_error": api_error
    }

if __name__ == "__main__":
    print(get_news_sentiment())
