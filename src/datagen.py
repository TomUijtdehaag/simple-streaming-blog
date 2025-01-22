import random
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Generator


class Ticker(Enum):
    AAPL = "AAPL"
    MSFT = "MSFT"
    GOOGL = "GOOGL"
    AMZN = "AMZN"
    FB = "FB"
    TSLA = "TSLA"
    NVDA = "NVDA"
    NFLX = "NFLX"


@dataclass
class MarketOrder:
    ticker: str
    price: float
    volume: int

    def serialize(self) -> dict:
        return asdict(self)


def simulate_market(size: int = 100) -> Generator[dict, None, None]:
    market = {
        Ticker.AAPL: 100.0,
        Ticker.MSFT: 200.0,
        Ticker.GOOGL: 300.0,
        Ticker.AMZN: 400.0,
        Ticker.FB: 500.0,
        Ticker.TSLA: 600.0,
        Ticker.NVDA: 700.0,
        Ticker.NFLX: 800.0,
    }
    for _ in range(size):
        # pick a random ticker
        ticker = random.choice(list(Ticker))

        # simulate price change
        new_price = market[ticker] + random.gauss(0.01, market[ticker] * 0.01)
        market[ticker] = new_price

        # simulate volume
        volume = int(random.lognormvariate(0, 2) * 100)

        yield MarketOrder(
            ticker=ticker.value,
            price=new_price,
            volume=volume,
        ).serialize()


if __name__ == "__main__":
    for offer in simulate_market(10000):
        print(offer)
