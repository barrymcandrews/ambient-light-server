from ambiance import configuration
from ambiance.router import Router
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1

config = configuration.MqttOptions
client = MQTTClient(config={
    'certfile': config.client_cert_file,
    'keyfile': config.client_key_file
})
router = Router(client=client)


async def start_client():
    await client.connect(uri=config.broker_url, cafile=config.ca_file)
    print("Connected to MQTT Broker @ " + config.broker_url)

    await client.subscribe([(t.topic, t.qos) for t in router.topics])
    while True:
        try:
            await router.push(await client.deliver_message())
        except Exception as e:
            print(e)
            raise


@router.topic('color', QOS_1)
def handle_color_change():
    pass
