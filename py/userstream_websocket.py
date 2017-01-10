import socket;
import threading;
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from threading import Thread, Lock
import datetime
from datetime import timedelta
import time
import base64
import hashlib
import MySQLdb

PORT = 7000;
DUMP = True;

def get_oauth():
    consumer_key = 'dTFlSvzNIkROO6BfAkTsDQ'
    consumer_secret = 'UnWZeo7rxdx38aVnGhbZSdmiraNgSUnwGuTxYdrvts'
    access_key = '105981624-84OpytBltuseQ1XWx2hTAlhQO9oO8IpSiSnxgL0e'
    access_secret = 'Kh3xAsVLyBiEESfRVpqp1WE4KVZH2w46JlKUU5wOI'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth


def handle(client, connection):
    print "-" * 100;
    lock = threading.Lock();

    lock.acquire();
    client.handshake();
    client.recv_init_data();
    lock.release();
    if (DUMP == True):
        client.dumpdata();

    while (1):
        recv_data = connection.recv(1024);
        print recv_data;
        
        if (len(recv_data) == 0 or ord(recv_data[0]) & 0xf == 0x8):
            connection.send("\x88");
            break;
    print "-" * 100;
    print "connect_end";
    print "-" * 100;
    lock.acquire();
    clients.remove(client);
    lock.release();
    connection.close();



class Client:
    def __init__(self, connect):
        self._is_handshaked = False;
        self._connect = connect;
        self._tags = [];
    
    def dumpdata(self):
        print self._is_handshaked;
        print self._tags;

    def send(self, data):
        if (self._is_handshaked == True):
            data = data.encode("utf8");
            header = "\x81";
            header += chr(len(data));
            self._connect.send(header + data);
    def handshake(self):
        handshake_data = self._connect.recv(1024);
        print handshake_data;
        handshake_dict = self.shake2dict(handshake_data);
        seckey = handshake_dict["Sec-WebSocket-Key"];
        seckey += "258EAFA5-E914-47DA-95CA-C5AB0DC85B11";
        ackey = base64.b64encode(hashlib.new("sha1", seckey).digest());
        
        result = 'HTTP/1.1 101 Switching Protocols\r\n';
        result += 'Upgrade: websocket\r\n';
        result += 'Connection: Upgrade\r\n';
        result += 'Sec-WebSocket-Accept: %s\r\n\r\n' % (ackey,);
        
        print result;

        self._connect.send(result);

        print "handshake finish";
    
    def recv_init_data(self):
        self._name = self.recv();
        print self._name;
        connector = MySQLdb.connect(host="localhost", db='twippt', user="root", passwd="26nKZAzS", charset="utf8");
        cursor = connector.cursor();
        cursor.execute("SELECT id FROM slide WHERE name = '%s'" % self._name);
        temp = cursor.fetchone();
        if (temp == None):
            self._tags = [];
        else:
            slide_id = temp[0];
            cursor.execute("SELECT text FROM tag WHERE id IN (SELECT tag_id FROM tag_slide_relation WHERE slide_id = %s)" % slide_id);
            tag_names = cursor.fetchall();
            self._tags = [tag_name[0] for tag_name in tag_names];
        cursor.close();
        connector.close();
        self._is_handshaked = True;

        print "init data recv";

    def recv(self):
        data = self._connect.recv(1024);
        header = data[:2];
        mask = data[2:6];
        body = data[6:];
        return "".join([chr(ord(body[i]) ^ ord(mask[i % 4])) for i in range(len(body))]);

    def shake2dict(self, shake):
        result = {};
        rows = shake.split("\r\n");
        for row in rows[1:]:
            if (row != ''):
                l = row.split(': ');
                result[l[0]] = l[1];

        return (result);
    def is_listen_tag(self, tag):
        return (tag in self._tags);
    def is_handshaked(self):
        return (self._is_handshaked);

class MyStreamListener(StreamListener):
    def on_status(self, status):
        status.created_at += timedelta(hours=9)
        tags = [];
        text = status.text;
        while (True):
            start_index = text.find('#');
            if (start_index == -1):
                break;
            end_index = text[start_index:].find(" ");
            if (end_index == -1):
                end_index = len(text);
            elif (len(text) != end_index + start_index):
                end_index = end_index + start_index;

            tag = text[start_index + 1 : end_index];
            tags.append(tag);
            lst = text.split("#" + tag, 1);
            text = lst[0] + lst[1];
        lock = threading.Lock();
        lock.acquire();
        for client in clients:
            for tag in tags:
                if (client.is_handshaked() == True and client.is_listen_tag(tag) == True):
                    client.send(text);
                    break;
        lock.release();
        
        print(u"{text}".format(text=status.text))

class TwitterThread(Thread):
    def init(self, stream, track):
        self.stream = stream;
        self.track = track;
    def run(self):
        self.stream.filter(track=self.track);
        print "end stream";


def track_controler(track, stream):
    now_track = track;
    while (1):
        connector = MySQLdb.connect(host="localhost", db='twippt', user="root", passwd="dameyo", charset="utf8");
        cursor = connector.cursor();
        cursor.execute("SELECT text FROM tag");
        new_track = [str("#" + t[0]) for t in cursor.fetchall()];
        print new_track;
        if (len(now_track) < len(new_track)):
            now_track = new_track;
            stream.disconnect();
            thread = TwitterThread();
            thread.init(stream, now_track);
            thread.start();
            print now_track;
        cursor.close();
        connector.close();
        time.sleep(5);

clients = [];

lock = threading.Lock();
s = socket.socket();
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT))
s.listen(1)
auth = get_oauth();
stream = Stream(auth, MyStreamListener());
track = ["#test",];
thread = TwitterThread();
thread.init(stream, track);
thread.start();
threading.Thread(target=track_controler, args=(track, stream,)).start();
while (True):
    (conn, addr) = s.accept();
    client = Client(conn);
    lock.acquire();
    clients.append(client);
    lock.release();
    threading.Thread(target=handle, args=(client, conn)).start();

