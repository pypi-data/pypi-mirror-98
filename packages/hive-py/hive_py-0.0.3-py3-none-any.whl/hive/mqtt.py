import paho.mqtt.client as mqtt
from hive.core import HivePubSub, Hive


class HiveMqtt(HivePubSub):

    def __init__(self,
                 host="localhost",
                 port=1883,
                 keepalive=60,
                 bind_address="",
                 bind_port=0,
                 clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                 properties=None,

                 client_id="",
                 clean_session=None,
                 userdata=None,
                 protocol=mqtt.MQTTv311,
                 transport="tcp"
                 ):
        self.client = mqtt.Client(client_id, clean_session, userdata, protocol, transport)
        self.client.connect(host, port, keepalive, bind_address, bind_port, clean_start, properties)
        self.client.on_message = self.on_message()  # we use this to close over self so we can access the subscription list
        self.subscriptions = {}

    def on_message(self):
        def client_on_message(client, userdata, message):
            for cb in self.subscriptions[message.topic]:
                cb(message.payload)

        return client_on_message

    def subscribe_raw(self, topic, callback):
        self.client.subscribe(topic)
        subscriptions = self.subscriptions.get(topic, [])
        subscriptions.append(callback)
        self.subscriptions[topic] = subscriptions

    def publish_raw(self, topic, message):
        self.client.publish(topic, message)

    def spin(self):
        self.client.loop_forever()


if Hive.DEFAULT_PUBSUB == HivePubSub:
    Hive.DEFAULT_PUBSUB = HiveMqtt
