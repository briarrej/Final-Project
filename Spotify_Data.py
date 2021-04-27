import spotipy
import spotipy.util as util
#from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import re
import os
import matplotlib.pyplot as plt
import csv
import unittest
import json
import sqlite3

def getSpotifyObject(username, scope):
    token = util.prompt_for_user_token(username, scope, client_id = '659482023a4b40c7b4356740ff599546', 
                                                            client_secret = 'b6ff42b1e22f4e94bdb0fa0e05789349',
                                                                redirect_uri='https://example.com/callback/')
    spotify = spotipy.Spotify(auth=token)
    return spotify

def user_info(spotify):
    return spotify.current_user()

def create_playlist(spotify):
    #user_id = spotify.user_info().get('id', "None")
    top_50_usa_data = spotify.playlist_tracks('37i9dQZF1DXcBWIGoYBM5M')
    top_50_uk_data = spotify.playlist_tracks('153yGNYdzvyCZxzDnIzNUx')
    song_tuple_list = []

    rank_counter = 1 
    for song in top_50_usa_data['items']:
        song_title = song['track']['name']
        song_artist = song['track']['artists'][0]['name']
        song_pop= song['track']['popularity']
        song_date = song['track']['album']['release_date']
        song_rank = rank_counter
        song_tuple_list.append((song_title, song_artist, song_rank, song_date, song_pop, "usa"))
        rank_counter += 1 

    rank_counter = 1 
    for song in top_50_uk_data['items']:
        song_title = song['track']['name']
        song_artist = song['track']['artists'][0]['name']
        song_pop= song['track']['popularity']
        song_date = song['track']['album']['release_date']
        song_rank = rank_counter
        song_tuple_list.append((song_title, song_artist, song_rank, song_date, song_pop, "uk"))
        rank_counter += 1 
    return song_tuple_list
    
#def spotify_viz_chart(song_tuple_list):
    #d = {}
    #for song in song_tuple_list:
        #song_title = song[1][1:-1]
        #print(song[4])
    
    
    #names = []
    #streams = []
    #i = 1

    #for item in d.items():
        #names.append(item[0])
        #streams.append(item[1])
        #i += 1
        #if i == 11:
            #break

    #plt.barh(names, streams, color="green")
    #plt.title("Tope 10 Highest Streamed Songs On Spotify")
    #plt.xlabel("Streams (millions)")
    #plt.ylabel("Song Title")

    #plt.tick_params(axis='x', rotation=50)
    #plt.show()


def join_tables(cur, conn):
    cur.execute("SELECT Hot100.song, ArtistIds.artist FROM Hot100 LEFT JOIN ArtistIds ON Hot100.artist_id = ArtistIds.artist_id")
    results = cur.fetchall()
    conn.commit()
    return results


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn, spotify):
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (song_title TEXT, song_artist TEXT, song_rank INTEGER, song_date TEXT, song_pop INTEGER, country_code TEXT)") 
    cur.execute("SELECT COUNT(*) FROM Spotify")
    add_25 = cur.fetchone()[0]
    for item in create_playlist(spotify)[add_25:add_25+25]:
        cur.execute("INSERT INTO Spotify (song_title, song_artist, song_rank, song_date, song_pop, country_code) VALUES (?, ?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4], item[5]))
        add_25 += 1
    conn.commit()


def main():
    spotify = getSpotifyObject("7tj4dlofb2yvuijru40p3grnp", 'playlist-modify-public')
    cur, conn = setUpDatabase('Billboard.db')
    createDatabase(cur, conn, spotify)
    playlist_songs = create_playlist(spotify)
    spotify_viz_chart(playlist_songs)
    conn.close()


if __name__ == "__main__":
    main()
