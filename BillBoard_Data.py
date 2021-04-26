from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def getBillBoardLink():
    url = 'https://www.billboard.com/charts/Hot-100/2021-03-27'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    songTitles = []
    songs = soup.find_all('span', class_ = "chart-list-item__title-text")
    for song in songs:
        goodSong = song.text.strip()
        songTitles.append(goodSong)
  
    
    artistNames = []
    artists = soup.find_all('div', class_ = "chart-list-item__artist")
    for artist in artists:
        goodArtist = artist.text.strip()
        artistNames.append(goodArtist)

    rankings = []
    ranks = soup.find_all('div', class_ = "chart-list-item__position")
    for rank in ranks:
        goodRank = rank.text.strip()
        rankings.append(goodRank)


    weeksOnTop100 = []
    songWeeksOnChart = soup.find_all('div', class_= "chart-list-item__weeks-on-chart")
    for song in songWeeksOnChart:
        goodWeek = int(song.text.strip())
        weeksOnTop100.append(goodWeek)
    
    #print(weeksOnTop100)
    

    songCategory = []
    for song in weeksOnTop100:
        if song < 5:
            songCat = 1
        if song < 10:
            songCat = 2
        elif song < 15:
            songCat = 3
        elif song < 20:
            songCat = 4
        elif song < 25:
            songCat = 5
        else:
            songCat = 6
        songCategory.append(songCat)
    return songTitles, artistNames, rankings, weeksOnTop100, songCategory

    
#weeksOnChart()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn, startIndex):
    song, artist, ranking, weeksOnTop100, songCategory = getBillBoardLink()
    #print(startIndex)
    for item in range(startIndex, startIndex + 25):
        cur.execute("INSERT INTO BillBoardSongs (song, artist, rank, weeks_id) VALUES (?, ?, ?, ?)", (song[item], artist[item], ranking[item], songCategory[item]))
    conn.commit()
def createDatabase2(cur, conn):
    stringWeeks = ['weeks less than 5', 'weeks less than 10', 'weeks less than 15', 'weeks less than 20', 'weeks over 20']
    #song, artist, ranking, weeksOnTop100, songCategory = getBillBoardLink()
    cur.execute('SELECT max (songCategory) from WeeksID')
    maxNum = cur.fetchone()[0]
    if maxNum == 5:
        pass
    else:
        for item in range(5):
            cur.execute("INSERT INTO WeeksID (songCategory, weeks) VALUES (?, ?)", (item+1, stringWeeks[item]))
    conn.commit()

    #pass

def main():
    getBillBoardLink()
    cur, conn = setUpDatabase('BillBoard.db')
    cur.execute("CREATE TABLE IF NOT EXISTS BillBoardSongs (song TEXT, artist TEXT, rank INTEGER UNIQUE, weeks_id INTEGER)") 
    cur.execute("CREATE TABLE IF NOT EXISTS WeeksID (songCategory INTEGER, weeks TEXT)") 
    cur.execute('SELECT* FROM BillBoardSongs JOIN WeeksID ON BillBoardSongs.weeks_id = WeeksID.songCategory')
    cur.execute('SELECT max (rank) from BillBoardSongs')
    startIndex = cur.fetchone()[0]
    if startIndex == None:
        startIndex = 0
    createDatabase(cur, conn, startIndex)
    createDatabase2(cur, conn)
    
main()

#API_key = ''