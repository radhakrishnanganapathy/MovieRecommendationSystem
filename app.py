import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
     try:
          # url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
          url = f"https://www.omdbapi.com/?t={movie_id}&apikey=c43e463f"

          data = requests.get(url)
          data = data.json()
          poster_path = data['Poster']
          # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
          full_path = poster_path

          return full_path
     except Exception as e:
          full_path = "image_not_found.webp"
          return full_path
def fetch_rating(movie_title):
    try:
          url = f"https://www.omdbapi.com/?t={movie_title}&apikey=c43e463f"

          data = requests.get(url)
          data = data.json()
          rating = data.get('imdbRating')
          # rating = data['Ratings'][0]
          return rating
    except Exception as e:
          return ("Rating Not Found")
        
def recommended(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(simalrity[index])), reverse=True, key=lambda x:x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    movie_rating = []
    for i in distances[0:21]:
         movie_id = movies.iloc[i[0]].movie_id
         movie_title = movies.iloc[i[0]].title
         recommended_movies_poster.append(fetch_poster(movie_title))
         recommended_movies_name.append(movies.iloc[i[0]].title)
         movie_rating.append(fetch_rating(movie_title))
    return recommended_movies_name ,recommended_movies_poster,movie_rating
     #    print(movies.iloc[i[0]].title)

st.header("Movie Recommendation system Using Machine Learning")
movies = pickle.load(open('articats/movie_list.pkl', 'rb'))
simalrity = pickle.load(open('articats/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox('movies list', movie_list)

if st.button('show Recommendation'):
     recommended_movies_name, recommended_movies_poster, movie_rating = recommended(selected_movie)

     # col1,col2,col3,col4,col5 = st.columns(5)
     # with col1:
     #      st.text(recommended_movies_name[0])
     #      st.image(recommended_movies_poster[0])
     # with col2:
     #      st.text(recommended_movies_name[1])
     #      st.image(recommended_movies_poster[1])
     # with col3:
     #      st.text(recommended_movies_name[2])
     #      st.image(recommended_movies_poster[2])
     # with col4:
     #      st.text(recommended_movies_name[3])
     #      st.image(recommended_movies_poster[3])
     # with col5:
     #      st.text(recommended_movies_name[4])
     #      st.image(recommended_movies_poster[4])
     num_recommendation = len(recommended_movies_name)
     num_cols = 5
     num_rows = -(-num_recommendation // num_cols)
     for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            index = row * num_cols + col
            if index < num_recommendation:
                with cols[col]:
                    st.text(recommended_movies_name[index])
                    st.image(recommended_movies_poster[index])
                    st.text(movie_rating[index])