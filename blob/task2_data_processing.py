import os
import json
import pandas as pd



# Step 1 — Locate JSON file


DATA_FOLDER = "data"

# find the latest trends_YYYYMMDD.json file automatically
json_files = [
    f for f in os.listdir(DATA_FOLDER)
    if f.startswith("trends_") and f.endswith(".json")
]

if not json_files:
    raise FileNotFoundError("No trends JSON file found in data/ folder.")

# choose latest file (sorted by name/date)
json_files.sort()
latest_file = json_files[-1]

json_path = os.path.join(DATA_FOLDER, latest_file)



# Step 2 — Load JSON into DataFrame


with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

print(f"Loaded {len(df)} stories from {json_path}")



# Step 3 — Clean the Data


# 1. Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing critical fields
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Remove extra whitespace from titles
df["title"] = df["title"].str.strip()



# Step 4 — Save Clean CSV


output_path = os.path.join(DATA_FOLDER, "trends_clean.csv")

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")



# Step 5 — Summary Statistics


print("\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")