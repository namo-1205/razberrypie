from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://ec2-3-36-171-69.ap-northeast-2.compute.amazonaws.com:8080/v1/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

def receive_tray_id(stock_name):
  query = gql('''query($stockName: String!){
    stock(where: {name: {_eq: $stockName}}, order_by: {id: desc}, limit: 1){
      created_at
      tray_id
      name
      id
    }
  }''')
  result = client.execute(query, variable_values={
    "stockName": stock_name
  })

  return result['stock'][0]['tray_id'] if len(result['stock']) > 0 else None

def new_stock_info(tray_id, name):
  query = gql("""mutation ($object: stock_insert_input!) {
      insert_stock_one(object: $object){
      tray_id
      name
    }
  }
  """)
  client.execute(query, variable_values = {
    "object": {
      "tray_id" : tray_id,
      "name": name
    }
  })

def new_tray(name):
  query = gql("""mutation ($object: tray_insert_input!) {
      insert_tray_one(object: $object){
      id
      stocks{
        id
      }
    }
  }""")
  client.execute(query, variable_values={
    "object": {
      "name": "your refridgerator",
      "order_priority": 1,
      "user_id": 1,
      "stocks": {
        "data": [
          {
              "name": name
          }
        ]
      }
    }
  })

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

def insert_sensor_info(stock_name, sensor_data):
  query = gql('''query($stockName: String!){
    stock(where: {name: {_eq: $stockName}}, order_by: {id: desc}, limit: 1){
      created_at
      tray_id
      name
      id
    }
  }''')
  result = client.execute(query, variable_values={
    "stockName": stock_name
  })
  is_stock_exist = len(result['stock']) > 0
  if is_stock_exist:
    stock_id = result['stock'][0]['id']
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
          "humidity": sensor_data.humadity,
          "temperature": sensor_data.temperature
      },
      "weight": {
        "stock_id": stock_id,
        "value": sensor_data.weight
      }
    })
  