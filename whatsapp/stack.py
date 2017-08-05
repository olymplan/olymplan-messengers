import sys
from yowsup.stacks import  YowStackBuilder
from layer import createBotLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

class BotStack(object):
    def __init__(self, credentials, encryptionEnabled = True, port=3000, token=''):
        stackBuilder = YowStackBuilder()

        self.botLayer = createBotLayer(token_=token, port_=port)

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(self.botLayer)\
            .build()

        self.stack.setCredentials(credentials)
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(self.botLayer.EVENT_START))

        try:
            self.stack.loop(timeout=0.5, discrete=0.5)
        except AuthError as e:
            print("Auth Error, reason %s" % e)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
