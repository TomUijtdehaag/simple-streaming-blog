import redis

from src.datagen import simulate_market

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, db=0)

# Generate and send market orders
for order in simulate_market(10000):
    r.xadd("orders", order)
