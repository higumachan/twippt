#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta
from threading import Thread
import sqlite3

def get_oauth():
# 以下4つのキー等は適宜取得して置き換えてください。
    consumer_key = 'dTFlSvzNIkROO6BfAkTsDQ'
    consumer_secret = 'UnWZeo7rxdx38aVnGhbZSdmiraNgSUnwGuTxYdrvts'
    access_key = '105981624-84OpytBltuseQ1XWx2hTAlhQO9oO8IpSiSnxgL0e'
    access_secret = 'Kh3xAsVLyBiEESfRVpqp1WE4KVZH2w46JlKUU5wOI'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

class AbstractedlyListener(StreamListener):
    """ Let's stare abstractedly at the User Streams ! """
    def on_status(self, status):
        status.created_at += timedelta(hours=9)
        text = status.text;
        start_index = text.find('#');
        end_index = text.find(" ");
        if (end_index == -1):
            end_index = len(text);
        elif (len(text) != end_index + 1):
            end_index = end_index + 1;

        print "end_index:" + str(end_index);
        tag = text[start_index + 1 : end_index];
        print "tag:" + tag;
        connector = sqlite3.connect("../test.db");
        cursor = connector.cursor();
        cursor.execute("SELECT COUNT(id) FROM tweet");
        tw_id = cursor.fetchone()[0];
        connector.execute("INSERT INTO tweet VALUES('%s', 'false', '%s', -1, %s, '%s')" % (tag, text, tw_id, "tekito"));
        connector.commit();
        cursor.close();
        connector.close();
        
        print(u"{text}".format(text=status.text))

class TwitterThread(Thread):
    def init(self, stream):
        self.stream = stream;
    def run(self):
        stream.filter(track=["#settestset",]);
if __name__ == '__main__':
    auth = get_oauth()
    stream = Stream(auth, AbstractedlyListener())
    thread = TwitterThread();
    thread.init(stream);
    thread.start();
    import time

