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

cid = '659482023a4b40c7b4356740ff599546'
secret = 'b6ff42b1e22f4e94bdb0fa0e05789349'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getSpotifyLink():
    url = 'https://spotifycharts.com/regional'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Spotify")
    cur.execute("CREATE TABLE Spotify (song TEXT, artist TEXT, rank INTEGER)") 
    song, artist, ranking = getSpotifyLink()
    for item in range(len(song))[:25]:
        cur.execute("INSERT INTO Spotify (song, artist, rank) VALUES (?, ?, ?)", (song[item], artist[item], ranking[item]))
    conn.commit()









def main():
    getSpotifyLink()
    cur, conn = setUpDatabase('Spotify.db')
    createDatabase(cur, conn)

main()