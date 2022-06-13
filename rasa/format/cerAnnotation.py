import requests

example = "vechicles in madras within 50 m with gps status as stop for driver Rohn"

url = 'https://entity-extract.herokuapp.com/hybrid'
myobj ={
    "query": f"{example}",
    "agent_name": "transo",
    "pack_name": ""   #no packname need to be mentioned we are loading all packs by default
}

x = requests.post(url, json= myobj )
req = x.json()
tokens = {}
for i in req["entities"]:
    #print(i['entityClass'] ,'\t',i['token'])
    tokens[i['entityClass']] = i['token']

def annotateNewExample(example,tokens):
    for token,value in tokens.items():
        example = example.replace(value, f"[{value}]" + "{"+ f"{token}" + "}")
    return example
newExample = annotateNewExample(example,tokens)