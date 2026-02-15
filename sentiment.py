import requests
from textblob import TextBlob
import random

def get_news_sentiment():
    """
    Fetches gold-related news and performs sentiment analysis.
    Uses NewsAPI if key is available, else falls back to mock data for demonstration.
    """
    
    # NOTE: You would typically get this from an environment variable
    # For this academic project, we will use a demo key or fallback if it fails.
    # Replace 'YOUR_NEWSAPI_KEY' with a real key to fetch live data.
    API_KEY = "YOUR_NEWSAPI_KEY" 
    
    url = f"https://newsapi.org/v2/everything?q=gold+price+market&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    
    articles = []
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") == "ok":
            for article in data.get("articles", [])[:5]: # Get top 5
                text = article.get("title", "") + " " + (article.get("description") or "")
                
                # Analyze Sentiment
                analysis = TextBlob(text)
                score = analysis.sentiment.polarity
                
                if score > 0.05:
                    label = "Positive"
                elif score < -0.05:
                    label = "Negative"
                else:
                    label = "Neutral"
                    
                articles.append({
                    "title": article.get("title"),
                    "source": article.get("source", {}).get("name"),
                    "url": article.get("url"),
                    "score": round(score, 3),
                    "label": label
                })
        else:
            raise Exception("API Limit or Error")
            
    except Exception as e:
        # Fallback Mock Data for Academic Demonstration if API fails
        # This ensures the project works even without an active internet connection or API key
        mock_news = [
            ("Gold prices surge as inflation fears grow", 0.4, "Positive"),
            ("Market uncertainty keeps gold stable", 0.0, "Neutral"),
            ("Strong dollar puts pressure on gold futures", -0.3, "Negative"),
            ("Investors flock to safe-haven assets amidst global tension", 0.5, "Positive"),
            ("Technical analysis suggests a bearish trend for gold", -0.2, "Negative")
        ]
        
        for title, score, label in mock_news:
             articles.append({
                "title": title,
                "source": "Market News (Simulated)",
                "url": "#",
                "score": score,
                "label": label
            })

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
        "mood": mood
    }

if __name__ == "__main__":
    print(get_news_sentiment())
