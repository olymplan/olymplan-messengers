import sys
import threading
from yowsup.layers                                     import YowLayerEvent, EventCallback
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.common.tools import Jid
from yowsup.layers.network import YowNetworkLayer

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def createBotLayer(token_='', port_=3000):
    class BotLayer(YowInterfaceLayer):
        EVENT_START = "org.openwhatsapp.yowsup.event.cli.start"
        token = token_
        port = port_

        def __init__(self):
            super(BotLayer, self).__init__()
            YowInterfaceLayer.__init__(self)
            self.login = False

        @ProtocolEntityCallback("message")
        def onMessage(self, messageProtocolEntity):

            if messageProtocolEntity.getType() == 'text':
                self.onTextMessage(messageProtocolEntity)

            print(messageProtocolEntity.getBody())

            self.toLower(messageProtocolEntity.ack())
            self.toLower(messageProtocolEntity.ack(True))

            #outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            #    'Привет! Это Олимплан.',
            #    to=messageProtocolEntity.getFrom())
            #self.toLower(outgoingMessageProtocolEntity)

        @EventCallback(EVENT_START)
        def onStart(self, layerEvent):
            self.getLayerInterface(YowNetworkLayer).connect()
            self.inputThread = threading.Thread(target=self.startInputThread)
            self.inputThread.daemon = True
            self.inputThread.start()
            print('Started')
            return True

        def startInputThread(self):
            self.run(port=self.port)

        def run(self, server_class=HTTPServer, port=80):
            handler = createServer(self)
            server_address = ('', port)
            httpd = server_class(server_address, handler)
            print('Starting httpd...')
            httpd.serve_forever()

        @ProtocolEntityCallback("receipt")
        def onReceipt(self, entity):
            self.toLower(entity.ack())

        @ProtocolEntityCallback("success")
        def onSuccess(self, entity):
            print('Logged in!')
            self.login = True

        def onTextMessage(self,messageProtocolEntity):
            pass

        def message_send(self, number, content):
            if self.login:
                outgoingMessage = TextMessageProtocolEntity(content.encode("utf-8") if sys.version_info >= (3,0) else content, to=self.phoneToJid(number))
                self.toLower(outgoingMessage)
            else:
                print('Not logged in.')

        def phoneToJid(self, phone):
            return Jid.normalize(phone)
    return BotLayer

def createServer(layer_):
    class Server(BaseHTTPRequestHandler):
        layer = layer_

        def __init__(self, *args, **kwargs):
            super(Server, self).__init__(*args, **kwargs)
            #self.layer = layer

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            self.wfile.write(b"<html><body><h1>Get outta here.</h1></body></html>")

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            self._set_headers()
            content_len = self.headers.get_all('content-length')
            if content_len:
                content_len = int(content_len[0])
                post_body = self.rfile.read(content_len)
                print(post_body)
            else:
                self.wfile.write(b"bad request")
                return
            try:
                data = json.loads(post_body)
            except json.decoder.JSONDecodeError as e:
                print('Error while decoding JSON: {}'.format(e))
                self.wfile.write(b"bad request")
                return
            if not 'to' in data or not 'message' in data or not 'token' in data or data['token'] != self.layer.token:
                self.wfile.write(b"bad request")
                print(data)
                return
            print('Sending {} to {}'.format(data['message'], data['to']))
            try:
                self.layer.message_send(data['to'], data['message'])
            except Exception as e:
                print('Exception while sending: {}'.format(e))

            self.wfile.write(b"success")
            return

    return Server