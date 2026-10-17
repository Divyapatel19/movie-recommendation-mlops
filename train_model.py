import ast
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading movie dataset...")

df = pd.read_csv("tmdb_5000_movies.csv")

print("Dataset loaded:", df.shape)
print("Columns:", df.columns.tolist())

required = ["title", "genres", "keywords", "overview"]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")


def extract_names(value):
    if pd.isna(value):
        return ""

    try:
        items = ast.literal_eval(value)
        if isinstance(items, list):
            return " ".join(
                str(item.get("name", ""))
                for item in items
                if isinstance(item, dict)
            )
    except (ValueError, SyntaxError, TypeError):
        pass

    return str(value)


print("Preparing movie information...")

df["genres_text"] = df["genres"].apply(extract_names)
df["keywords_text"] = df["keywords"].apply(extract_names)
df["overview"] = df["overview"].fillna("").astype(str)

df["combined_features"] = (
    df["genres_text"] + " " +
    df["keywords_text"] + " " +
    df["overview"]
).str.strip()

df = df.dropna(subset=["title"])
df = df[df["title"].astype(str).str.strip() != ""]
df = df[df["combined_features"] != ""]
df = df.reset_index(drop=True)

if df.empty:
    raise ValueError("No usable movie records found.")

print("Preparing TF-IDF model...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=20000
)

tfidf_matrix = vectorizer.fit_transform(
    df["combined_features"]
)

artifacts = {
    "titles": df["title"].astype(str).tolist(),
    "vectorizer": vectorizer,
    "tfidf_matrix": tfidf_matrix
}

joblib.dump(artifacts, "recommender_artifacts.joblib")

print("SUCCESS! Model artifacts saved.")
print("Total movies:", len(df))
print("TF-IDF matrix shape:", tfidf_matrix.shape)