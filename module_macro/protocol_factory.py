from autobahn.twisted.component import Component, run
from autobahn.twisted.component import inlineCallbacks
from twisted.internet.ssl import CertificateOptions

class ProtocolFactory:

    __protocols = {
        "WAMP":  WAMPProtocol
    }

    def get_protocols(self):

        return self.__protocols.keys()

    def create(self, protocol_name):

        return self.__protocols[protocol_name]


class WAMPProtocol:

    def __init__(self, url):

        self.__component = Component(
            realm=u'realm1',
            transports=[{
                'endpoint': {
                    'type': 'tcp',
                    'host': u'api.poloniex.com',
                    'port': 443,
                    'tls': CertificateOptions()
                },
                'type': 'websocket',
                'url': url,
                'options': {
                    'open_handshake_timeout': 60.0
                }
            }]
        )

        @self.__component.on_join
        @inlineCallbacks
        def join(session, details):
            print("Session {} joined: {}".format(details.session, details))
            yield session.subscribe(self.__ticker, 'ticker')

    def do(self, command):

        if command == "ticker":
            run(self.__component)

    def __ticker(self, *args):
        print('{0}: {1} A:{2} B:{3} {4}% V:{5} H:{8} L:{9}'.format(*args))