"""
Database functions and YT api request for channel names, and video status (true=live, false=removed)
"""
import requests
import sqlite3
from datetime import date
import csv

"""
Global Variables
"""

#date for adding
today = date.today()

#name and filepath conventions
db = 'YTdatabase'
filepath = 'C:\\Users\\j.attwood\\Documents\\Python Scripts\\YoutubeAPI\\Spreadsheets\\videos.csv'

"""
Database functions
"""
#Create database table
def createTable(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"""CREATE TABLE {db} (
        videoID text primary key,
        YTChannelName text,
        date text,
        videoStatus NULL
        )""")
    conn.commit()
    conn.close()
    print('Table created!')

#Show all data in record
def show_all_data(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(f"SELECT videoID, * FROM {db}")
    objs = c.fetchall()

    for obj in objs:
        print(obj)

    conn.commit()
    conn.close()

#add a single record
def add_record(videoID, YTChannelName=None, date=today, videoStatus=False):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"INSERT INTO {db} VALUES (?,?,?,?)", (videoID, YTChannelName, today, videoStatus, ))
    conn.commit()
    conn.close()
    print('Data added!')

#add a list of records (list will be passed in as function arguement)
def addList(data):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.executemany(f"INSERT INTO {db} VALUES (?,?,?,?)", data, )
    conn.commit()
    conn.close()
    print('Data list added!')

#delete single line of data
def delete_data(videoID):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"DELETE from {db} WHERE videoID = (?)", (videoID, ))
    conn.commit()
    conn.close()
    print('Data has been deleted!')

def delete_channel(YTChannelName):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"DELETE from {db} WHERE YTChannelName = (?)", (YTChannelName, ))
    conn.commit()
    conn.close()
    print('Channel has been deleted!')

#lookup YT Channel Name
def lookup(YTChannelName):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"SELECT * from {db} WHERE YTChannelName = (?)", (YTChannelName, ))
    objs = c.fetchall()

    if len(objs) == 0:
        print('No data found')

    for obj in objs:
        print(obj)

def returnList(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(f"SELECT videoID, * FROM {db}")
    objs = c.fetchall()
    output = [i for i in objs]
    return output

def returnTrue(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(f"SELECT videoID, * FROM {db} WHERE videoStatus = TRUE")
    objs = c.fetchall()
    output = [i for i in objs]
    return output

def returnFalse(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(f"SELECT videoID, * FROM {db} WHERE videoStatus = FALSE")
    objs = c.fetchall()
    output = [i for i in objs]
    return output


def updateData(boolValue, videoID):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(f"""UPDATE {db} SET videoStatus = {bool(boolValue)}, date = (?)
            WHERE videoID = (?)""", (today, videoID, ))
    # c.execute(f"""UPDATE {db} SET date = (?)
    #             WHERE videoID = (?)""", (today, videoID, ))
    conn.commit()
    conn.close()
    print(f"{videoID} updated")

def updateMany(data):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for item in data:
        c.execute(f"""UPDATE {db} SET videoStatus = TRUE, date = (?)
                WHERE videoID = (?)""", (today, item, ))
    conn.commit()
    conn.close()
    print(f"{data} updated")


"""
Youtube API functions
"""
def youtubeStatus(id_of_video):
    api_key = 'AIzaSyA-SLqDUtyMcKGGoUxJXL0mYQ2cRsbWoq0'
    url = f'https://www.googleapis.com/youtube/v3/videos?id={id_of_video}&key={api_key}&part=status'
    url_get = requests.get(url)
    result = url_get.json()['items'][0]['status']['publicStatsViewable']
    return result


def youtubeContents(id_of_video):
    api_key = 'AIzaSyA-SLqDUtyMcKGGoUxJXL0mYQ2cRsbWoq0'
    url = f'https://www.googleapis.com/youtube/v3/videos?id={id_of_video}&key={api_key}&part=snippet'
    url_get = requests.get(url)
    result = url_get.json()['items'][0]['snippet']['channelId']
    return result


"""
CSV/Spreadsheet handling functions
"""
def csvFileOut(filepath):
    videoIDs = []
    with open(filepath) as csvfile:
        array = [i for i in list(csvfile)]

    for i in array:
        i = i.strip()
        videoIDs.append(i)
    return videoIDs


print(show_all_data(db))











