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
        tag = MySQLdb.escape_string(tag.encode("utf-8"));
        text = MySQLdb.escape_string(text.encode("utf-8"));
        tws.append((tag, text, "tekito"));
        lock.release();
        
        print(u"{text}".format(text=status.text))

class TwitterThread(Thread):
    def init(self, stream, track):
        self.stream = stream;
        self.track = track;
    def run(self):
        self.stream.filter(track=track);

if __name__ == '__main__':
    connector = MySQLdb.connect(host="localhost", db='twippt', user="root", passwd="26nKZAzS", charset="utf8");
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
        print start, time.time() - start < 10
        while (time.time() - start < 10):
            time.sleep(1);
            lock.acquire();
            for tw in tws:
                print tw[0], track;
                if ('#' + tw[0] in track):
                    cursor.execute("SELECT COUNT(id) FROM tweet");
                    tw_id = cursor.fetchone()[0];
                    cursor.execute("SELECT id FROM tag WHERE text = '%s'" % (tw[0],));
                    tag_id = cursor.fetchone()[0];
                    cursor.execute("SELECT slide_id FROM tag_slide_relation WHERE tag_id = %s" % (tag_id,));
                    temp = cursor.fetchone();
                    slide_id = temp[0];
                    cursor.execute("INSERT INTO tweet VALUES(%s, '%s', false, '%s', %s)" % (tw_id, tw[1], datetime.datetime.now().replace(microsecond=0).isoformat(), slide_id));
                    cursor.execute("SELECT COUNT(id) FROM tag_tweet_relation");
                    new_id = cursor.fetchone()[0];
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
        if (new_tag_count > len(track)):
            print "Came Change Track";
            try:
                cursor.execute("SELECT text FROM tag");
            except:
                print "Erorr";
            track = ['#' +  t[0] for t in cursor.fetchall()];
            print track;
            stream.disconnect();
            thread = TwitterThread();
            thread.init(stream, track);
            thread.start();

    cursor.close();
    connector.close();
