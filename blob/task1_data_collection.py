import requests
import json
import os
import time
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Keywords used to classify stories
CATEGORIES = {
    "technology": [
        "ai", "software", "tech", "code", "computer",
        "data", "cloud", "api", "gpu", "llm"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "nfl", "nba", "fifa", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "nasa", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "netflix",
        "game", "book", "show", "award", "streaming"
    ],
}

MAX_PER_CATEGORY = 25
MAX_TOP_STORIES = 500


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def fetch_top_story_ids():
    """
    Fetch list of top story IDs from HackerNews.
    """
    url = f"{BASE_URL}/topstories.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()[:MAX_TOP_STORIES]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return []


def fetch_story(story_id):
    """
    Fetch individual story details using story ID.
    If request fails, return None instead of crashing.
    """
    url = f"{BASE_URL}/item/{story_id}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def categorize_title(title):
    """
    Assign category based on keyword matching.
    Matching is case-insensitive.
    """
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None  # ignore stories without category


def ensure_data_folder():
    """
    Create data folder if it doesn't exist.
    """
    if not os.path.exists("data"):
        os.makedirs("data")


# ---------------------------------------------------
# Main Logic
# ---------------------------------------------------

def main():

    print("Fetching top stories...")

    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No stories found. Exiting.")
        return

    collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}

    collected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Loop category by category (required for sleep rule)
    for category in CATEGORIES.keys():

        print(f"\nCollecting category: {category}")

        for story_id in story_ids:

            # Stop if category limit reached
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = fetch_story(story_id)

            # Skip failed or invalid responses
            if not story or "title" not in story:
                continue

            assigned_category = categorize_title(story["title"])

            # Only keep stories matching current category
            if assigned_category != category:
                continue

            # Extract required fields safely
            record = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": collected_time
            }

            collected_stories.append(record)
            category_counts[category] += 1

        # Required delay: ONE sleep per category loop
        time.sleep(2)

    # ---------------------------------------------------
    # Save JSON Output
    # ---------------------------------------------------

    ensure_data_folder()

    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4, ensure_ascii=False)

    print(
        f"\nCollected {len(collected_stories)} stories. "
        f"Saved to {filename}"
    )


# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------

if __name__ == "__main__":
    main()