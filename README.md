# CineMatch: Movie Recommendation System

CineMatch is a Flask-based movie recommendation application. Enter a movie title and the app returns five movies with similar content using a TF-IDF model and cosine similarity.

## Features

- Clean web interface for movie discovery.
- Content-based recommendations using movie genres, keywords, and overview text.
- Five recommendations with similarity scores.
- JSON API for programmatic access.
- Health-check endpoint for deployment monitoring.
- Docker support.

## How It Works

1. `train_model.py` loads the TMDB movie dataset.
2. Genres and keywords are converted from JSON-like values into text.
3. Genres, keywords, and movie overviews are combined into one feature string.
4. `TfidfVectorizer` converts the feature text into numerical vectors.
5. The trained vectorizer, movie titles, and TF-IDF matrix are saved in `recommender_artifacts.joblib`.
6. `app.py` compares the selected movie with all other movies using cosine similarity.

## Project Structure

```text
movie-recommendation-mlops/
├── app.py                        # Flask web app and API
├── train_model.py                # Training and artifact-generation script
├── recommender_artifacts.joblib  # Saved recommendation model artifacts
├── tmdb_5000_movies.csv          # Movie dataset
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container configuration
├── templates/
│   └── index.html                 # Web page template
├── static/
│   └── style.css                  # Application styling
└── .gitignore                     # Files excluded from Git
```

## Requirements

- Python 3.11 or later
- pip
- Docker (optional)

## Run Locally on Windows

Open PowerShell in the project directory:

```powershell
cd C:\Users\DELL\movie-recommendation-mlops
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python app.py
```

Open the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

> Search using an exact movie title from the dataset, such as `Titanic`.

## Retrain the Model

The repository includes a generated artifact, so retraining is not required for normal use. To generate a new artifact after changing the dataset or training logic, run:

```powershell
python train_model.py
```

The script reads `tmdb_5000_movies.csv` and updates `recommender_artifacts.joblib`.

## API Endpoints

### Health check

```text
GET /health
```

Example:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
```

Response:

```json
{
  "status": "healthy"
}
```

### Get recommendations

```text
GET /api/recommend?movie=Titanic
```

PowerShell example:

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/api/recommend?movie=Titanic"
```

The response contains the requested movie and five recommended movies with their similarity scores.

## Run with Docker

Build the image:

```powershell
docker build -t movie-recommendation-mlops .
```

Run the container:

```powershell
docker run --name movie-recommendation -p 5000:5000 movie-recommendation-mlops
```

Open [http://localhost:5000](http://localhost:5000).

To stop and remove the container:

```powershell
docker stop movie-recommendation
docker rm movie-recommendation
```
## License

Add a license before distributing this project publicly. The TMDB dataset may have its own usage and attribution requirements; review the dataset's terms before redistribution.
