import configparser

parser = configparser.ConfigParser()
parser.read('defaults.conf')

# Section Titles
MQTT = 'mqtt'
WEB = 'web'


# MQTT Settings
class MqttOptions(object):
    broker_url: str = parser[MQTT].get('broker_url')
    ca_file: str = parser[MQTT].get('ca_file')
    client_cert_file: str = parser[MQTT].get('client_cert_file')
    client_key_file: str = parser[MQTT].get('client_key_file')
    topic_prefix: str = parser[MQTT].get('topic_prefix')


# Web Settings
class WebOptions(object):
    hostname: str = parser[WEB].get('hostname', fallback='localhost')
    port: int = parser[WEB].get_int('port', fallback=8080)
    debug: bool = parser[WEB].get_bool('debug', fallback=False)

