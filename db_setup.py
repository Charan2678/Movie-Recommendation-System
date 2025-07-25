from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date)
    genres = Column(JSON)  # Stored as JSON array
    director = Column(String)
    cast = Column(JSON)  # Stored as JSON array
    plot_summary = Column(Text)
    average_rating = Column(Float)
    poster_url = Column(String)
    trailer_url = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True)
    registration_date = Column(Date)
    preferred_genres = Column(JSON)  # Stored as JSON array

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    timestamp = Column(Date)

# Create an SQLite in-memory database for demonstration, or a file-based one
# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///movie_recommendation.db')

Base.metadata.create_all(engine)

print("Database and tables created successfully!")

