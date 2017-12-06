from autobahn.twisted.component import Component, run
from autobahn.twisted.component import inlineCallbacks
from twisted.internet.ssl import CertificateOptions


class WAMPProtocol:

    def __init__(self, url, bot):

        self.bot = bot

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

    def do(self, command):

        self.__define_action(command)
        run(self.__component)

    def stop(self):

        self.__session.leave()

    def __define_action(self, action):

        @self.__component.on_join
        @inlineCallbacks
        def join(session, details):
            self.__session = session
            print("Session {} joined: {}".format(details.session, details))
            print(action)
            yield session.subscribe(self.__call_action, action)

    def __call_action(self, *args):

        print("cos")
        if not self.bot.done:
            self.bot.action(args)

    def __str__(self):

        return "WAMP"


class ProtocolFactory:

    __protocols = {
        "WAMP":  WAMPProtocol
    }

    def get_protocols(self):

        return self.__protocols.keys()

    def create(self, protocol_name):

        return self.__protocols[protocol_name]