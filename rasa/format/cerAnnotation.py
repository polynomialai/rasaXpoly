import requests

example = "My work mail is deepak.g@polynmial.ai"

url = 'https://entity-extract.herokuapp.com/hybrid'
myobj ={
    "query": f"{example}",
    "agent_name": "transo",           #no packname need to be mentioned we are loading all packs by default
    "pack_name": "",   
    "threshold": 80
}

x = requests.post(url, json= myobj )
req = x.json()
tokens = {}

for i in req["entities"]:
    #print(i['entityClass'] ,'\t',i['token'])
    tokens[i['entityClass']] = i['token']
print(tokens)
def annotateNewExample(example,tokens):
    for token,value in tokens.items():
        example = example.replace(value, f"[{value}]" + "("+ f"{token}" + ")")
    return example
newExample = annotateNewExample(example,tokens)