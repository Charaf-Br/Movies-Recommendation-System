import pickle
import pandas as pd
import tmdbsimple as tmdb
from dotenv import load_dotenv
import os


# Load the variables in .env file
load_dotenv()

# Set the API key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY is missing. Set it in .env or the environment.")
else:
    # set the API KEY
    tmdb.API_KEY = TMDB_API_KEY


# Load the pickle files
movies_df = pickle.load(open('data\\movies_list.pkl', 'rb'))
similarities = pickle.load(open('data\\similarity.pkl', 'rb'))


def fetch_more_details(movie_id : int):
    result = {
        "homepage": pd.NA,
        "overview": pd.NA,
        "popularity": pd.NA,
        "poster_path": pd.NA,
        "tagline": pd.NA,
        "revenue": pd.NA,
        "runtime": pd.NA
        
    }
    # Instantiate the object
    movie = tmdb.Movies(movie_id)
    # Get movie details
    movie_info = movie.info()
    
    # Fetch the home page
    if 'homepage' in movie_info:
        result['homepage'] = movie_info.get('homepage')
    
    # Fetch the overview
    if 'overview' in movie_info:
        result['overview'] = movie_info.get('overview')
        
    # Fetch the popularity
    if 'popularity' in movie_info:
        result['popularity'] = movie_info.get('popularity')
    
    # Fetch the tagline
    if 'tagline' in movie_info:
        result['tagline'] = movie_info.get('tagline')
        
    # Fetch the revenue
    if 'revenue' in movie_info:
        result['revenue'] = movie_info.get('revenue')
        
    # Fetch the runtime
    if 'runtime' in movie_info:
        result['runtime'] = movie_info.get('runtime')
        
    # Fetch the poster path
    base_url = "https://image.tmdb.org/t/p/w500"
    if 'poster_path' in movie_info:
        poster_path = movie_info.get('poster_path')
        result['poster_path'] = base_url + poster_path
    
    return result


def recommend(title : str, movies_df : pd.DataFrame, sim_matrix, top_n=10):
    if title in movies_df['title'].values:
        movies_index = movies_df[movies_df['title'] == title].index.item() # return the index of the row matching the title (eg; "avatar" index = 0)
        scores = dict(enumerate(sim_matrix[movies_index])) # returns the indices of the films and their similarities with the film with index "movie_index" [this includes also the movie itself so we need to eliminate the first element]
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)) # first we use sorted() to sort the list of pairs (key = "movie_index", item = "similarity_score") which we obtained using (scores.items()), and we use a lambda function to sort by score (because by default it is sorted by the key cuz it is the first element in the pair) and we used reverse=True because we need a DESC order (by default it is ASC but we want the most similar movies so we need greater scores) and because the result is a list we need to transform it to a dict to keep the access easy to movies_scores (ie; each score is mapped to the movie_index so we can easily know which movie it is ad its score)
        
        selected_movies_index = [movie_id for movie_id, _ in sorted_scores.items()] # we will take the movies indices sorted by similarity scores
        selected_movies_score = [scores for _, scores in sorted_scores.items()] # we will take the similarity scores of movies sorted from the greater to the lesser
        
        # Create a new dataframe that is indexed using the sorted movies' indices by score similarity
        rec_movies = movies_df.iloc[selected_movies_index]
        rec_movies['similarity'] = selected_movies_score
        
        # Reset indices
        rec_movies = rec_movies.reset_index(drop=True)
        # Keep only top_n rows and skip the first row (because the first row represent the movie itself [it is naturally the most similar movie to itself])
        #! rec_movies = rec_movies[1:top_n+1]
        
        # Keep the selected movie to show its details before showing recommendation
        rec_movies = rec_movies[0:top_n+1]
        
        # fetch the movies posters
        movie_more_details = [fetch_more_details(movie_id) for movie_id in rec_movies['tmdb_id']]
        
        homepage = []
        overview = []
        popularity = []
        poster_path = []
        tagline = []
        revenue = []
        runtime = []
        for details_dict in movie_more_details:
            homepage.append(details_dict.get("homepage"))
            overview.append(details_dict.get("overview"))
            popularity.append(details_dict.get("popularity"))
            poster_path.append(details_dict.get("poster_path"))
            tagline.append(details_dict.get("tagline"))
            revenue.append(details_dict.get("revenue"))
            runtime.append(details_dict.get("runtime"))    
            
        rec_movies["homepage"] = homepage
        rec_movies["overview"] = overview
        rec_movies["popularity"] = popularity
        rec_movies["poster_path"] = poster_path
        rec_movies["tagline"] = tagline
        rec_movies["revenue"] = revenue
        rec_movies["runtime"] = runtime
        
        return rec_movies # Return the top_n similar movies while skipping the first 
    else:
        print("Title not in dataset. Please check spelling.")
        return pd.NA
    
    
