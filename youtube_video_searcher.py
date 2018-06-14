#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime

# yt api
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# threading
from threading import Thread


import sys
reload(sys)
sys.setdefaultencoding('utf8')


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCIxk2Yt6Pc4WvuHWKfNFG075YqXttJQDQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MAX_PAGES = 0


def youtube_search(query, pageToken=None, page=0):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.

    print 'GETTING PAGE %i of query %s' % (page, query)

    #if pageToken != None:
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=50,
        type="video",
        videoCaption="closedCaption",
        pageToken=pageToken,        
        regionCode="RU",
        relevanceLanguage='ru'
    ).execute()
    

    videos = []
    

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result["id"]["videoId"])
        

    #print "Videos:\n", "\n".join(videos), "\n"

    if "nextPageToken" in search_response and page < MAX_PAGES:
        print search_response['nextPageToken']
        videos = videos + youtube_search(query, search_response['nextPageToken'], page+1)



    return videos

if __name__ == "__main__":
    print youtube_search("пиджак")
