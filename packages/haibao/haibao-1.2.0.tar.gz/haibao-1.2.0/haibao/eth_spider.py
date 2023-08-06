# -*- encoding: utf-8 -*-
import os
import sys
import json
from ws4py.client.threadedclient import WebSocketClient


class Client(WebSocketClient):
    def opened(self):
        data = {"op":"subscribe","args":[{"channel":"candle15m","instId":"ETH-USDT"}]}
        req = json.dumps(data)
        self.send(req)

    def closed(self, code, reason=None):
        print "closed down:", code, reason

    def received_message(self, resp):
        try:
            resp = json.loads(unicode(resp))
            data = resp['data'][0][4]
            os.system('cls')
            print u'ETH: {} / {:.2f}'.format(data, float(data) * 6.5)
        except:
            pass
