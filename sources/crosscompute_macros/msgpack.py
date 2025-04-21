import msgpack

from .sqlalchemy import EncryptedBinary


class EncryptedMap(EncryptedBinary):

    def process_bind_param(self, value, dialect):
        if not value:
            return
        payload = msgpack.packb(value)
        return super().process_bind_param(payload, dialect)

    def process_result_value(self, value, dialect):
        if not value:
            return {}
        payload = super().process_result_value(value, dialect)
        return msgpack.unpackb(payload)
