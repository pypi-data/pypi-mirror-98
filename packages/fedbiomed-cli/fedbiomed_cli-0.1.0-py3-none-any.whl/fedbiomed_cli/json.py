import json
from typing import Union

from fedbiomed_cli import CLIENT_ID


def deserialize_msg(msg: Union[str, bytes]) -> dict:
    """
    Deserializes a JSON string or bytes message as a dictionary.
    :param msg: message in JSON format but encoded as string or bytes
    :return: parsed message as python dictionary.
    """
    import json
    return json.loads(msg)


def serialize_msg(msg: dict):
    """
    Serialize an object as a JSON message (applies for dict-like objects)
    :param msg: dict-like object containing the message to send.
    :return: JSON parsed message ready to transmit.
    """
    try:
        if isinstance(msg, str):
            raise ValueError('Message must be a JSON-like object (dict).')

        msg['client_id'] = CLIENT_ID
        return json.dumps(msg)
    except ValueError:  # Message was not serializable
        return json.dumps({'success': False, 'msg': 'Message was not serializable'})
