import sqlite3
from functools import reduce
#initialize
con = sqlite3.connect('./test.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS stock1
                (created_at, tray_id, name, id)''')

def cache_stock_info(server_query_result):
  records = [[(stock['created_at'], tray['id'], stock['name'], stock['id']) for stock in tray['stocks']] for tray in server_query_result['tray']]
  records = reduce(lambda till_now, current: till_now + current, records, [])
  cur.executemany('''INSERT INTO stock1 (created_at, tray_id, name, id) VALUES (?, ?, ?, ?)''', records)
  con.commit()

def get_stocks_cached():
  cur.execute('''SELECT * FROM stock1''')
  result = cur.fetchall()
  return result

def get_created_at_cached(now):
  cur.execute('''SELECT tray_id, id FROM stock1 WHERE JULIANDAY(%d) - JULIANDAY(created_at) >= 3''', now)
  result = cur.fetchall()
  return result