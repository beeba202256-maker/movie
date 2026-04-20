from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Sample movie data (in real app, connect to TMDB API or database)
MOVIES = [
    {
        "id": 1,
        "title": "Interstellar",
        "year": 2014,
        "genre": ["Sci-Fi", "Drama"],
        "rating": 8.7,
        "duration": "2h 49m",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"]
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "year": 2008,
        "genre": ["Action", "Crime"],
        "rating": 9.0,
        "duration": "2h 32m",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/dqK9Hag1054tghRQSqLSfrkvQnA.jpg",
        "trailer": "https://www.youtube.com/embed/EXeTwQWrcwY",
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"]
    },
    {
        "id": 3,
        "title": "Inception",
        "year": 2010,
        "genre": ["Sci-Fi", "Thriller"],
        "rating": 8.8,
        "duration": "2h 28m",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/s3TBrRGB1iav7gFOCNx3H31MoES.jpg",
        "trailer": "https://www.youtube.com/embed/YoHD9XEInc0",
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"]
    },
    {
        "id": 4,
        "title": "Avengers: Endgame",
        "year": 2019,
        "genre": ["Action", "Adventure"],
        "rating": 8.4,
        "duration": "3h 1m",
        "description": "After the devastating events of Infinity War, the universe is in ruins. The Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
        "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/7RyHsO4yDXtBv1zUU3mTpHeQ0d5.jpg",
        "trailer": "https://www.youtube.com/embed/TcMBFSGVi1c",
        "director": "Anthony & Joe Russo",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"]
    },
    {
        "id": 5,
        "title": "Parasite",
        "year": 2019,
        "genre": ["Drama", "Thriller"],
        "rating": 8.5,
        "duration": "2h 12m",
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "poster": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
        "trailer": "https://www.youtube.com/embed/5xH0HfJHsaY",
        "director": "Bong Joon-ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"]
    },
    {
        "id": 6,
        "title": "Dune",
        "year": 2021,
        "genre": ["Sci-Fi", "Adventure"],
        "rating": 8.0,
        "duration": "2h 35m",
        "description": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.",
        "poster": "https://wallpapercave.com/wp/wp10254425.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/jYEW5xZkZk2WTrdbMGAPFuBqbDc.jpg",
        "trailer": "https://www.youtube.com/embed/8g18jFHCLXk",
        "director": "Denis Villeneuve",
        "cast": ["Timothée Chalamet", "Rebecca Ferguson", "Oscar Isaac"]
    },
    {
        "id": 7,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": ["Drama"],
        "rating": 9.3,
        "duration": "2h 22m",
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "poster": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
        "trailer": "https://www.youtube.com/embed/6hB3S9bIaco",
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"]
    },
    {
        "id": 8,
        "title": "Oppenheimer",
        "year": 2023,
        "genre": ["Drama", "History"],
        "rating": 8.3,
        "duration": "3h 0m",
        "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
        "poster": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/fm6KqXpkh7wm1k5qiCDHQQZLYkG.jpg",
        "trailer": "https://www.youtube.com/embed/uYPbbksJxIg",
        "director": "Christopher Nolan",
        "cast": ["Cillian Murphy", "Emily Blunt", "Matt Damon"]
    }
]

@app.route('/')
def index():
    return render_template('index.html', movies=MOVIES)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('detail.html', movie=movie, movies=MOVIES)

@app.route('/api/movies')
def api_movies():
    genre = request.args.get('genre', '')
    search = request.args.get('search', '').lower()
    
    filtered = MOVIES
    if genre:
        filtered = [m for m in filtered if genre in m['genre']]
    if search:
        filtered = [m for m in filtered if search in m['title'].lower() or search in m['description'].lower()]
    
    return jsonify(filtered)

@app.route('/api/movies/<int:movie_id>')
def api_movie(movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(movie)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
