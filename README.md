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

## Add This Project to GitHub

### 1. Create the GitHub repository

Go to [https://github.com/new](https://github.com/new), create a repository named `movie-recommendation-mlops`, and leave **Add a README file** unchecked because this project already has one.

### 2. Configure Git in PowerShell

Run these commands from the project directory:

```powershell
cd C:\Users\DELL\movie-recommendation-mlops
git init
git branch -M main
git add .
git status
```

Before committing, confirm that `Project.pem`, `venv/`, and `65.0.178.96` are not listed. `Project.pem` is a private key and must never be uploaded.

### 3. Commit and connect the repository

```powershell
git commit -m "Add CineMatch movie recommendation system"
git remote add origin https://github.com/YOUR_USERNAME/movie-recommendation-mlops.git
```

Replace `YOUR_USERNAME` with your actual GitHub username. For example:

```powershell
git remote set-url origin https://github.com/Divyapatel19/movie-recommendation-mlops.git
```

Use `git remote set-url` instead of `git remote add` if an `origin` remote already exists.

### 4. Push to GitHub

```powershell
git push -u origin main
```

Complete GitHub authentication in the browser if prompted.

## Security

- Never commit `Project.pem`, API keys, passwords, or `.env` files.
- The project `.gitignore` excludes private keys, virtual environments, cache files, and local deployment metadata.
- If a private key has already been pushed to GitHub, revoke or replace it immediately.

## License

Add a license before distributing this project publicly. The TMDB dataset may have its own usage and attribution requirements; review the dataset's terms before redistribution.
