import datetime
import sqlite3


class TableManager:

    def __init__(self, table_id, base_dir):
        self.table_id = table_id
        self.connection = sqlite3.Connection(base_dir)
        self.add_table_for_pair()

    def _check_table_exists(self, table_name):
        c = self.connection.execute(
            f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ''')
        if c.fetchone()[0] != 1:
            raise Exception("no table")

    def add_table_for_transaction(self, table_name=None):
        if not table_name:
            table_name = self.table_id
        self.connection.execute(
            f'''CREATE TABLE {table_name} (tx_hash text, 
                                           from_address text, 
                                           to_address text, 
                                           amount real , 
                                           coin text, 
                                           [timestamp] timestamp)''')

    def insert_element_for_transaction(self, element, table_name=None):
        if not table_name:
            table_name = self.table_id
        c = self.connection.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}' ")
        if not c.fetchall():
            print("creating table")
            self.add_table_for_transaction()

        # print(f"INSERT INTO {table_name} VALUES ({element['date']}, {element['price']} )")
        self.connection.execute(
            f"""INSERT INTO {table_name} (tx_hash, from_address, to_address, amount, coin, timestamp ) 
            VALUES (?,?,?,?,?,?)""",
            (element['tx_hash'][2:], element['from'][2:], element['to'][2:], element['amount'], element['coin'],
             datetime.datetime.now()))
        self.connection.commit()

    def exists_for_transaction(self, element, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"SELECT count(*) FROM {table_name} WHERE tx_hash = ?", (element['tx_hash'][2:],))
        data = c.fetchone()[0]
        print("data ", data)
        return data >= 1

    def add_table_for_pair(self, table_name=None):
        if not table_name:
            table_name = self.table_id
        c = self.connection.execute(
            f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ''')
        if c.fetchone()[0] != 1:
            self.connection.execute("""CREATE TABLE %s (tx_hash_base text,
                                tx_hash_quote text,
                                passcode text,
                                from_address text, 
                                to_address text, 
                                coin_base text, 
                                coin_quote text,
                                APR real,
                                amount_base real , 
                                amount_quote real , 
                                amount_USDD real , 
                                chain_type text , 
                                [timestamp] timestamp)""" % table_name)

    def insert_element_for_pair(self, tx_pair, apr, passcode, TokenLP_amount,chain_type, table_name=None):
        if not table_name:
            table_name = self.table_id
        c = self.connection.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not c.fetchall():
            print("creating table")
            self.add_table_for_pair()

        # print(f"INSERT INTO {table_name} VALUES ({element['date']}, {element['price']} )")
        self.connection.execute(
            f"""INSERT INTO {table_name} (tx_hash_base,
                                          tx_hash_quote, 
                                          passcode,
                                          from_address, 
                                          to_address, 
                                          coin_base, 
                                          coin_quote,
                                          APR,
                                          amount_base , 
                                          amount_quote ,
                                          amount_USDD ,
                                          chain_type,
                                          timestamp
                                           ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (tx_pair[0]['tx_hash'][2:],
             tx_pair[1]['tx_hash'][2:],
             passcode,
             tx_pair[0]['from'][2:],
             tx_pair[0]['to'][2:],
             tx_pair[0]['coin'],
             tx_pair[1]['coin'],
             apr,
             tx_pair[0]['amount'],
             tx_pair[1]['amount'],
             TokenLP_amount,
             chain_type,
             datetime.datetime.now()))
        self.connection.commit()

    def exists_account(self, from_address, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"SELECT count(*) FROM {table_name} WHERE from_address = ?", (from_address[2:],))
        data = c.fetchone()[0]
        print("data ", data)
        return data >= 1

    def exists_for_pair(self, tx_pair, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"SELECT count(*) FROM {table_name} WHERE tx_hash_base = ? AND tx_hash_quote = ? ",
            (tx_pair[0]['tx_hash'][2:], tx_pair[1]['tx_hash'][2:]))
        data = c.fetchone()[0]
        print("data ", data)
        return data >= 1

    def contract_exists(self, transaction_info, called_params, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"""SELECT count(*) FROM {table_name} 
            WHERE  coin_base =? AND coin_quote =? AND APR =? AND amount_base =? 
            AND amount_quote =? AND amount_USDD =? AND from_address = ? AND passcode = ?""",
            (transaction_info[0],
             transaction_info[1],
             transaction_info[2],
             transaction_info[3],
             transaction_info[4],
             transaction_info[5],
             called_params['wallet_address'][2:],
             called_params['passcode']))
        data = c.fetchone()[0]
        print("data ", data)
        return data == 1

    def get_passcode(self, from_address, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"SELECT passcode FROM {table_name} WHERE from_address = ?", (from_address[2:],))
        passcode = c.fetchone()[0]
        print("passcode ", passcode)
        return passcode

    def get_pairs(self, wallet_address, passcode, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"""SELECT coin_base, coin_quote, APR, amount_base, amount_quote, amount_USDD, timestamp 
            FROM {table_name} WHERE from_address = ? and passcode = ?""", (wallet_address[2:], passcode))
        data = c.fetchall()
        print("data ", data)
        data = list(map(list, data))
        return ['coin_base', 'coin_quote', 'APR', 'amount_base', 'amount_quote', 'amount_USDD', 'timestamp'], data

    def get_pairs_full(self, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"""SELECT from_address, 
                       coin_base, 
                       coin_quote, 
                       APR, 
                       amount_base, 
                       amount_quote, 
                       amount_USDD, 
                       chain_type,
                       timestamp 
                FROM {table_name}""")

        data = list(map(list, c.fetchall()))
        labels = [
            'address',
            'coin_base',
            'coin_quote',
            'APR',
            'amount_base',
            'amount_quote',
            'amount_USDD',
            'chain_type',
            'timestamp'
        ]
        return labels, data

    def get_pairs_full_info_for_resign(self, wallet_address, passcode, index, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        c = self.connection.execute(
            f"""SELECT coin_base, coin_quote, APR, amount_base, amount_quote, amount_USDD
            FROM {table_name} WHERE from_address = ? and passcode = ?""", (wallet_address[2:], passcode))
        data = c.fetchall()
        print("data ", data[int(index)])
        return data[int(index)]

    def drop_contract(self, transaction_info, called_params, table_name=None):
        if not table_name:
            table_name = self.table_id
        self._check_table_exists(table_name)
        self.connection.execute(
            f"""DELETE FROM {table_name} 
            WHERE  coin_base =? AND coin_quote =? AND APR =? AND amount_base =? 
            AND amount_quote =? AND amount_USDD =? AND from_address = ? AND passcode = ?""",
            (transaction_info[0],
             transaction_info[1],
             transaction_info[2],
             transaction_info[3],
             transaction_info[4],
             transaction_info[5],
             called_params['wallet_address'][2:],
             called_params['passcode']))
        self.connection.commit()


if __name__ == '__main__':
    tm = TableManager('paired_transactions_final', "./db.sqlite3")
    tm.get_pairs(wallet_address='0x6dFad349cB62550eC276b265929555190735C2a4', passcode='PTX7C2VH4ypdYVqx34Ug')
