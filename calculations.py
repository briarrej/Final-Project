import json
import requests
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def set_connection(db_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+db_file)
        # print('connected')
    except:
        print('not connected')
    return conn

# get the number of weeks that songs typically spend on the charts 
def get_weeks_popularity(conn):
    #weeks_dict = {}
    cur = conn.cursor()
    weeks = cur.execute('SELECT weeks_id FROM BillBoardSongs').fetchall()


    # print(type(genres))
    weeks_list = []
    for weekID in weeks:
        weeks_list.append(weekID)
    week_dict = {}
    for num in weeks_list:
        if num in week_dict:
            week_dict[num] += 1
        else:
            week_dict[num] = 1
    return week_dict
# make visualization
def viz(data):
    weeksOnChart = []
    numOfSongs = []
    dataSorted = sorted(data.items(),key = lambda x:x[0])
    for i in dataSorted:
        weeksOnChart.append(i[0])
        numOfSongs.append(i[1])
    #print(weeksOnChart)
    newList = []
    for weeks in weeksOnChart:
        weeks = weeks[0]
        if weeks == 1:
            weeks ='less than 5 weeks'
        elif weeks == 2:
            weeks = 'less than 10 weeks' 
        elif weeks == 3:
            weeks = 'less than 15 weeks' 
        elif weeks == 4:
            weeks = 'less than 20 weeks'
        else:
            weeks = 'more than 20 weeks'
        newList.append(weeks)
    xposition = np.arange(len(newList))
    plt.bar(xposition, numOfSongs)
    plt.xticks(xposition, newList)
    plt.xlabel('The Numbers of Weeks on The Top 100')
    plt.ylabel('Number of Songs')
    plt.title('Average Amount of Time Spent on Billboard Top 100 ')
    plt.show()

#make spotify viz
def get_week_popularity(conn):
    #weeks_dict = {}
    cur = conn.cursor()
    weeks = cur.execute('SELECT weeks_id FROM Spotify').fetchall()

def spotify_viz_chart(song_tuple_list):
    d = {}
    weeks_on_chart = []
    numbOfSongs = []
    dataSorted = sorted(data.items(),key = lambda x:x[0])
    
    for i in dataSorted:
        weeks_on_chart.append(i[0])
        numbOfSongs.append(i[1])
    new_list = []
    
    for week in weeks_on_chart:
        weeks = weeks[0]

    
    
    
    for song in song_tuple_list:
        song_title = song[1][1:-1]
        #print(song[4])












def main():
    conn = set_connection('BillBoard.db')
    data = get_weeks_popularity(conn)
    viz(data)
    
main()