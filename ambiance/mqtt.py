from ambiance import configuration
from ambiance.router import Router
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_1
from ambiance import algorithm
import json

config = configuration.MqttOptions
client = MQTTClient()
router = Router(client=client)
connected = False
devices = []


async def start_client():
    global connected

    try:
        await client.connect(uri=config.broker_url, cafile=config.ca_file)
        print("Connected to MQTT Broker @ " + config.broker_url)
        connected = True

        await client.subscribe([(t.topic, t.qos) for t in router.topics])
        while True:
            try:
                await router.push(await client.deliver_message())
            except Exception as e:
                print(e)
                raise
    except ConnectException:
        connected = False


@router.topic('system/join', QOS_1)
async def handle_join(message):
    packet = message.publish_packet
    try:
        data = json.loads(packet.payload.data.decode("utf-8"))
        if data['uuid'] not in devices:
            devices.append(data['uuid'])
        # print("Join: => %s" % (str(packet.payload.data)))
    except ValueError as e:
        error = json.dumps({"name": "JSONDecodeError", "reason": str(e)}).encode()
        await client.publish('ambiance/error', error, QOS_1)
    except KeyError as e:
        error = json.dumps({"name": "KeyError", "reason": str(e)}).encode()
        await client.publish('ambiance/error', error, QOS_1)


@router.topic('device/+/data', QOS_1)
async def handle_data(message, wc):
    packet = message.publish_packet
    if wc not in devices:
        devices.append(wc)
    try:
        data = json.loads(packet.payload.data.decode("utf-8"))
        await algorithm.record_change(data)
        # print("Device %s: => %s" % (wc, str(packet.payload.data)))
    except ValueError as e:
            error = json.dumps({"name": "JSONDecodeError", "reason": str(e)}).encode()
            await client.publish('ambiance/error', error, QOS_1)
    except KeyError as e:
            error = json.dumps({"name": "KeyError", "reason": str(e)}).encode()
            await client.publish('ambiance/error', error, QOS_1)
