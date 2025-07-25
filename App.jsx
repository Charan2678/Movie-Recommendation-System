import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Star, Search, Film, Users, Sparkles } from 'lucide-react'
import './App.css'

function App() {
  const [movies, setMovies] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedMovie, setSelectedMovie] = useState(null)
  const [loading, setLoading] = useState(false)

  // Mock data for demonstration - in a real app, this would come from your backend API
  const mockMovies = [
    {
      id: 1,
      title: "The Shawshank Redemption",
      genres: ["Drama", "Crime"],
      director: "Frank Darabont",
      cast: ["Tim Robbins", "Morgan Freeman"],
      plot_summary: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
      average_rating: 9.3,
      poster_url: "https://via.placeholder.com/300x450/1e40af/ffffff?text=Shawshank"
    },
    {
      id: 2,
      title: "The Godfather",
      genres: ["Crime", "Drama"],
      director: "Francis Ford Coppola",
      cast: ["Marlon Brando", "Al Pacino"],
      plot_summary: "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
      average_rating: 9.2,
      poster_url: "https://via.placeholder.com/300x450/dc2626/ffffff?text=Godfather"
    },
    {
      id: 3,
      title: "The Dark Knight",
      genres: ["Action", "Crime", "Drama"],
      director: "Christopher Nolan",
      cast: ["Christian Bale", "Heath Ledger"],
      plot_summary: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
      average_rating: 9.0,
      poster_url: "https://via.placeholder.com/300x450/7c3aed/ffffff?text=Dark+Knight"
    },
    {
      id: 4,
      title: "Pulp Fiction",
      genres: ["Crime", "Drama"],
      director: "Quentin Tarantino",
      cast: ["John Travolta", "Samuel L. Jackson"],
      plot_summary: "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
      average_rating: 8.9,
      poster_url: "https://via.placeholder.com/300x450/059669/ffffff?text=Pulp+Fiction"
    },
    {
      id: 5,
      title: "Forrest Gump",
      genres: ["Drama", "Romance"],
      director: "Robert Zemeckis",
      cast: ["Tom Hanks", "Robin Wright"],
      plot_summary: "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man.",
      average_rating: 8.8,
      poster_url: "https://via.placeholder.com/300x450/ea580c/ffffff?text=Forrest+Gump"
    }
  ]

  useEffect(() => {
    setMovies(mockMovies)
  }, [])

  const filteredMovies = movies.filter(movie =>
    movie.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    movie.genres.some(genre => genre.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const getRecommendations = (movieId) => {
    setLoading(true)
    // Simulate API call delay
    setTimeout(() => {
      const movie = movies.find(m => m.id === movieId)
      if (movie) {
        // Simple content-based recommendation: same genres
        const recs = movies.filter(m => 
          m.id !== movieId && 
          m.genres.some(genre => movie.genres.includes(genre))
        ).slice(0, 3)
        setRecommendations(recs)
        setSelectedMovie(movie)
      }
      setLoading(false)
    }, 1000)
  }

  const MovieCard = ({ movie, showRecommendButton = true }) => (
    <Card className="group hover:shadow-lg transition-all duration-300 hover:scale-105">
      <div className="relative overflow-hidden rounded-t-lg">
        <img 
          src={movie.poster_url} 
          alt={movie.title}
          className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>
      <CardHeader>
        <CardTitle className="text-lg font-bold">{movie.title}</CardTitle>
        <CardDescription className="flex items-center gap-2">
          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
          <span className="font-semibold">{movie.average_rating}</span>
          <span className="text-muted-foreground">• {movie.director}</span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-1 mb-3">
          {movie.genres.map(genre => (
            <Badge key={genre} variant="secondary" className="text-xs">
              {genre}
            </Badge>
          ))}
        </div>
        <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
          {movie.plot_summary}
        </p>
        <div className="mb-3">
          <p className="text-xs text-muted-foreground mb-1">Cast:</p>
          <p className="text-sm">{movie.cast.join(", ")}</p>
        </div>
        {showRecommendButton && (
          <Button 
            onClick={() => getRecommendations(movie.id)}
            className="w-full"
            disabled={loading}
          >
            <Sparkles className="w-4 h-4 mr-2" />
            Get Recommendations
          </Button>
        )}
      </CardContent>
    </Card>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Film className="w-8 h-8 text-primary" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                MovieRecommend
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search movies or genres..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-slate-900 to-slate-600 dark:from-slate-100 dark:to-slate-400 bg-clip-text text-transparent">
            Discover Your Next Favorite Movie
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Get personalized movie recommendations based on your preferences. 
            Click on any movie to discover similar films you might love.
          </p>
        </section>

        {/* Recommendations Section */}
        {selectedMovie && (
          <section className="mb-12">
            <div className="bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border">
              <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Users className="w-6 h-6 text-primary" />
                Recommendations based on "{selectedMovie.title}"
              </h3>
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                  <span className="ml-3 text-muted-foreground">Finding perfect matches...</span>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map(movie => (
                    <MovieCard key={movie.id} movie={movie} showRecommendButton={false} />
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Movies Grid */}
        <section>
          <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Film className="w-6 h-6 text-primary" />
            {searchTerm ? `Search Results (${filteredMovies.length})` : 'Popular Movies'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredMovies.map(movie => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
          {filteredMovies.length === 0 && searchTerm && (
            <div className="text-center py-12">
              <Film className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No movies found</h3>
              <p className="text-muted-foreground">Try searching for a different title or genre.</p>
            </div>
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-t mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Film className="w-6 h-6 text-primary" />
              <span className="text-lg font-semibold">MovieRecommend</span>
            </div>
            <p className="text-muted-foreground">
              Powered by advanced recommendation algorithms to help you discover amazing movies.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
