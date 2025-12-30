from flask import Flask, request, url_for, render_template
import utils

app = Flask(__name__)


# since you’re already passing movie_df into the template, 
# the most reliable and efficient way to populate the <select> is to pass a simple list of titles 
# from the backend and then render them in Jinja. This avoids heavy DataFrame method calls inside 
# the template and keeps things fast.
@app.route("/", methods=['POST', 'GET'])
def index():
    selected_movie_name = None
    # If the form submits informations about the movie 
    if request.method == 'POST':
        # The selected movie name
        selected_movie_name = request.form.get("movie")
        # top_n value
        top_n = int(request.form.get("topn"))
        rec_movies = utils.recommend(selected_movie_name, utils.movies_df, utils.similarities, top_n)
        return render_template('rec.html', title="Home", movie_titles=utils.movies_df['title'].tolist(), rec_movies=rec_movies, movie_name=selected_movie_name)
        
        
    return render_template('index.html', title="Home", movie_titles=utils.movies_df['title'].tolist(), movie_name=selected_movie_name)



@app.route("/test")
def test():
    return render_template('index2.html', title="Home", movie_titles=utils.movies_df['title'].tolist(), movie_name=utils.movies_df['title'].iloc[0])
