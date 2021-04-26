from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json
import sqlite3

def getBillBoardLink():
    url = 'https://www.billboard.com/charts/Hot-100/2021-03-27'
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

def weeksOnChart():
    url = 'https://www.billboard.com/charts/Hot-100/2021-03-27'
    resp = requests.get(url)
    #print(resp.content)
    soup = BeautifulSoup(resp.text, 'html.parser')

    weeksOnTop100 = []
    songCategory = []
    songWeeksOnChart = soup.find_all('div', class_= "chart-list-item__weeks-on-chart")
    for song in songWeeksOnChart:
        goodWeek = int(song.text.strip())
        weeksOnTop100.append(goodWeek)
    for song in weeksOnTop100:
        if song < 5:
            songCat = 1
        elif song < 10:
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
    #print(songCategory)

   # print(weeksOnTop100)

    return weeksOnTop100, songCategory

    
#weeksOnChart()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn, startIndex):
    song, artist, ranking = getBillBoardLink()
    for item in range(startIndex, startIndex + 25):
        cur.execute("INSERT INTO BillBoardSongs (song, artist, rank) VALUES (?, ?, ?)", (song[item], artist[item], ranking[item]))
    conn.commit()

def createDatabase2(cur, conn, startIndex):
    weeksOnTop, songCategory = weeksOnChart()
    for item in range(startIndex, startIndex + 25):
        cur.execute("INSERT INTO WeeksOnTopChart (weeks, songCategory) VALUES (?, ?)", (weeksOnTop[item], songCategory[item]))
    conn.commit()
    

def main():
    getBillBoardLink()
    cur, conn = setUpDatabase('BillBoard.db')
    cur.execute("CREATE TABLE IF NOT EXISTS BillBoardSongs (song TEXT, artist TEXT, rank INTEGER UNIQUE)") 
    cur.execute("CREATE TABLE IF NOT EXISTS WeeksOnTopChart (weeks INTEGER, songCategory INTEGER)")
    cur.execute('SELECT max (rank) from BillBoardSongs')
    startIndex = cur.fetchone()[0]
    if startIndex == None:
        startIndex = 0
    createDatabase(cur, conn, startIndex)
    createDatabase2(cur, conn, startIndex)
    
main()

#API_key = ''