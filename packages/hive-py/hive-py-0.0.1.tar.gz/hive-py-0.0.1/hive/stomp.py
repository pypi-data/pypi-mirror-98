import time
import uuid

import stomp

from hive.core import HivePubSub, Hive

class Listener(stomp.ConnectionListener):

    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, topic, callback):
        subscriptions = self.subscriptions.get(topic, [])
        subscriptions.append(callback)
        self.subscriptions[topic] = subscriptions

    def on_message(self, headers, body):
        for cb in self.subscriptions[headers['destination']]:
            cb(body.encode("utf-8"))



class HiveStomp(HivePubSub):

    def __init__(self):
        self.client = stomp.Connection()
        self.listener = Listener()
        self.client.set_listener('', self.listener)
        self.client.connect(wait=True)

    def subscribe_raw(self, topic, callback):
        self.client.subscribe(destination=topic, id=str(uuid.uuid4()), ack='auto')
        self.listener.subscribe(topic, callback)

    def publish_raw(self, topic, message):
        self.client.send(destination=topic, body=message)

    def spin(self):
        while True:
            time.sleep(0.01)

    def __del__(self):
        self.client.disconnect()


if Hive.DEFAULT_PUBSUB == HivePubSub:
    Hive.DEFAULT_PUBSUB = HiveStomp
