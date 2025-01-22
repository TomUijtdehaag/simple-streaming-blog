from argparse import ArgumentParser

from src.datagen import simulate_market
from src.streamers import RedisStreamer, SocketStreamer, Streamer, StreamerKinds

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("kind", choices=["socket", "redis"])
    argparser.add_argument("end", choices=["consumer", "producer"])
    argparser.add_argument("--size", type=int, default=1000)

    args = argparser.parse_args()

    simulated_market = simulate_market(args.size)
    s: Streamer

    match args.kind:
        case StreamerKinds.SOCKET:
            s = SocketStreamer()
        case StreamerKinds.REDIS:
            s = RedisStreamer()
        case _:
            raise ValueError(f"Unkown StreamerKind {args.kind}")

    try:
        match args.end:
            case "consumer":
                s.consume()
            case "producer":
                s.produce(simulated_market)

    except KeyboardInterrupt:
        print("Stopping", args.kind, args.end)
