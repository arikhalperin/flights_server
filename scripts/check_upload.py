import json

import requests

payload = {"interaction_type":"text",
           "text": "cancel a flight"}
result = requests.request("POST", "http://localhost:5000/v1/upload",params=payload)
print(result.json())

payload= {"data":json.dumps(result.json()["data"]),
          "text": "moscow"}
result = requests.request("POST", "http://localhost:5000/v1/upload",params=payload)
print(result.json())

payload= {"data":json.dumps(result.json()["data"]),
          "text": "19.11.2020"}
result = requests.request("POST", "http://localhost:5000/v1/upload",params=payload)
print(result.json())

payload= {"data":json.dumps(result.json()["data"]),
          "text": "12"}
result = requests.request("POST", "http://localhost:5000/v1/upload",params=payload)
print(result.json())
