import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = "bae96be1ba274dc882c10b8b2b4beeb3"
SPOTIPY_CLIENT_SECRET = "d4ceb53253a44550af6d4dfe99a5898f"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
billboard_html = response.text

# print(URL)

soup = BeautifulSoup(billboard_html, "html.parser")
songs_soup = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")

songs_names = []
for song_name in songs_soup:
    name = song_name.getText()
    songs_names.append(name)

print(songs_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

songs_uris = []
for song_name in songs_names:
    song_search = sp.search(f"{song_name}", limit=1, type="track")
    try:
        song_uri = song_search["tracks"]["items"][0]["uri"]
    except IndexError:
        pass
    else:
        songs_uris.append(song_uri)

# print(songs_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=True, collaborative=False,
                                   description="100PythonCode")
playlist_id = playlist["id"]
print(sp.playlist_add_items(playlist_id=playlist_id, items=songs_uris))