def annotate_example(example : str, token : str,  entity : str, synonym: str) -> str:
    annotation_add = f'"entity": "{entity}", "value": "{synonym}"'
    example = example.replace(token, f"[{token}]" )+ "{"+ f"{annotation_add}" + "}"
    return example

def add_regex_annotation(example : str, token : str, regex_entity : str) -> str:    
    example = example.replace(token, f"[{token}]" )+ f"({regex_entity})"

    return example

print(add_regex_annotation("I am a boy","boy","gender"))


import requests

example = "vechicles in madras within 50 m with gps status as stop for driver Rohn"

url = 'https://entity-extract.herokuapp.com/hybrid'
myobj ={
    "query": f"{example}",
    "agent_name": "transo",
    "pack_name": "location",
    "threshold":80
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