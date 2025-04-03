import requests
import webbrowser
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
person=input("Name an Actor/Actress: ")
url = f"https://api.themoviedb.org/3/search/person?api_key={API_KEY}&query={person}"
response = requests.get(url)
data = response.json()["results"]
person_id=data[0]["id"]
credit_url=f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={API_KEY}"
credits_response = requests.get(credit_url)
credits_data = credits_response.json()

#find titles of all associated movies in credits_data
titles = [movie["title"] for movie in credits_data["cast"]]
#find popularity of all associated movies in credits_data
popularity = [movie["popularity"] for movie in credits_data["cast"]]
#combine titles and popularity into a list of tuples
data=list(zip(titles, popularity))
#Drop list into dataframe and sort by popularity
df=pd.DataFrame(data, columns=["Title", "Popularity"])
df.sort_values(by="Popularity", ascending=False, inplace=True)


top_10_list=[i for i in df["Title"][:10]]
path_list=[]

for i in top_10_list:
    movie_info_url=f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={i}"
    movie_info_response = requests.get(movie_info_url)
    movie_info_data = movie_info_response.json()
    movie_poster_path = movie_info_data["results"][0]["poster_path"]
    path_list.append(movie_poster_path)

for Rank, Movie in enumerate(top_10_list):
    print(Rank+1, Movie)

for i in path_list:
    url=f"https://image.tmdb.org/t/p/w500{i}"
    webbrowser.open(url)
