import random
from datetime import datetime
from random import randrange
from math import sin, cos

time_delta = 5 * 60
date = 1625558400
date_2020_08_01 = 1582800593
price = 0.001
to_price = 0.33
coefficient = to_price - price
print(coefficient)
start_month = 8
with open("data_base1.csv", 'w') as CSV_WRITE:
    for i in range(date_2020_08_01, date, time_delta):
        if datetime.fromtimestamp(i).month == start_month + 1:
            start_month += 1
            if start_month == 12:
                start_month = 1
            price = coefficient * (i - date_2020_08_01) / (date - date_2020_08_01)
            print(datetime.fromtimestamp(i).date(), datetime.fromtimestamp(i).month)
        final_price = price + random.random() * sin(i) * cos(2 * i) * price * 0.2 - 1 * random.randint(0, 1) * random.random() * sin(3 * i) * cos(4 * i) * price * 0.25
        print(final_price)
        CSV_WRITE.write(f"{i},{final_price}\n")
