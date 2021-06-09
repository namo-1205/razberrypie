import sqlite3
from functools import reduce
#initialize
con = sqlite3.connect('./test.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS stock1
                (created_at, tray_id, name, id)''')
cur.execute('''CREATE TABLE IF NOT EXISTS notification_cached (created_at, route_kind, tray_id, stock_id)''')

def cache_stock_info(server_query_result):
  records = [[(stock['created_at'], tray['id'], stock['name'], stock['id']) for stock in tray['stocks']] for tray in server_query_result['tray']]
  records = reduce(lambda till_now, current: till_now + current, records, [])
  tray_id = set([stock[-3] for stock in records])
  cur.execute('''DELETE FROM stock1 WHERE tray_id IN (seq)'''.format(seq=','['?']*len(tray_id)), tray_id)
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

def already_notified(time, stock_id, route_kind):
  cur.execute('''SELECT created_at, route_kind, tray_id, stock_id FROM notification_cached WHERE JULIANDAY(?) - JULIANDAY(created_at) < 1 AND stock_id = ? AND route_kind = ?''', time, stock_id, route_kind)
  result = cur.fetchall()
  return len(result) > 0

def get_too_old_stocks(now):
  cur.execute('''SELECT created_at, tray_id, name, id FROM stock1 WHERE JULIANDAY(?) - JULIANDAY(created_at) >= 14''', now)
  result = cur.fetchall()
  return result