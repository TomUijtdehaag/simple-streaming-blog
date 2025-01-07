import json
import socket
import time
from typing import Iterable, Protocol

import redis

from .datagen import MarketOrder


class Stream(Protocol):
    def consume(self):
        pass

    def produce(
        self, data: Iterable[MarketOrder], interval: float = 0.1, *args, **kwargs
    ):
        pass


class SocketStream(Stream):
    def __init__(self, host: str = "127.0.0.1", port: int = 50000):
        self.host = host
        self.port = port

    def consume(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print("Consumer: connected to producer")
            while True:
                data = s.recv(1024)
                if not data:
                    break
                for line in data.decode("utf-8").splitlines():
                    order = MarketOrder(**json.loads(line))
                    print(f"Consumed: {order}")

    def produce(self, data: Iterable[MarketOrder], interval: float = 0.1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            print("Producer: waiting for a connection...")
            conn, addr = s.accept()
            with conn:
                print(f"Producer: connected to {addr}")
                for record in data:
                    record_serialized = json.dumps(record.serialize())
                    conn.sendall(record_serialized.encode("utf-8") + b"\n")
                    print(f"Produced: {record}")
                    time.sleep(interval)


class RedisStream(Stream):
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.r = redis.Redis(host=host, port=port, db=0)

    def consume(self, stream_key: str = "mystream"):
        last_id = "$"

        while True:
            # Block for new messages up to 5000 milliseconds (5 seconds)
            messages = self.r.xread({stream_key: last_id}, block=5000, count=1)
            if messages:
                # messages = [(stream_name, [(message_id, {field: value, ...})])]
                for stream, msgs in messages:
                    for msg_id, msg_data in msgs:
                        deserialized_order = {
                            k.decode(): v.decode() for k, v in msg_data.items()
                        }
                        order = MarketOrder(**deserialized_order)
                        print(f"Consumed: {order}")
                        last_id = msg_id
            else:
                print("No new messages; waiting...")
                time.sleep(1)

    def produce(
        self,
        data: Iterable[MarketOrder],
        interval: float = 0.1,
        stream_key: str = "mystream",
    ):
        for record in data:
            self.r.xadd(stream_key, record.serialize())
            print(f"Produced: {record}")
            time.sleep(interval)
