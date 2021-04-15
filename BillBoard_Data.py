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
    print(rankings)


    
    #do .text and look through the elements 
    #do re.findall to find all song titles 

  # with open('chart.json', 'w') as json_file:
   #     json.loads(chart.text)
    #chart_json = jso
    #print(titles)

#<div class="chart-list-item now-playing" data-rank="1" data-artist="Drake" data-title="What's Next" data-has-content="true">
            
getBillBoardLink()


#API_key = ''