import paho.mqtt.client as mqtt
from json.decoder import JSONDecodeError

from .json import serialize_msg, deserialize_msg
from .tasks import add_task
from . import CLIENT_ID, MQTT_BROKER, MQTT_BROKER_PORT
from .data_manager import search_by_tags


def reply_to_server(msg: dict):
    client.publish('general/server', serialize_msg(msg))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("general/clients")
    client.subscribe(f"general/{CLIENT_ID}")


def on_message(client: mqtt.Client, userdata, msg):
    print('[CLIENT] Message received: ', msg.payload)
    try:
        msg_dict = deserialize_msg(msg.payload)
        command = msg_dict['command']

        if command == 'train':
            add_task(msg_dict)
        elif command == 'search':
            # Look for databases corresponding with tags
            databases = search_by_tags(msg_dict['tags'])
            if len(databases) != 0:
                # remove path from search to avoid privacy issues
                for d in databases:
                    d.pop('path', None)
                msg = {'success': True, 'databases': databases, 'count': len(databases)}
                reply_to_server(msg)

        else:
            raise NotImplementedError('Command not found')
    except JSONDecodeError:
        reply_to_server({'success': False, 'msg': "Not able to deserialize the message"})
    except NotImplementedError:
        reply_to_server({'success': False, 'msg': f"Command `{msg_dict['command']}` is not implemented"})
    except KeyError:
        reply_to_server({'success': False, 'msg': "'command' property was not found"})
    except TypeError:  # Message was not serializable
        reply_to_server('error')


client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_BROKER_PORT, 60)


def start_mqtt_service():
    client.loop_start()
