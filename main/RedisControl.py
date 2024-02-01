import redis
from .CoinInfoCollector import CoinInfoCollector


class RedisControl:
    @staticmethod
    def get_string(value) -> str:
        return value.decode('utf-8')

    def __init__(self, host='localhost', port=6379, db=0, sql_db="../db.sqlite3"):
        self.coin_control = CoinInfoCollector("dench-denchcoin", sql_db)
        self.host = host
        self.port = port
        self.db = db
        self.list_names = ["5m","15m", "1d", "7d", "30d", "1y"]
        # self.list_names = ["min", "hour", "day", "week", "month", "year"]
        self.redis_db = redis.Redis(host=host, port=port, db=db)
        # self.redis_db.flushdb()

    def set_list(self, list_name, element) -> None:
        self.redis_db.rpush(list_name, element)

    def get_list(self, list_name, start=0, end=-1):
        return self.redis_db.lrange(list_name, start=start, end=end)

    def add_to_set(self, set_name, element) -> None:
        self.redis_db.sadd(set_name, element)

    def get_set_members(self, set_name) -> map:
        return map(self.get_string, self.redis_db.smembers(set_name))

    def is_element_in_set(self, set_name, element) -> bool:
        return self.redis_db.sismember(set_name, element)

    def set_hash(self, hash_name, key, value) -> None:
        self.redis_db.hset(hash_name, key=key, value=value)

    def set_hash_map(self, hash_name, hash_map) -> None:
        self.redis_db.hmset(hash_name, mapping=hash_map)

    def get_hash_map(self, hash_name):
        return self.redis_db.hgetall(hash_name)

    def update_ticker(self):
        for list_name in self.list_names:
            self.redis_db.delete(list_name)
            for date_tick_pack in self.coin_control.get_candle(list_name):
                self.set_list(list_name + "_date", int(date_tick_pack[0]))
                self.set_list(list_name, date_tick_pack[1])

    def get_ticker(self, candle_type):
        info = self.get_list(candle_type)
        info_date = self.get_list(candle_type + "_date")
        if not info:
            self.update_ticker()
            info = self.get_list(candle_type)
            info_date = self.get_list(candle_type + "_date")
        # print(candle_type)
        # print(info, info_date)
        return info, info_date


if __name__ == "__main__":
    control = RedisControl(host="localhost")
    control.update_ticker()
    # for name in control.list_names:
    #     print(control.get_ticker(name))
