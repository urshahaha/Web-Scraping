import requests
import json
from bs4 import BeautifulSoup
from newspaper import Article
import time

# --- Updated News Sources ---
NEWS_SOURCES = [
    {
        "newspaper": "MyRepublica",
        "base_url": "https://myrepublica.nagariknetwork.com"
    },
    {
        "newspaper": "The Rising Nepal",
        "base_url": "https://risingnepaldaily.com"
    }
]

POLITICAL_KEYWORDS = [
    "election", "vote", "voting", "parliament", "government",
    "prime minister", "minister", "party", "candidate",
    "assembly", "congress", "uml", "maoist", "coalition",
    "ballot", "commission", "poll", "constitutional"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_political(title):
    title = title.lower()
    return any(word in title for word in POLITICAL_KEYWORDS)

def extract_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return ""

def summarize_text(text, max_sentences=3):
    sentences = text.split(". ")
    summary = ". ".join(sentences[:max_sentences])
    return summary.strip() + "."

def scrape_homepage(source):
    articles = []
    try:
        response = requests.get(source["base_url"], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            title = link.get_text(strip=True)
            url = link["href"]

            if not title or len(title) < 25:
                continue

            if not url.startswith("http"):
                url = source["base_url"] + url

            if is_political(title):
                articles.append({
                    "title": title,
                    "url": url,
                    "source": source["newspaper"]
                })
        return articles[:6]  
    except:
        return []

results = []

for source in NEWS_SOURCES:
    print(f"Scraping {source['newspaper']}...")
    article_links = scrape_homepage(source)

    for article in article_links:
        text = extract_article_text(article["url"])
        if text.strip():
            summary = summarize_text(text)
            results.append({
                "source": article["source"],
                "title": article["title"],
                "url": article["url"],
                "summary": summary
            })
        time.sleep(2)  

with open("nepal_election_summaries.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print("\nElection summaries saved in nepal_election_summaries.json")
