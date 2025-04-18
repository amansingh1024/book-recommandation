import pickle
import numpy as np
import pandas as pd

# Load your model and data files
def load_data():
    try:
        model = pickle.load(open('artifacts/model.pkl', 'rb'))
        book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
        final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
        book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
        return model, book_names, final_rating, book_pivot
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

# Initialize global variables
try:
    model, book_names, final_rating, book_pivot = load_data()
except Exception as e:
    print(f"Failed to initialize data: {e}")
    raise

# Function to fetch posters
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion[0]:
        try:
            book_name.append(book_pivot.index[book_id])
            ids = np.where(final_rating['title'] == book_name[-1])[0][0]
            ids_index.append(ids)
            url = final_rating.iloc[ids]['image_url']
            poster_url.append(url)
        except IndexError:
            print(f"Could not find data for book id: {book_id}")
            poster_url.append("")  # Add a placeholder URL

    return poster_url

# Recommendation function
def recommend_book(book_name):
    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
        poster_url = fetch_poster(suggestion)
        
        recommended_books = [book_pivot.index[book_id] for book_id in suggestion[0]]
        return recommended_books, poster_url
    except Exception as e:
        print(f"Error in recommend_book: {e}")
        return [], []

if __name__ == "__main__":
    print("app.py is running...")
    # Print some debug information
    print(f"Number of books loaded: {len(book_names) if hasattr(book_names, '__len__') else 'Unknown'}")