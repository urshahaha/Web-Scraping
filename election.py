import requests
from bs4 import BeautifulSoup

# Function to scrape election news from a website
def scrape_news(url, paper_name):
    print(f"\nScraping election news from: {paper_name}")

    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Failed to fetch:", url)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []

    # Extract headlines from h2 and h3 tags
    for tag in soup.find_all(["h2", "h3"]):
        text = tag.get_text(strip=True)

        # Filter only election related news
        if "election" in text.lower() or "निर्वाचन" in text:
            headlines.append(text)

    return headlines


# Newspaper Source
sources = [ ("https://www.onlinekhabar.com/?s=निर्वाचन", "OnlineKhabar")
   
]

all_data = []

# Scrape each site
for url, name in sources:
    news = scrape_news(url, name)

    for item in news[:5]:  # Only first 5 headlines
        all_data.append(f"{name}: {item}")


# Save into file
with open("election_news.txt", "w", encoding="utf-8") as file:
    file.write("Election News Data from 3 Newspapers\n")
    file.write("====================================\n\n")

    for line in all_data:
        file.write(line + "\n")

print("\n✅ Data saved successfully into election_news.txt")
