from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json
import sqlite3
import spotipy.util as util
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def getSpotifyLink():
    url = 'https://spotifycharts.com/regional'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')















def main():
    getSpotifyLink()
    cur, conn = setUpDatabase('Spotify.db')
    createDatabase(cur, conn)

main()