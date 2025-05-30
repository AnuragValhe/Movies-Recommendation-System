import pickle
import streamlit as st
import requests
import time
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry
import pandas as pd

movies_dict = pickle.load(open('Saved Models/movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('Saved Models/similarity.pkl','rb'))


def fetch_poster_by_title(title):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key=7ecb2c4e8b87694c5d849a9392295ea5&query={title}"
        for _ in range(3):  # retry up to 3 times
            response = requests.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    poster_path = data['results'][0].get('poster_path')
                    if poster_path:
                        return "https://image.tmdb.org/t/p/w92/" + poster_path
            time.sleep(1)  # small delay before retry
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")
    return "https://via.placeholder.com/300x450?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    m_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in m_list:
        title = movies.iloc[i[0]].title
        recommended_movie_names.append(title)
        recommended_movie_posters.append(fetch_poster_by_title(title))
    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    names,posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
