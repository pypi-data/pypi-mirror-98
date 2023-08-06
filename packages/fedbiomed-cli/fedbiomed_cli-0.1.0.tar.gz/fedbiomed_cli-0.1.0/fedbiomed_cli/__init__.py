import os
import uuid


ROOT = os.path.dirname(os.path.abspath(__file__))
QUEUE_DIR = os.path.join(ROOT, f'queue_manager')
DB_DIR = os.path.join(ROOT, f'db.json')

MQTT_BROKER = os.getenv('MQTT_BROKER', 'epione-demo.inria.fr')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 80))

UPLOADS_URL = os.getenv('UPLOADS_URL', 'https://epione-demo.inria.fr/fedbiomed/upload/')
CLIENT_ID = os.getenv('CLIENT_ID', str(uuid.UUID(int=uuid.getnode())))
