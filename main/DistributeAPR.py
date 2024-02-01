from datetime import datetime, timedelta
from pprint import pprint

from main.DBTableManager import TableManager
from main.MetamaskManager import MetamaskManager


def main():
    tm = TableManager('paired_transactions_final', "./db.sqlite3")
    address = "0xa1e453b2c576acEEA6d406b7366536feB8A6DF55"
    private_key = "34dfb81837d00d9b5992d911caaeeda19a76015ef74ad88d018f7badbae1e3e4"
    metaMask = MetamaskManager(address, private_key)
    labels, active_pairs = tm.get_pairs_full()
    index_of_timestamp = labels.index('timestamp')
    if index_of_timestamp < 0:
        raise Exception('The timestamp is not returned as a db table column!')
    date_now = datetime.now()
    first = date_now.replace(day=1)
    one_month_back = first - timedelta(days=1)
    one_month_back = one_month_back.replace(day=1)
    two_month_back = one_month_back - timedelta(days=1)
    two_month_back = two_month_back.replace(day=1)
    for pair_info in active_pairs:
        start_time = datetime.fromisoformat(pair_info[index_of_timestamp])
        delta_time_from_start = date_now - start_time
        delta_time_from_one_month = date_now - one_month_back
        delta_time_from_two_month = date_now - two_month_back
        day_count = 0
        if delta_time_from_one_month < delta_time_from_start < delta_time_from_two_month:
            day_count = delta_time_from_start.days
        elif delta_time_from_two_month < delta_time_from_start:

            day_count = delta_time_from_one_month.days
        if day_count > 0:
            try:
                coin_count = float(pair_info[labels.index('amount_quote')])
                percent = float(pair_info[labels.index('APR')])
                reward = day_count * ((coin_count * percent) / 100) / 365
                to_address = pair_info[labels.index('from_address')]
                coin_name = pair_info[labels.index('coin_quote')]
                chain_type = pair_info[labels.index('chain_type')]
                coin_name = metaMask.get_coin_name_by_chain(coin_name, chain_type)
                print({'to_address': to_address, 'coin_name': coin_name, 'coin_amount': reward})
                result = metaMask.send_coin_to_address(to_address=to_address, coin_name=coin_name, coin_amount=reward)
                if 'Success' not in result[1]:
                    raise Exception('Transaction failed please use above stdout as a reference')
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
