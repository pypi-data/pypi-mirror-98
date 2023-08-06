class ProtobufEncoder:
    def __call__(self, _, obj):
        return obj.SerializeToString()


class ProtobufDecoder:
    def __call__(self, cls, bytes):
        obj = cls()
        obj.ParseFromString(bytes)
        return obj