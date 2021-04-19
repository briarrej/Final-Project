import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json
import sqlite3

def getSpotifyData():
    token = util.prompt_for_user_token(	'7tj4dlofb2yvuijru40p3grnp', scope = 'playlist-modify-public', 
    cid = '659482023a4b40c7b4356740ff599546',
    secret = 'b6ff42b1e22f4e94bdb0fa0e05789349',
    redirect_uri='https://example.com/callback/',
    sp = spotipy.Spotify(token))


def join_tables(cur, conn):
    cur.execute("SELECT Hot100.song, ArtistIds.artist FROM Hot100 LEFT JOIN ArtistIds ON Hot100.artist_id = ArtistIds.artist_id")
    results = cur.fetchall()
    conn.commit()
    return results


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+Spotify.db)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Spotify")
    cur.execute("CREATE TABLE Spotify (song TEXT, artist TEXT, rank INTEGER)") 
    song, artist, ranking = getSpotifyData()
    for item in range(len(song))[:25]:
        cur.execute("INSERT INTO Spotify (song, artist, rank) VALUES (?, ?, ?)", (song[item], artist[item], ranking[item]))
    conn.commit()



#def set_up_spotify_table:

#def write_data_to_file:





def main():
    getSpotifyLink()
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/Spotify.db')
    cur = conn.cursor()

    cur, conn = setUpDatabase('Spotify.db')
    createDatabase(cur, conn)

    set_up_spotify_table(cur, conn)

    write_data_to_file("spotify_data.txt", cur, conn)

    conn.close()



if __name__ == "__main__":
    main()
