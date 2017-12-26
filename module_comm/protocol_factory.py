from autobahn.twisted.component import Component, run
from autobahn.twisted.component import inlineCallbacks


from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.internet.ssl import CertificateOptions, ClientContextFactory
from twisted.web.client import Agent


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

        self.__define_action_to_subscribe(command)
        run(self.__component)

    def stop(self):

        self.__session.leave()

    def __define_action_to_subscribe(self, action):

        @self.__component.on_join
        @inlineCallbacks
        def join(session, details):
            self.__session = session
            print("Session {} joined: {}".format(details.session, details))
            yield session.subscribe(self.__call_action, action)

    def __call_action(self, *args):

        if not self.bot.done:
            self.bot.action(args)

    def __str__(self):

        return "WAMP"


class RESTProtocol:

    def __init__(self, url, bot):

        self.__url = url
        self.bot = bot

        class WebClientContextFactory(ClientContextFactory):
            def getContext(self, hostname, port):
                return ClientContextFactory.getContext(self)
        context_factory = WebClientContextFactory()
        self.__agent = Agent(reactor, context_factory)

    def do(self, action):

        self.__define_action(action)

    def stop(self):

        print("---------------------------------------")

    def __define_action(self, command):

        url = self.__url+command
        url = url.encode()
        d = self.__agent.request(b'GET', url)
        d.addCallbacks(self.__print_resource, self.__print_error)
        d.addBoth(self.stop)

    def __print_resource(self, response):

        class ResourcePrinter(Protocol):
            def __init__(self, finished_inner, bot):
                self.finished = finished_inner
                self.bot = bot
                self.response = b""

            def dataReceived(self, data):
                self.response += data

            def connectionLost(self, reason):
                print(reason)
                self.bot.action(self.response)
                self.finished.callback(self.bot.stop)

        finished = Deferred()
        finished.addErrback(self.__print_error)

        response.deliverBody(ResourcePrinter(finished, self.bot))
        return finished

    def __print_error(self, failure):

        print("Something has gone wrong.")
        print(failure)
        self.stop()

    def __str__(self):

        return "REST"


class ProtocolFactory:

    __protocols = {
        "WAMP": WAMPProtocol,
        "REST": RESTProtocol
    }

    def get_protocols(self):

        return self.__protocols.keys()

    def create(self, protocol_name):

        return self.__protocols[protocol_name]