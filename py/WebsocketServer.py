import SocketServer
import base64
import hashlib
import random


class WebsocketHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        
        shake = self.request.recv(1024);
        print shake;
        self.send_shake(shake);
        print "HandShake Finish"

        self.request.send("");

        while (1):
            data = self.request.recv(1024);
            #self.request.send(data);

            mask = data[2:6];
            text = data[6:]
            
            real_text = "";
            for i in range(len(text)):
                real_text += chr(ord(text[i]) ^ ord(mask[i % 4]));
            print real_text;

            header = data[0:6];
            req_text = real_text;

            mask = "".join([chr(random.randint(0, 255)) for i in range(4)]);

            header = header[0:2] + mask;
            req_body = "".join([chr(ord(req_text[i]) ^ ord(mask[i % 4])) for i in range(len(req_text))]);
            req_data = header + req_body;

            print "".join([chr(ord(req_body[i]) ^ ord(mask[i % 4])) for i in range(len(req_text))]);
            
            print ["%x " % ord(d) for d in req_data];

            self.send_data("test");
    def send_shake(self, shake):
        shake_dict = self.shake2dict(shake);

        print shake_dict

        seckey = shake_dict["Sec-WebSocket-Key"];
        seckey += "258EAFA5-E914-47DA-95CA-C5AB0DC85B11";
        ackey = base64.b64encode(hashlib.new("sha1", seckey).digest());
        
        result = 'HTTP/1.1 101 Switching Protocols\r\n';
        result += 'Upgrade: websocket\r\n';
        result += 'Connection: Upgrade\r\n';
        result += 'Sec-WebSocket-Accept: %s\r\n\r\n' % (ackey,);
        
        print result

        self.request.sendall(result);
        self.request.sendall( "\x81\x05\x48\x65\x6c\x6c\x6f")

    def send_data(self, data):
        packet = '\x81';
        packet += chr(len(data));
        packet += data;
        print self.request.sendall(packet);
        print packet;

    def shake2dict(self, shake):
        result = {};
        rows = shake.split("\r\n");
        for row in rows[1:]:
            if (row != ''):
                l = row.split(': ');
                result[l[0]] = l[1];

        return (result);


server = SocketServer.TCPServer(('localhost', 14226), WebsocketHandler);
server.handle_request();

