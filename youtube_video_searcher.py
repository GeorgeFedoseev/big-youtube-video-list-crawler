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

from pprint import pprint

import re
from time import time
import os

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
            #pprint(search_result)
            title = search_result["snippet"]["title"]

            if re.sub(u'[^а-яё]', '',  title).strip() != "":
                #print title
                videos.append(search_result)    
        

    #print "Videos:\n", "\n".join(videos), "\n"

    if "nextPageToken" in search_response and page < MAX_PAGES:
        print search_response['nextPageToken']
        videos = videos + youtube_search(query, search_response['nextPageToken'], page+1)



    return videos

if __name__ == "__main__":

    output_videos_file = "yt_rus_vids.txt"
    processed_words_file = 'processed_words.txt'
    dictionary_file = 'word_rus.txt'

    all_video_ids = []
    dict_lines = []
    processed_lines = []

    # read saved data
    with open(output_videos_file, 'r') as vids_f:
        all_video_ids = [x.strip() for x in vids_f.readlines()]

    with open(processed_words_file, 'r') as processed_f:
        processed_lines = [x.strip() for x in processed_f.readlines()]

    # read dict file
    with open(dictionary_file, 'r') as dict_f:
        dict_lines = [x.strip() for x in dict_f.readlines()]

    print "previously processed %i/%i words, got %i videos" % (len(processed_lines), len(dict_lines), len(all_video_ids))



    with open(output_videos_file, 'a+') as vids_f:
        with open(processed_words_file, 'a+') as processed_f:

            searches_count = 0      

            save_every = 50

            started_time = time()

            print "started time: %f" % started_time


            for l in dict_lines:
                l = l.strip()

                print l
                if l in processed_lines:
                    continue

                try:
                    results = youtube_search(l)
                except Exception as ex:
                    print "Exception: "+str(ex)
                    break

                video_ids = [x["id"]["videoId"] for x in results if x["id"]["videoId"] not in all_video_ids]

                for vid_id in video_ids:
                    vids_f.write("%s\n" % vid_id)


                if searches_count % save_every == 0:
                    print "FLUSH"
                    # flush video ids
                    vids_f.flush()
                    os.fsync(vids_f.fileno())

                    # flush processed
                    processed_f.write("%s\n" % l)
                    processed_f.flush()
                    os.fsync(processed_f.fileno())

                    print "FLUSHED"

                all_video_ids += video_ids
              
                searches_count += 1

                elapsed_time = time() - started_time

                print "elapsed_time: %f" % elapsed_time

                print "%i searches, %i videos found, seconds per dict word: %.2f" % (len(processed_lines) + searches_count, len(all_video_ids), elapsed_time/searches_count)

                    

                








