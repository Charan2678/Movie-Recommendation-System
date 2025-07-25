import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from db_setup import Movie, Base  # Assuming db_setup.py is in the same directory

# Replace with your actual TMDb API key
# For security, consider loading this from an environment variable or config file
TMDB_API_KEY = "cc69edde6ba70167f01f88b06523b94b"  # Placeholder - user needs to replace this

# Setup database connection
engine = create_engine("sqlite:///movie_recommendation.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def fetch_popular_movies(api_key, page=1):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def fetch_movie_details(api_key, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=credits,videos"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def import_movies_to_db(api_key, num_pages=1):
    print(f"Starting movie data import for {num_pages} pages...")
    for page in range(1, num_pages + 1):
        print(f"Fetching page {page} of popular movies...")
        popular_movies_data = fetch_popular_movies(api_key, page)
        for movie_summary in popular_movies_data["results"]:
            movie_id = movie_summary["id"]
            existing_movie = session.query(Movie).filter_by(id=movie_id).first()
            if existing_movie:
                print(f"Movie {movie_summary['title']} (ID: {movie_id}) already exists. Skipping.")
                continue

            print(f"Fetching details for {movie_summary['title']} (ID: {movie_id})...")
            movie_details = fetch_movie_details(api_key, movie_id)

            genres = [genre["name"] for genre in movie_details.get("genres", [])]
            director = next((crew["name"] for crew in movie_details.get("credits", {}).get("crew", []) if crew["job"] == "Director"), None)
            cast = [cast_member["name"] for cast_member in movie_details.get("credits", {}).get("cast", [])[:5]] # Top 5 cast members
            trailer_url = None
            for video in movie_details.get("videos", {}).get("results", []):
                if video["type"] == "Trailer" and video["site"] == "YouTube":
                    trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                    break

            release_date_str = movie_details.get("release_date")
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date() if release_date_str else None

            poster_path = movie_details.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            new_movie = Movie(
                id=movie_details["id"],
                title=movie_details["title"],
                release_date=release_date,
                genres=genres,
                director=director,
                cast=cast,
                plot_summary=movie_details.get("overview"),
                average_rating=movie_details.get("vote_average"),
                poster_url=poster_url,
                trailer_url=trailer_url
            )
            session.add(new_movie)
            session.commit()
            print(f"Successfully imported {movie_details['title']}")
    print("Movie data import complete!")

if __name__ == "__main__":
    if TMDB_API_KEY == "YOUR_TMDB_API_KEY":
        print("ERROR: Please replace 'YOUR_TMDB_API_KEY' in tmdb_data_importer.py with your actual TMDb API key.")
        print("You can get one from https://developer.themoviedb.org/docs/getting-started")
    else:
        # Import the first 5 pages of popular movies as an example
        import_movies_to_db(TMDB_API_KEY, num_pages=5)
    session.close()

