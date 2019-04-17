import configparser

parser = configparser.ConfigParser()
parser.read('defaults.conf')

# Section Titles
MQTT = 'mqtt'
WEB = 'web'
HUE = 'hue'


class GeneralOptions(object):
    logo = """
    ___              __
   /   |  ____ ___  / /_  (_)___ _____  ________ 
  / /| | / __ `__ \/ __ \/ / __ `/ __ \/ ___/ _ \\
 / ___ |/ / / / / / /_/ / / /_/ / / / / /__/  __/
/_/  |_/_/ /_/ /_/_.___/_/\__,_/_/ /_/\___/\___/ 
    """


# MQTT Settings
class MqttOptions(object):
    broker_url: str = parser.get(MQTT, 'broker_url')
    ca_file: str = parser.get(MQTT, 'ca_file')
    client_cert_file: str = parser.get(MQTT, 'client_cert_file')
    client_key_file: str = parser.get(MQTT, 'client_key_file')
    topic_prefix: str = parser.get(MQTT, 'topic_prefix')


# Web Settings
class WebOptions(object):
    hostname: str = parser.get(WEB, 'hostname', fallback='localhost')
    port: int = parser.getint(WEB, 'port', fallback=8080)
    debug: bool = parser.getboolean(WEB, 'debug', fallback=False)


# Hue Settings
class HueOptions(object):
    bridge_url: str = parser.get(HUE, 'bridge_url', fallback='localhost')
    username: str = parser.get(HUE, 'username', fallback=None)
    create_username_on_start: bool = parser.getboolean(HUE, 'create_username_on_start', fallback=True)
