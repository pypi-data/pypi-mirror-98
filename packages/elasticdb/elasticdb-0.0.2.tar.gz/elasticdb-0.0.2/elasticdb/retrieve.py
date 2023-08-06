import requests
import json

def wholeIndex(db_ip,index):
    x = requests.get("http:/"+db_ip+"/"+index+"/_search")
    response = json.loads(x.text)
    hits = response['hits']['hits']
    result = {}
    for y in hits:
        result[y["_id"]] = y["_source"]
    return result
    
def byId(db_ip,index,_id):
    x = requests.get("http:/"+db_ip+"/"+index+"/_source/"+_id)
    response = json.loads(x.text)
    return(response)
