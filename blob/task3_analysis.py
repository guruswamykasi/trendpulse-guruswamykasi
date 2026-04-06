import os
import pandas as pd
import numpy as np



# Step 1 — Load and Explore Data


DATA_PATH = os.path.join("data", "trends_clean.csv")

# load CSV into dataframe
df = pd.read_csv(DATA_PATH)

print(f"Loaded data: {df.shape}")

# print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# average statistics using pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")



# Step 2 — Analysis using NumPy


print("\n--- NumPy Stats ---")

# convert columns to numpy arrays
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

# numpy calculations
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

max_score = np.max(scores)
min_score = np.min(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_category_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# story with most comments
max_comments_index = np.argmax(comments)
top_story_title = df.iloc[max_comments_index]["title"]
top_story_comments = comments[max_comments_index]

print(
    f'\nMost commented story: "{top_story_title}" — {top_story_comments} comments'
)



# Step 3 — Add New Columns


# engagement = comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score greater than average score
df["is_popular"] = df["score"] > avg_score



# Step 4 — Save Analysed Data


OUTPUT_PATH = os.path.join("data", "trends_analysed.csv")

df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved to {OUTPUT_PATH}")