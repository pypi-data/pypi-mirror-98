import requests
import json

def byId(db_ip,index, _id, data):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(data)
    x = requests.put("http://"+db_ip+"/"+index+"/_doc/"+_id,headers=headers,data=data)
    return x.text