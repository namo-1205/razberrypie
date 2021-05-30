import sqlite3
from functools import reduce
#initialize
con = sqlite3.connect('./test.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS stock1
                (created_at, tray_id, name, id)''')

def cache_stock_info(server_query_result):
  records = [[(stock['created_at'], tray['id'], stock['name'], stock['id']) for stock in tray['stocks']] for tray in server_query_result['tray']] #이중 배열 구성요소를 tuple로 전환
  records = reduce(lambda till_now, current: till_now + current, records, []) #이중 배열을 spread
  cur.execute('''INSERT INTO stock1 (created_at, tray_id, name, id) VALUES (?, ?, ?, ?)''', records)
  cur.commit()

def get_stocks_cached():
  cur.execute('''SELECT * FROM stock1''')
  result = cur.fetchall()
  return result