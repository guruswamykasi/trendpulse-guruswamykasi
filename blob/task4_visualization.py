import os
import pandas as pd
import matplotlib.pyplot as plt


# Step 1 — Setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "trends_analysed.csv")
OUTPUT_DIR = "outputs"

# create outputs folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# load dataframe
df = pd.read_csv(DATA_PATH)

print("Data loaded successfully.")



# Helper function: shorten long titles

def shorten_title(title, max_len=50):
    """Shortens titles longer than max_len characters."""
    if len(title) > max_len:
        return title[:max_len] + "..."
    return title



# Chart 1 — Top 10 Stories by Score


top10 = df.sort_values(by="score", ascending=False).head(10)

titles = top10["title"].apply(shorten_title)
scores = top10["score"]

plt.figure(figsize=(10, 6))
plt.barh(titles, scores)
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # highest score on top

chart1_path = os.path.join(OUTPUT_DIR, "chart1_top_stories.png")
plt.savefig(chart1_path, bbox_inches="tight")
plt.close()

print("Chart 1 saved.")



# Chart 2 — Stories per Category


category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

chart2_path = os.path.join(OUTPUT_DIR, "chart2_categories.png")
plt.savefig(chart2_path, bbox_inches="tight")
plt.close()

print("Chart 2 saved.")



# Chart 3 — Score vs Comments Scatter


popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8, 6))

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

chart3_path = os.path.join(OUTPUT_DIR, "chart3_scatter.png")
plt.savefig(chart3_path, bbox_inches="tight")
plt.close()

print("Chart 3 saved.")



# Bonus — Dashboard (All Charts Together)


fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Dashboard Chart 1
axes[0].barh(titles, scores)
axes[0].set_title("Top Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Dashboard Chart 2
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")

# Dashboard Chart 3
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard")

dashboard_path = os.path.join(OUTPUT_DIR, "dashboard.png")
plt.savefig(dashboard_path, bbox_inches="tight")
plt.close()

print("Dashboard saved.")