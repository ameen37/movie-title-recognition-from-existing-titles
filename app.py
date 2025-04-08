from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load the updated dataset
titles_file = "titles_dataset.csv"
if not os.path.exists(titles_file):
    raise FileNotFoundError(f"Dataset file '{titles_file}' not found. Make sure it's in the project directory.")

titles_df = pd.read_csv(titles_file)

@app.route('/', methods=['GET', 'POST'])
def home():
    movie_details = None
    
    if request.method == 'POST':
        new_title = request.form.get('new_title', '').strip()
        
        if new_title:
            movie_row = titles_df[titles_df['Title'].str.lower() == new_title.lower()]
            if not movie_row.empty:
                movie_details = {
                    "title": movie_row.iloc[0]['Title'],
                    "release_date": movie_row.iloc[0]['Release Date'],
                    "star_cast": movie_row.iloc[0]['Star Cast'],
                    "director": movie_row.iloc[0]['Director'],
                    "poster_path": f"static/posters/{movie_row.iloc[0]['Title'].replace(' ', '_')}.jpg"
                }
            else:
                movie_details = "Movie not found in database."
        else:
            movie_details = "Please enter a title."
    
    return render_template('index.html', movie=movie_details)

if __name__ == '_main_':
    app.run(debug=True)