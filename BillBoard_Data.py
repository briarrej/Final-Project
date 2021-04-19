from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json
import sqlite3

def getBillBoardLink():
    url = 'https://www.billboard.com/charts/Hot-100/2021-03-20'
    resp = requests.get(url)
    #print(resp.content)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    songTitles = []
    songs = soup.find_all('span', class_ = "chart-list-item__title-text")
    for song in songs:
        goodSong = song.text.strip()
        songTitles.append(goodSong)
    #print(songTitles)
    
    artistNames = []
    artists = soup.find_all('div', class_ = "chart-list-item__artist")
    for artist in artists:
        goodArtist = artist.text.strip()
        artistNames.append(goodArtist)
    #print(artistNames)

    rankings = []
    ranks = soup.find_all('div', class_ = "chart-list-item__position")
    for rank in ranks:
        goodRank = rank.text.strip()
        rankings.append(goodRank)
    #print(songTitles, artistNames, rankings)
    return songTitles, artistNames, rankings
    #print(rankings)

    #peak = []
    #songPeaks = soup.find_all('div', class_ = "chart-list-item__position")


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn, startIndex):
    #cur.execute("DROP TABLE IF EXISTS BillBoard")
    #cur, conn = setUpDatabase('BillBoard.db')
    song, artist, ranking = getBillBoardLink()
    for item in range(startIndex, startIndex + 25):
        cur.execute("INSERT INTO BillBoard (song, artist, rank) VALUES (?, ?, ?)", (song[item], artist[item], ranking[item]))
    conn.commit()

def main():
    getBillBoardLink()
    cur, conn = setUpDatabase('BillBoard.db')
    cur.execute("CREATE TABLE IF NOT EXISTS BillBoard (song TEXT, artist TEXT, rank INTEGER UNIQUE)") 
    cur.execute('SELECT max (rank) from BillBoard')
    startIndex = cur.fetchone()[0]
    if startIndex == None:
        startIndex = 0
    createDatabase(cur, conn, startIndex)
    
main()

#API_key = ''