import time

from coinpaprika import client as cp
import sqlite3


class CoinInfoCollector:

    def __init__(self, coin_id, base_dir):
        self.coin_id = coin_id
        self.client = cp.Client()
        self.connection = sqlite3.Connection(base_dir)
        self.candle_size_map = {
            "5m": 1,
            "15m": 3,
            "1d": 288,
            "7d": 24 * 7,
            "30d": 24 * 30,
            "1y": 24 * 65,
        }

        self.candle_sample_map = {
            "5m": 80,
            "15m": 56,
            "1d": 36,
            "7d": 15,
            "30d": 12,
            "1y": 12 * 3,
        }

    def add_table(self, table_name=None):
        if not table_name:
            table_name = self.coin_id.split("-")[0]
        self.connection.execute(f'''CREATE TABLE {table_name}
                                    (date real, price real)''')

    def insert_element(self, element, table_name=None):
        if not table_name:
            table_name = self.coin_id.split("-")[0]
        c = self.connection.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not c.fetchall():
            print("creating table")
            self.add_table()

        # print(f"INSERT INTO {table_name} VALUES ({element['date']}, {element['price']} )")
        self.connection.execute(
            f"INSERT INTO {table_name} VALUES ( {element['date']}, {element['price']} )")
        self.connection.commit()

    def get_tick(self):
        tick = self.client.ticker(self.coin_id)
        data = {
            "date": time.time(),
            "price": tick["quotes"]["USD"]["price"]

        }
        return data

    def get_avg_price_group_by_group(self, count, samples):
        total = []
        count_of_elements = self.connection.execute("SELECT COUNT(price) FROM dench ").fetchall()[0][0]
        for i in range(max(0, int(count_of_elements / count) - samples), int(count_of_elements / count) + 1):
            avg_price_for_group = self.connection.execute(
                f"select  AVG(date), MAX(price) from (select price, date from dench LIMIT {count}  offset {i * count} )").fetchone()
            if avg_price_for_group[0] and avg_price_for_group[1]:
                total = [avg_price_for_group] + total

        return total[::-1]

    def get_candle(self, candle_type):
        return self.get_avg_price_group_by_group(self.candle_size_map[candle_type],
                                                 int(self.candle_sample_map[candle_type]))

    def get_data_for_period(self, sampel_type):
        count_of_elements = self.connection.execute("SELECT COUNT(price) FROM dench ").fetchall()[0][0]
        avg_price_for_group = self.connection.execute(
            f"select date, price from dench  ORDER BY date DESC LIMIT {self.candle_sample_map[sampel_type]}  ").fetchall()
        # print(avg_price_for_group)
        return avg_price_for_group


if __name__ == '__main__':
    coin_control = CoinInfoCollector("dench-denchcoin", "./db.sqlite3")

    while True:

        try:
            coin_control.insert_element(coin_control.get_tick())
            time.sleep(300)
        except Exception as e:
            print(e)
            time.sleep(3)
