A comprehensive movie recommendation system built with modern web technologies and machine learning algorithms. The system provides personalized movie recommendations using content-based filtering, collaborative filtering, and hybrid approaches.

✨ Features

🎯 Core Functionality

•
Content-Based Filtering: Recommends movies based on genres, cast, director, and plot similarities

•
Collaborative Filtering: Suggests movies based on user behavior patterns and preferences

•
Hybrid Recommendations: Combines multiple approaches for improved accuracy

•
Real-time Search: Search movies by title or genre with instant results

•
Interactive UI: Modern, responsive design with smooth animations and transitions

🎨 User Experience

•
Movie Discovery: Browse popular movies with detailed information

•
Personalized Recommendations: Get tailored suggestions based on selected movies

•
Rich Movie Details: View ratings, cast, director, genres, and plot summaries

•
Mobile-Responsive: Optimized for both desktop and mobile devices

🛠 Tech Stack

Frontend

•
Framework: React 18 with Vite

•
Styling: Tailwind CSS with shadcn/ui components

•
Icons: Lucide React icons

•
Animations: Framer Motion for smooth transitions

Backend & Data

•
Database: SQLite with SQLAlchemy ORM

•
Data Source: The Movie Database (TMDb) API

•
Machine Learning: scikit-learn for recommendation algorithms

•
Language: Python 3.11

Algorithms

1.
Content-Based Filtering

•
TF-IDF vectorization on movie metadata

•
Cosine similarity between movies

•
Considers genres, cast, director, and plot summaries



2.
Collaborative Filtering

•
User-item matrix for rating patterns

•
Cosine similarity between users

•
Recommends based on similar users' preferences



3.
Hybrid Approach

•
Combines content-based and collaborative filtering

•
Weighted scoring system for improved recommendations



📁 Project Structure

Plain Text


movie-recommendation-system/
├── movie-recommendation-app/          # React frontend application
│   ├── src/
│   │   ├── components/ui/            # shadcn/ui components
│   │   ├── App.jsx                   # Main application component
│   │   ├── App.css                   # Styling and theme
│   │   └── main.jsx                  # Application entry point
│   ├── dist/                         # Production build
│   └── package.json                  # Dependencies and scripts
├── db_setup.py                       # Database schema and setup
├── tmdb_data_importer.py             # Movie data import from TMDb API
├── recommendation_engine.py          # ML algorithms implementation
├── movie_recommendation.db           # SQLite database
├── movie_list.html                   # Static HTML movie list
├── improved_movie_recommendation.html # Enhanced HTML interface
└── README.md                         # Project documentation


🚀 Quick Start

Prerequisites

•
Python 3.11+

•
Node.js 20+

•
TMDb API key (Get one here)

Installation

1.
Clone the repository

2.
Backend Setup

3.
Frontend Setup

4.
Access the application




📖 Usage

For Users

1.
Browse Movies: View the collection of popular movies with ratings and details

2.
Search: Use the search bar to find movies by title or genre

3.
Get Recommendations: Click "Get Recommendations" on any movie to discover similar films

4.
Explore: Navigate through recommendations to find your next favorite movie

