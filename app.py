from flask import Flask, render_template, request, jsonify
import joblib
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the trained movie recommendation artifacts
artifacts = joblib.load("recommender_artifacts.joblib")

titles = artifacts["titles"]
tfidf_matrix = artifacts["tfidf_matrix"]

# Build a lookup for movie titles
title_lookup = {}

for index, title in enumerate(titles):
    title_lookup.setdefault(title.strip().lower(), index)


def recommend_movies(movie_name, limit=5):
    movie_name = movie_name.strip().lower()

    if movie_name not in title_lookup:
        return None

    movie_index = title_lookup[movie_name]

    scores = cosine_similarity(
        tfidf_matrix[movie_index],
        tfidf_matrix
    ).flatten()

    ranked_indices = scores.argsort()[::-1]
    recommendations = []

    for index in ranked_indices:
        if index == movie_index:
            continue

        recommendations.append({
            "title": titles[index],
            "similarity": round(float(scores[index]), 4)
        })

        if len(recommendations) >= limit:
            break

    return recommendations


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    movie_name = ""
    error = None

    if request.method == "POST":
        movie_name = request.form.get("movie_name", "").strip()

        if not movie_name:
            error = "Please enter a movie name."
        else:
            result = recommend_movies(movie_name)

            if result is None:
                error = "Movie not found. Enter an exact title from the dataset."
            else:
                recommendations = result

    return render_template(
        "index.html",
        movie_name=movie_name,
        recommendations=recommendations,
        error=error
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/recommend")
def api_recommend():
    movie_name = request.args.get("movie", "").strip()

    if not movie_name:
        return jsonify({"error": "Please provide a movie name."}), 400

    result = recommend_movies(movie_name)

    if result is None:
        return jsonify({"error": "Movie not found."}), 404

    return jsonify({
        "movie": movie_name,
        "recommendations": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)