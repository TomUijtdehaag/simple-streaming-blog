from pprint import pprint

import redis


def main():
    r = redis.Redis(host="localhost", port=6379, db=0)
    while True:
        res = r.xread({"orders": "$"}, count=1, block=0)

        if res:
            # Unpack the response
            [[stream, [(message_id, order)]]] = res
            order = {k.decode(): v.decode() for k, v in order.items()}
            pprint(order)


if __name__ == "__main__":
    main()
