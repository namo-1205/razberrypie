from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://ec2-3-36-171-69.ap-northeast-2.compute.amazonaws.com:8080/v1/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

def last_stock(tray_id):
  query = gql('''query($trayId: Int!){
    stock(where: {tray_id: {_eq: $trayId}}, limit: 1, order_by: {id: desc}){
      name
      id
    }
  }''')
  result = client.execute(query, variable_values={
    'trayId': tray_id
  })
  return result['stock'][0] if len(result['stock']) > 0 else None

def new_stock_info(tray_id, name):
  query = gql("""mutation ($object: stock_insert_input!) {
      insert_stock_one(object: $object){
      tray_id
      name
    }
  }
  """)
  result = client.execute(query, variable_values = {
    "object": {
      "tray_id" : tray_id,
      "name": name
    }
  })
  return result['insert_stock_one']['tray_id']

def fetch_tray_info():
  query = gql('''query{
    tray{
      id
      name
      user_id
      order_priority
      stocks{
        created_at
        tray_id
        name
        id
      }
    }
  }''')
  return client.execute(query)

def insert_stock_with_sensor_info(stock_name, tray_id, sensor_data):
  mutation=gql("""mutation($stock: stock_insert_input!){
    insert_stock_one(object: $stock){
      id
    }
  }""")
  client.execute(mutation, variable_values={
    "object": {
      "tray_id": tray_id,
      "name": stock_name,
      "humidity_temperatures": {
        "data": {
          "humidity": sensor_data.humidity,
          "temperature": sensor_data.temperature
        }
      },
      "weights":{
        "data": {
          "value": sensor_data.weight
        }
      }
    }
  })
def insert_sensor_info(stock_id, sensor_data):
  mutation=gql("""mutation ($humdityTemperature: humidity_temperature_insert_input!, $weight: weight_insert_input) {
    insert_humidity_temperature_one(object: $humdityTemperature){
      stock_id
      humidity
      temperature
      created_at
    }
    insert_weight_one(object: $weight){
      stock_id
      created_at
      value
    }
  }""")
  client.execute(mutation, variable_values={
    "humdityTemperature": {
        "stock_id": stock_id,
        "humidity": sensor_data.humidity,
        "temperature": sensor_data.temperature
    },
    "weight": {
      "stock_id": stock_id,
      "value": sensor_data.weight
    }
  })