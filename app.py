import base64
from requests import post, get, request
from dotenv import load_dotenv
from pytube import YouTube, Search
import json
import os


#--------------------------------------------SPOTIFY PARSING--------------------------------------------------

#Spotify Api authentication Pre-Requesites
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#Grabs the token needed for the Spotify API to function
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode (auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def check_website_validity(url):
    if len(url) != 22:
        return False
    return True

token = get_token()

#Grabs the first 100 songs in a playlist and returns a list of the song name and the artist
def get_playlist_songs(token, spotify_url):
    url = f"https://api.spotify.com/v1/playlists/{spotify_url}/tracks"  
    if check_website_validity(spotify_url):
        header = get_auth_header(token)
        result = get(url, headers=header)
        tracks = []
        total = int(json.loads(result.content)["total"])
        for i in range(total):
            if i == 100:
                break
            artistname = (json.loads(result.content)["items"][i]["track"]["artists"][0]['name'])
            songname = (json.loads(result.content)["items"][i]["track"]["name"])
            newtrack = artistname + " " + songname
            tracks.append(newtrack)
        return tracks
    print("Not a real link...")

#Grabs the tracks in an album and returns a dictionary
def get_album_songs(token, spotify_url):
    url = f"https://api.spotify.com/v1/albums/{spotify_url}/tracks"  
    if check_website_validity(spotify_url):
        header = get_auth_header(token)
        result = get(url, headers=header)
        tracks = {}
        items = []
        total = int(json.loads(result.content)["total"])
        name = (json.loads(result.content)["items"][0]["artists"][0]['name'])
        for i in range(total):
            if i == 100:
                break
            items.append(json.loads(result.content)["items"][i]["name"])
        tracks[name] = items
        return tracks
    print("Not a real link...")

#Grabs the song name and returns a string in the format of (Artist - Song)
def get_song_song(token, spotify_url):
    url = f"https://api.spotify.com/v1/tracks/{spotify_url}"
    header = get_auth_header(token)
    result = get(url, headers=header)
    artistname = (json.loads(result.content)["artists"][0]["name"])
    songname = (json.loads(result.content)["name"])
    track = artistname + " " + songname
    return track

#Isolates the spotify playlist ID
def playlist_string_cleaner(spotify_link):
    key = "https://open.spotify.com/playlist/"
    if key in spotify_link:
        spotify_link = spotify_link.replace(key, '')
        count = 0
        str = []
        for char in spotify_link:
            if char == "?":
                break
            str += char
            count += 1
            if count == 22:
                return ''.join(str)  
    return 0

#isolates the song ID
def song_string_cleaner(spotify_link):
    key = "https://open.spotify.com/track/"
    if key in spotify_link:
        spotify_link = spotify_link.replace(key, '')
        count = 0
        str = []
        for char in spotify_link:
            if char == "?":
                break
            str += char
            count += 1
            if count == 22:
                return ''.join(str) 
    return 0

#isolates the spotify album ID
def album_string_cleaner(spotify_link):
    key = "https://open.spotify.com/album/"
    if key in spotify_link:
        spotify_link = spotify_link.replace(key, '')
        count = 0
        str = []
        for char in spotify_link:
            if char == "?":
                break
            str += char
            count += 1
            if count == 22:
                return ''.join(str)  
    return 0

#Runs the functions necessary to retrieve the dictionary for albums
def get_album(spotify_link):
    valid_link = False
    while valid_link == False:
        final_link = album_string_cleaner(spotify_link)
        if final_link == 0:
            return 0
        else:
            valid_link = True
        
    track = get_album_songs(token, final_link)
    return track

#Retrieves a string in the format of (Artist - Song)
def get_song(spotify_link):
    valid_link = False
    while valid_link == False:
        final_link = song_string_cleaner(spotify_link)
        if final_link == 0:
            return 0
        else:
            valid_link = True

    track = get_song_song(token, final_link)
    return track

#Runs the functions necessary to retrieve the dictionary for playlists
def get_playlist(spotify_link):
    valid_link = False
    while valid_link == False:
        final_link = playlist_string_cleaner(spotify_link)
        if final_link == 0:
            return 0
        else:
            valid_link = True

    track = get_playlist_songs(token, final_link)
    return track

#--------------------------------------DOWNLOADING AND LINK PARSING---------------------------------------------------


#returns a list of the playlist's track urls
def get_playlist_links(spotify_link):
    track = get_playlist(spotify_link)
    if track == 0:
        return 0
    playlist_url = []
    for song in track:
        search = Search(song)
        link = search.results[0].watch_url
        playlist_url.append(link)
    return playlist_url

#returns a list variable of a song url
def get_song_link(spotify_link):
    track = get_song(spotify_link)
    if track == 0:
        return 0
    song_url = []
    search = Search(track)
    link = search.results[0].watch_url
    song_url.append(link)
    return song_url

#returns a list of the album's track urls
def get_album_links(spotify_link):
    track = get_album(spotify_link)
    if track == 0:
        return 0
    new_tracks = []
    playlist_url = []
    artist = list(track)
    for x in range(len(track[artist[0]])):
        new_string = artist[0] + " " + track[artist[0]][x]
        new_tracks.append(new_string)
    for song in new_tracks:
        search = Search(song)
        link = search.results[0].watch_url
        playlist_url.append(link)
    return playlist_url

#returns the file destination for the download
def getDestination():
    destination = input("Enter the file destination: ")
    return destination

#downloads the music through the links given in the list
def download(links, destination):
    for link in links:
        yt = YouTube(link)
        video = yt.streams.get_audio_only()
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

#downloads playlists
def download_playlist(spotify_link, destination):
    links = get_playlist_links(spotify_link)
    if links == 0:
        return 0
    download(links, destination)
    return 1

#download song
def download_song(spotify_link, destination):
    link = get_song_link(spotify_link)
    if link == 0:
        return 0
    download(link, destination)
    return 1

#downloads albums
def download_album(spotify_link, destination):
    links = get_album_links(spotify_link)
    if links == 0:
        return 0
    download(links, destination)
    return 1

#END

#IMPLEMENTATION OF COPY
