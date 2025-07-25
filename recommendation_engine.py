from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from db_setup import Movie, User, Rating, Base
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Setup database connection
engine = create_engine("sqlite:///movie_recommendation.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class RecommendationEngine:
    def __init__(self):
        self.movies = self._load_movies()
        self.users = self._load_users()
        self.ratings = self._load_ratings()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self._create_tfidf_matrix()
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.user_movie_matrix = self._create_user_movie_matrix()

    def _load_movies(self):
        return session.query(Movie).all()

    def _load_users(self):
        return session.query(User).all()

    def _load_ratings(self):
        return session.query(Rating).all()

    def _create_tfidf_matrix(self):
        movie_descriptions = []
        for movie in self.movies:
            genres_str = " ".join(movie.genres) if movie.genres else ""
            cast_str = " ".join(movie.cast) if movie.cast else ""
            director_str = movie.director if movie.director else ""
            plot_summary_str = movie.plot_summary if movie.plot_summary else ""
            movie_descriptions.append(f"{genres_str} {cast_str} {director_str} {plot_summary_str}")
        
        if not movie_descriptions:
            return np.array([])

        return self.tfidf_vectorizer.fit_transform(movie_descriptions)

    def _create_user_movie_matrix(self):
        # Create a user-movie matrix from ratings for collaborative filtering
        # This is a simplified approach; in a real system, this would be more robust
        if not self.ratings or not self.users or not self.movies:
            return pd.DataFrame()

        user_ids = [user.id for user in self.users]
        movie_ids = [movie.id for movie in self.movies]
        
        # Create a dictionary for quick lookup of movie index
        movie_id_to_idx = {movie.id: i for i, movie in enumerate(self.movies)}

        # Initialize matrix with NaNs
        matrix = np.full((len(user_ids), len(movie_ids)), np.nan)

        for rating in self.ratings:
            try:
                user_idx = user_ids.index(rating.user_id)
                movie_idx = movie_id_to_idx[rating.movie_id]
                matrix[user_idx, movie_idx] = rating.rating
            except ValueError: # Handle cases where user or movie might not be in current loaded lists
                continue

        return pd.DataFrame(matrix, index=user_ids, columns=movie_ids)

    def get_content_based_recommendations(self, movie_id, num_recommendations=10):
        try:
            idx = next(i for i, movie in enumerate(self.movies) if movie.id == movie_id)
        except StopIteration:
            return [] # Movie not found

        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations+1] # Exclude the movie itself

        movie_indices = [i[0] for i in sim_scores]
        return [self.movies[i] for i in movie_indices]

    def get_collaborative_filtering_recommendations(self, user_id, num_recommendations=10):
        if self.user_movie_matrix.empty or user_id not in self.user_movie_matrix.index:
            return []

        user_ratings = self.user_movie_matrix.loc[user_id].dropna()
        if user_ratings.empty:
            return []

        # Calculate similarity between users (simplified: using all users)
        user_similarity = cosine_similarity(self.user_movie_matrix.fillna(0))
        user_similarity_df = pd.DataFrame(user_similarity, index=self.user_movie_matrix.index, columns=self.user_movie_matrix.index)

        # Get similar users
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)
        similar_users = similar_users.drop(user_id) # Exclude self

        recommendations = {}
        for sim_user_id, sim_score in similar_users.items():
            if sim_score <= 0: # Only consider positively correlated users
                continue
            
            other_user_ratings = self.user_movie_matrix.loc[sim_user_id].dropna()
            unrated_movies = other_user_ratings[~other_user_ratings.index.isin(user_ratings.index)]

            for movie_id, rating in unrated_movies.items():
                if movie_id not in recommendations:
                    recommendations[movie_id] = 0
                recommendations[movie_id] += rating * sim_score

        # Sort recommendations by score
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        # Convert movie IDs back to Movie objects
        recommended_movies = []
        for movie_id, _ in sorted_recommendations:
            movie = next((m for m in self.movies if m.id == movie_id), None)
            if movie:
                recommended_movies.append(movie)
            if len(recommended_movies) >= num_recommendations:
                break
        return recommended_movies

    def get_hybrid_recommendations(self, user_id, movie_id=None, num_recommendations=10):
        # Combine content-based and collaborative filtering recommendations
        # This is a basic combination; more sophisticated methods exist
        content_recs = []
        if movie_id:
            content_recs = self.get_content_based_recommendations(movie_id, num_recommendations)
        
        collab_recs = self.get_collaborative_filtering_recommendations(user_id, num_recommendations)

        # Simple merging: prioritize collaborative, then content-based for diversity
        hybrid_recs = []
        collab_ids = set()
        for movie in collab_recs:
            hybrid_recs.append(movie)
            collab_ids.add(movie.id)
        
        for movie in content_recs:
            if movie.id not in collab_ids:
                hybrid_recs.append(movie)
            if len(hybrid_recs) >= num_recommendations:
                break
        
        return hybrid_recs[:num_recommendations]

