from flask import Flask, request, jsonify
from flask_cors import CORS
from app import recommend_book, book_names
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        book_name = data.get('book_name')
        if not book_name:
            return jsonify({"error": "Book name is required"}), 400

        recommended_books, poster_url = recommend_book(book_name)
        return jsonify({
            "recommended_books": recommended_books,
            "poster_urls": poster_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/book_names', methods=['GET'])
def get_book_names():
    try:
        # Convert pandas Index to list and handle empty case
        books_list = book_names.tolist() if hasattr(book_names, 'tolist') else list(book_names)
        if not books_list:
            return jsonify({"error": "No books available"}), 404
        return jsonify({"book_names": books_list})
    except Exception as e:
        print(f"Error in get_book_names: {str(e)}")  # For debugging
        return jsonify({"error": "Failed to fetch book names"}), 500

if __name__ == '__main__':
    # Print the type and first few items of book_names for debugging
    print(f"book_names type: {type(book_names)}")
    print(f"First few book names: {list(book_names)[:5] if hasattr(book_names, '__iter__') else 'Not iterable'}")
    app.run(debug=True, port=5000)