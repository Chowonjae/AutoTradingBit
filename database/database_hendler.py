import datetime
import pymysql
# import mainAlgorithm as mA


class MariaDBHandler:
    def __init__(self):
        self.host = '192.168.0.24'
        self.user = 'root'
        self.password = 'sun1030'
        self.db = 'CryptoCurrencyBase'
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
        self.cur = self.conn.cursor()

    def bid_side_insert(self, data):
        # 매수 SQL
        bid_sql = """
        INSERT INTO test_sample (
        order_time, market, side, price, volume, fee
        ) VALUES (
        %(order_time)s, %(market)s, %(side)s, %(price)s, %(volume)s, %(fee)s
        );
        """
        self.cur.execute(bid_sql, data)
        self.conn.commit()

    def ask_side_insert(self, data):
        # 매도 SQL
        ask_sql = """
        INSERT INTO test_sample (
        order_time, market, side, price, volume, fee, ratio
        ) VALUES (
        %s, %s, %s, %s, %s, %s, %s
        );
        """
        self.cur.execute(ask_sql, data)
        self.conn.commit()

    def ask_get_order(self):
        mA.mainTrading


if __name__ == '__main__':
    db = MariaDBHandler()
    now = datetime.datetime.now()
    order_time = datetime.datetime(now.year, now.month, now.day)
    insert_data = [order_time, 'BTC', '매수', '7630520.0', '26.0', '19.9', '2%']
    print(insert_data)
    # db.ask_side_insert(insert_data)




