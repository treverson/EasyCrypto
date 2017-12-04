from autobahn.twisted.component import Component, run
from autobahn.twisted.component import inlineCallbacks
from twisted.internet.ssl import CertificateOptions

component = Component(
    realm=u'realm1',
    transports=[{
        'endpoint': {
            'type': 'tcp',
            'host': u'api.poloniex.com',
            'port': 443,
            'tls': CertificateOptions()
        },
        'type': 'websocket',
        'url': u'wss://api.poloniex.com',
        'options': {
            'open_handshake_timeout': 60.0
        }
    }]
)

def on_event(*args):
    print('{0}: {1} A:{2} B:{3} {4}% V:{5} H:{8} L:{9}'.format(*args))

@component.on_join
@inlineCallbacks
def join(session, details):
    print("Session {} joined: {}".format(details.session, details))
    yield session.subscribe(on_event, 'ticker')

if __name__ == '__main__':
    run(component)