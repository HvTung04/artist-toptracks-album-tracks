import os
from dotenv import load_dotenv
import base64
import json
from requests import post, get

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token():
    '''
    In this function we get Spotify token by the Client Credentials flow
    -> Only able to access endpoints that do not access user information
    (unscoped data)
    About Client Credentials Flow: https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow 
    '''
    # Generate <client_id:client_secret> in base64 as required
    auth_string = spotify_client_id + ':' + spotify_client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials",}
    # Send POST request
    result = post(url, headers=headers, data=data)
    # Load and extract access token
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    '''
    This function generate authorization header as instructed in:
    https://developer.spotify.com/documentation/web-api/concepts/access-token
    '''
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    '''
    In this function we use Spotify API to search for artist.
    About Spotify search API: https://developer.spotify.com/documentation/web-api/reference/search
    '''
    url = "https://api.spotify.com/v1/search" 
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    # Send GET request
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']

    if len(json_result) == 0:
        print("Artist doesnt exist")
        return None
    
    return json_result[0]

def search_for_album(token, album_name):
    '''
    In this function we use Spotify API to search for album.
    About Spotify search API: https://developer.spotify.com/documentation/web-api/reference/search
    '''
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=1&market=VN"

    query_url = url + query
    # Send GET request
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['albums']['items']

    if len(json_result) == 0:
        print("No album with this name exist...")
        return None
    
    return json_result[0]

def get_artist_top_tracks(token, artist_id):
    '''
    This function get 10 top tracks from an artist in Viet Nam, country code VN
    About get artist's top tracks: https://developer.spotify.com/documentation/web-api/reference/get-an-artists-top-tracks
    '''
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=VN"
    headers = get_auth_header(token)
    # Send GET request
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_album_tracks(token, album_id):
    '''
    This function get tracks from an album
    About get album's tracks: https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks
    '''
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    # Send GET request
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

token = get_token()
artist_name = "Bruno Mars"
album_name = "99%"

artist_id = search_for_artist(token, artist_name)['id']
album_id = search_for_album(token, album_name)['id']

print(f"Top tracks from {artist_name}.")
artist_top_tracks = get_artist_top_tracks(token, artist_id)
for idx, song in enumerate(artist_top_tracks):
    print(f"{idx+1}. {song['name']}")

print(f"Top tracks from {album_name} album.")
album_tracks = get_album_tracks(token, album_id)
for idx, song in enumerate(album_tracks):
    print(f"{idx+1}. {song['name']}")
