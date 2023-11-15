from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64
import os
from requests import post, get
import json

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_token():
    auth_string = clientID + ":" + clientSecret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)

    result.raise_for_status()

    json_result = result.json()
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    print(json_result)

def search_song(song_name):
    results = sp.search(q=song_name, type='track')

    songs = results['tracks']['items']
    for song in songs:
        print(f"Name: {song['name']}")
        print(f"Artist: {song['artists'][0]['name']}")
        print("=========================")


def search_artist(artist_name):
    results = sp.search(q=artist_name, type='artist')

    artists = results['artists']['items']
    for artist in artists:
        print(f"Name: {artist['name']}, ID: {artist['id']}")

search_value = input("Type song name:")
search_song(search_value)