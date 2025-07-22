from flask import Flask, render_template
import pickle
import os

app = Flask(__name__)

# Load the pickled data safely
def load_popular_df():
    try:
        popular_pkl_path = os.path.join(os.path.dirname(__file__), 'popular.pkl')
        print(f"Loading popular.pkl from: {popular_pkl_path}")
        with open(popular_pkl_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("Error: 'popular.pkl' file not found. Please check the file path.")
    except Exception as e:
        print(f"Error loading 'popular.pkl': {e}")
    return None

popular_df = load_popular_df()

@app.route('/')
def index():
    error_message = None
    book_name = author = rating = num_ratings = []
    if popular_df is None:
        error_message = "Error: Could not load book data. Please check server logs for details."
    else:
        required_columns = ['Book-Title', 'Book-Author',  'avg_ratings']
        for col in required_columns:
            if col not in popular_df.columns:
                error_message = f"Error: Missing column '{col}' in 'popular.pkl'."
                break
        if not error_message:
            book_name = popular_df['Book-Title'].to_list()
            author = popular_df['Book-Author'].to_list()
            rating = popular_df['avg_ratings'].to_list()
    return render_template('index.html',
                           book_name=book_name,
                           author=author,
                           rating=rating,
                           num_ratings=num_ratings,
                           error_message=error_message
                           )

@app.route('/recommend')
def recommend_ui():
    error_message = None
    book_name = author = rating = []
    if popular_df is None:
        error_message = "Error: Could not load book data. Please check server logs for details."
    else:
        book_name = popular_df['Book-Title'].to_list()
        author = popular_df['Book-Author'].to_list()
        rating = popular_df['avg_ratings'].to_list()
    return render_template('recommend.html',
                           book_name=book_name,
                           author=author,
                           rating=rating,
                           error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)