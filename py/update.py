#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta
from threading import Thread, Lock
import datetime
import MySQLdb
import time;

lock = Lock();
tws = [];

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
        print text[start_index + 1:];
        end_index = text[start_index:].find(" ");
        if (end_index == -1):
            end_index = len(text);
        elif (len(text) != end_index + start_index):
            end_index = end_index + start_index;

        print "start_index:" + str(start_index);
        print "end_index:" + str(end_index);
        tag = text[start_index + 1 : end_index];
        print "tag:" + tag;
        lst = text.split("#" + tag, 2);
        print lst;
        text = lst[0] + lst[1];
        lock.acquire();
        tws.append((tag, text, "tekito"));
        lock.release();
        
        print(u"{text}".format(text=status.text))

class TwitterThread(Thread):
    def init(self, stream, track):
        self.stream = stream;
        self.track = track;
    def run(self):
        stream.filter(track=track);

if __name__ == '__main__':
    connector = MySQLdb.connect(host="localhost", db='twippt', user="root", passwd="26nKZAzS");
    cursor = connector.cursor();
    auth = get_oauth()
    stream = Stream(auth, AbstractedlyListener())
    thread = TwitterThread();
    track = ["#test",];
    thread.init(stream, track);
    thread.start();
    cursor.execute("SELECT COUNT(id) FROM tag");
    tag_count = cursor.fetchone()[0];
    while (True):
        start = time.time();
        while (time.time() - start):
            time.sleep(1);
            lock.acquire();
            for tw in tws:
                cursor.execute("SELECT COUNT(id) FROM tweet");
                tw_id = cursor.fetchone()[0];
                cursor.execute("SELECT id, slide_id FROM tag_slide_relation WHERE tag = '%s'" % (tw[0],));
                temp = cursor.fetchone();
                tag_id = temp[0];
                slide_id = temp[1];
                cursor.execute("INSERT INTO tweet VALUES(%s, '%s', 'false', '%s', %s)" % (tw_id, tw[1], datetime.datetime.now().isoformat(), slide_id));
                cursor.execute("INSERT INTO tag_tweet_relation VALUES(%s, %s, %s)" % (new_id, tag_id, tw_id));
            if (tws):
                connector.commit();
            tws = [];
            lock.release();
        try:
            cursor.execute("SELECT COUNT(id) FROM tag");
        except:
            print "Ellor21"
        new_tag_count = cursor.fetchone()[0];
        if (new_tag_count > tag_count):
            stream.disconnect();
            try:
                cursor.execute("SELECT COUNT(id) FROM tag");
            except:
                print "Erorr";
            track = [t[0] for t in cursro.fetchall()];
            thread.init(stream, track);
            thread.run();
    cursor.close();
    connector.close();
