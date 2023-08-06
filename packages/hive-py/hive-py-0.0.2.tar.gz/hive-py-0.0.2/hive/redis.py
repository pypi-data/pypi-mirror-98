from hive.core import HivePubSub, Hive
import redis


class HiveRedis(HivePubSub):

    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)
        self.sub = self.client.pubsub()
        self.subscriptions = {}

    def subscribe_raw(self, topic, callback):
        self.sub.subscribe(topic)
        subscriptions = self.subscriptions.get(topic, [])
        subscriptions.append(callback)
        self.subscriptions[topic] = subscriptions

    def publish_raw(self, topic, message):
        self.client.publish(topic, message)

    def spin(self):
        while True:
            msg = self.sub.get_message()
            if msg and msg["type"] == "message":
                for cb in self.subscriptions[msg["channel"].decode("utf-8")]:
                    cb(msg["data"])  # adjusting for hive working in bytes


if Hive.DEFAULT_PUBSUB == HivePubSub:
    Hive.DEFAULT_PUBSUB = HiveRedis
