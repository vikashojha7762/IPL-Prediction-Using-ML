import streamlit as st
import requests
import pandas as pd


movies = pd.read_csv('tmdb_5000_movies.csv')
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load the pickled files
try:
    with open('model/movie_list.pkl', 'rb') as file:
        movies = pickle.load(file)
    print("Movies loaded successfully.")
except FileNotFoundError:
    print("Error: movie_list.pkl file not found.")
except pickle.UnpicklingError:
    print("Error: Unpickling error while loading movie_list.pkl.")
except Exception as e:
    print(f"An error occurred while loading movie_list.pkl: {e}")

try:
    with open('model/similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
    print("Similarity loaded successfully.")
except FileNotFoundError:
    print("Error: similarity.pkl file not found.")
except pickle.UnpicklingError:
    print("Error: Unpickling error while loading similarity.pkl.")
except Exception as e:
    print(f"An error occurred while loading similarity.pkl: {e}")

# Ensure 'Vector' is defined
try:
    # Assuming 'Vector' is defined somewhere in your code
    # For example, it could be a result of some processing done on 'movies'
    # Vector = some_processing_function(movies)
    
    # Example placeholder for Vector
    Vector = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # This should be replaced with your actual data
    
    similarity = cosine_similarity(Vector)
    print("Cosine similarity calculated successfully.")
except NameError:
    print("Error: 'Vector' is not defined.")
except Exception as e:
    print(f"An error occurred while calculating cosine similarity: {e}")


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
import pickle

try:
    with open('model/movie_list.pkl', 'rb') as file:
        movies = pickle.load(file)
    print("Movies loaded successfully.")
except FileNotFoundError:
    print("Error: movie_list.pkl file not found.")
except pickle.UnpicklingError:
    print("Error: Unpickling error while loading movie_list.pkl.")
except Exception as e:
    print(f"An error occurred while loading movie_list.pkl: {e}")

try:
    with open('model/similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
    print("Similarity loaded successfully.")
except FileNotFoundError:
    print("Error: similarity.pkl file not found.")
except pickle.UnpicklingError:
    print("Error: Unpickling error while loading similarity.pkl.")
except Exception as e:
    print(f"An error occurred while loading similarity.pkl: {e}")


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])