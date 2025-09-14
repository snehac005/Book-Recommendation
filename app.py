from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Home route - displays some predefined popular books from Google Books
@app.route('/')
def index():
    # Fetching a static list of books as "popular"
    query = "bestseller fiction"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=12"
    response = requests.get(url).json()

    book_name = []
    author = []
    publisher = []
    image = []
    votes = []     # Placeholder
    rating = []    # Placeholder

    if 'items' in response:
        for item in response['items']:
            volume_info = item.get('volumeInfo', {})
            book_name.append(volume_info.get('title', 'Unknown Title'))
            author.append(", ".join(volume_info.get('authors', ['Unknown Author'])))
            publisher.append(volume_info.get('publisher', 'Unknown Publisher'))
            image.append(volume_info.get('imageLinks', {}).get('thumbnail', ''))
            votes.append('N/A')  # Google Books API doesn't give votes
            rating.append(volume_info.get('averageRating', 'N/A'))

    return render_template('index.html',
                           book_name=book_name,
                           author=author,
                           publisher=publisher,
                           image=image,
                           votes=votes,
                           rating=rating)

# Recommendation page
@app.route('/recommendation')
def recommendation_ui():
    return render_template('recommendation.html')

# Recommendation logic using Google Books API
@app.route("/recommend", methods=['POST'])
def recommendation():
    user_input = request.form.get('user_input')
    url = f"https://www.googleapis.com/books/v1/volumes?q={user_input}&maxResults=5"
    response = requests.get(url).json()

    if 'items' not in response:
        return render_template('recommendation.html', error="❌ Book not found. Try another title.")

    data = []
    for item in response['items']:
        volume_info = item.get('volumeInfo', {})
        title = volume_info.get('title', 'Unknown Title')
        author = ", ".join(volume_info.get('authors', ['Unknown Author']))
        image = volume_info.get('imageLinks', {}).get('thumbnail', '')

        data.append([title, author, image])

    return render_template('recommendation.html', data=data)

# Optional API route for frontend JavaScript usage
@app.route("/api/recommend", methods=['POST'])
def recommend_api():
    data = request.get_json()
    user_input = data.get('user_input', '')
    url = f"https://www.googleapis.com/books/v1/volumes?q={user_input}&maxResults=5"
    response = requests.get(url).json()

    if 'items' not in response:
        return jsonify({'success': False, 'message': '❌ Book not found.'}), 404

    recommendations = []
    for item in response['items']:
        volume_info = item.get('volumeInfo', {})
        recommendations.append({
            'title': volume_info.get('title', 'Unknown Title'),
            'author': ", ".join(volume_info.get('authors', ['Unknown Author'])),
            'image': volume_info.get('imageLinks', {}).get('thumbnail', '')
        })

    return jsonify({'success': True, 'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