if __name__ == "__main__":
    # Example: Add a dummy user and some ratings for testing collaborative filtering
    # In a real application, users would register and add ratings via the UI
    from db_setup import User, Rating
    
    # Add a dummy user if not exists
    dummy_user = session.query(User).filter_by(username="test_user").first()
    if not dummy_user:
        dummy_user = User(username="test_user", password_hash="hashed_password", email="test@example.com", registration_date=datetime.now())
        session.add(dummy_user)
        session.commit()
        print(f"Added dummy user: {dummy_user.username} (ID: {dummy_user.id})")
    
    # Add some dummy ratings for the test user if not exists
    # Ensure these movie IDs exist in your database
    movies_in_db = session.query(Movie).limit(5).all() # Get first 5 movies for dummy ratings
    if dummy_user and movies_in_db:
        for i, movie in enumerate(movies_in_db):
            existing_rating = session.query(Rating).filter_by(user_id=dummy_user.id, movie_id=movie.id).first()
            if not existing_rating:
                rating_value = (i % 5) + 1 # Assign ratings 1-5
                new_rating = Rating(user_id=dummy_user.id, movie_id=movie.id, rating=rating_value, timestamp=datetime.now())
                session.add(new_rating)
                session.commit()
                print(f"Added dummy rating for movie {movie.title} by {dummy_user.username}: {rating_value}")

    engine = RecommendationEngine()
    
    # Test content-based recommendations
    if engine.movies:
        sample_movie_id = engine.movies[0].id
        print(f"\nGetting content-based recommendations for movie ID: {sample_movie_id} ({engine.movies[0].title})")
        content_recommendations = engine.get_content_based_recommendations(sample_movie_id)
        for movie in content_recommendations:
            print(f"- {movie.title} (ID: {movie.id})")
    else:
        print("\nNo movies found in the database to generate content-based recommendations.")

    # Test collaborative filtering recommendations
    if dummy_user:
        print(f"\nGetting collaborative filtering recommendations for user: {dummy_user.username} (ID: {dummy_user.id})")
        collab_recommendations = engine.get_collaborative_filtering_recommendations(dummy_user.id)
        if collab_recommendations:
            for movie in collab_recommendations:
                print(f"- {movie.title} (ID: {movie.id})")
        else:
            print("No collaborative filtering recommendations found (might need more users/ratings).")

    # Test hybrid recommendations
    if dummy_user and engine.movies:
        sample_movie_id_for_hybrid = engine.movies[1].id # Use a different movie for hybrid test
        print(f"\nGetting hybrid recommendations for user: {dummy_user.username} (ID: {dummy_user.id}) and movie ID: {sample_movie_id_for_hybrid} ({engine.movies[1].title})")
        hybrid_recommendations = engine.get_hybrid_recommendations(dummy_user.id, sample_movie_id_for_hybrid)
        if hybrid_recommendations:
            for movie in hybrid_recommendations:
                print(f"- {movie.title} (ID: {movie.id})")
        else:
            print("No hybrid recommendations found.")

session.close()

