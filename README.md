# Movies-Recommendation-System
## Overview
MovieRecs is a sleek, Tailwind‑styled Flask web application that delivers fast, high‑quality movie recommendations from a curated dataset of 7,000+ titles. Users select a film and choose how many recommendations to fetch, then explore a polished details panel (overview, genres, runtime, revenue...) alongside a responsive grid of suggested movies. The cinematic dark‑glass UI, typeahead search, and TMDB integration for posters make discovery intuitive, visually engaging, and performant.

### Home page
<p align='center'>
  <img src="https://github.com/Charaf-Br/Movies-Recommendation-System/blob/a334f659b0dee17b4b32b19240ef758f56857d36/static/assets/homepage.png">
</p>

### Movie Detail Page
<p align='center'>
  <img src="https://github.com/Charaf-Br/Movies-Recommendation-System/blob/a334f659b0dee17b4b32b19240ef758f56857d36/static/assets/movie_details.png">
</p>

### Recommendation Page
<p align='center'>
  <img src="https://github.com/Charaf-Br/Movies-Recommendation-System/blob/a334f659b0dee17b4b32b19240ef758f56857d36/static/assets/rec_page.png">
</p>

## Features
- Beautiful dark/glassy UI (Tailwind) with responsive layout.
- Select dropdown + typeahead text input for movie titles.
- Slider to choose the number of recommendations (Top‑N).
- Selected movie panel (poster + details table).
- Recommended movies grid (up to 5 per row).
- TMDB integration for posters/metadata (via API key).
- Jinja2 templating with robust formatting and fallbacks.


## Content-based similarity
The content-based recommender system is highly based on the similarity calculation among items. The similarity or closeness of items is measured based on the similarity in the content or features of those items. The important features used in this project are:
- Keywords
- Genres
- Production companies
- Director
- Cast
- Original language
- Origin country

## Steps taken to build the recommender systems
- **Data Collection:** Gathered a comprehensive dataset of over 7,000 movies, including metadata such as titles, genres, release dates, and other relevant attributes.
- **Data Cleaning:** Processed and standardized the dataset by handling missing values, normalizing text fields, and ensuring consistent formatting for different fields.
- **Build the Recommender System:** Implemented a similarity-based recommendation engine using a precomputed similarity matrix derived from movie features, enabling accurate and fast recommendations.
- **Build the Web App with Flask:** Developed a responsive, Tailwind-styled Flask application featuring a cinematic UI, dynamic dropdowns, typeahead suggestions, and integration with the TMDB API for fetching posters and additional movie details.

## Data Sources:
- [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv)
- [IMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/carolzhangdc/imdb-5000-movie-dataset)
- [Lists of films by country and year](https://en.wikipedia.org/wiki/Category:Lists_of_films_by_country_and_year)
