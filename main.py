from argparse import ArgumentParser
from enum import Enum

from src.datagen import simulate_market
from src.streams import RedisStream, SocketStream, Stream


class StreamKinds(str, Enum):
    SOCKET = "socket"
    REDIS = "redis"


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("kind", choices=["socket", "redis"])
    argparser.add_argument("end", choices=["consumer", "producer"])
    argparser.add_argument("--size", type=int, default=1000)

    args = argparser.parse_args()

    simulated_market = simulate_market(args.size)

    s: Stream

    match args.kind:
        case StreamKinds.REDIS:
            s = RedisStream()
        case StreamKinds.SOCKET:
            s = SocketStream()
        case _:
            raise ValueError("Unknown stream kind")

    match args.end:
        case "consumer":
            s.consume()
        case "producer":
            s.produce(simulated_market)
