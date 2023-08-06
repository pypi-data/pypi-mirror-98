from hive.core import JsonDecoder, Hive, JsonEncoder


class ProtobufEncoder:
    def __call__(self, _, obj):
        return obj.SerializeToString()


class ProtobufDecoder:
    def __call__(self, cls, bytes):
        obj = cls()
        obj.ParseFromString(bytes)
        return obj


if Hive.DEFAULT_ENCODER == JsonEncoder:
    Hive.DEFAULT_ENCODER = ProtobufEncoder

if Hive.DEFAULT_DECODER == JsonDecoder:
    Hive.DEFAULT_DECODER = ProtobufDecoder
