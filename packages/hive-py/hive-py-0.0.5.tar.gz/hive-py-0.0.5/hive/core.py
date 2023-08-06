import jsonpickle
import time


class HivePubSub:
    def subscribe_raw(self, topic, callback):
        """
        Subscribe to the bytes received on a topic

        :param topic: topic name
        :param callback: callback function to execute - cb(bytes)
        :return: None
        """
        pass

    def publish_raw(self, topic, message):
        """
        Publish raw bytes to a topic
        :param topic: topic to subscribe
        :param message: message bytes to publish
        :return:
        """
        pass

    def spin(self):
        '''
        Start the broker connection and take over the main thread
        :return:
        '''
        while True:
            time.sleep(0.01)


class Publisher:

    def __init__(
            self,
            pubsub,
            topic,
            cls,
            encoder
    ):
        self.pubsub = pubsub
        self.topic = topic
        self.cls = cls
        self.encoder = encoder

    def publish(self, obj):
        self.pubsub.publish_raw(self.topic, self.encoder(self.cls, obj))


class Subscriber:

    def __init__(
            self,
            pubsub,
            topic,
            cls,
            decoder,
            callback
    ):
        pubsub.subscribe_raw(
            topic,
            lambda obj: callback(decoder(cls, obj))
        )


def json_encoder(cls, obj):
    return jsonpickle.encode(obj, unpicklable=False).encode("utf-8")


def json_decoder(cls, msg_bytes):
    d = jsonpickle.decode(msg_bytes.decode("utf-8"))
    if type(d) == cls:
        return d

    msg_bytes = cls()
    for k, v in d.items():
        setattr(msg_bytes, k, v)
    return msg_bytes


class HiveWorker:

    pubsub_cls = HivePubSub
    encoder = json_encoder
    decoder = json_decoder

    def __init__(self, *args, **kwargs):
        self.pubsub = HiveWorker.pubsub_cls(*args, **kwargs)

    def spin(self):
        self.pubsub.spin()

    def publisher(self, topic, cls):
        return Publisher(self.pubsub, topic, cls, HiveWorker.encoder)

    def subscribe(self, topic, cls, callback):
        return Subscriber(self.pubsub, topic, cls, HiveWorker.decoder, callback)
