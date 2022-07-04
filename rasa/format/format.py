import json
import os
import re
import datetime
import uuid 
from rasa.format.annotator import annotate_example,add_regex_annotation

class nlu_format:
    def __init__(self) -> None:
        self.format = {
          "name":"defaultName101",
                            "pipeline": [
    {
      "name": "WhitespaceTokenizer"
    },
    {
      "name": "RegexFeaturizer"
    },
    {
      "name": "LexicalSyntacticFeaturizer"
    },
    {
      "name": "CountVectorsFeaturizer",
      "analyzer": "char_wb",
      "min_ngram": 1,
      "max_ngram": 4
    },
    {
      "name": "DIETClassifier",
      "epochs": 300,
      "constrain_similarities": True
    },
    {
      "name": "EntitySynonymMapper"
    },
    {
      "name": "ResponseSelector",
      "epochs": 300,
      "constrain_similarities": True
    },
    {
      "name": "FallbackClassifier",
      "threshold": 0.3,
      "ambiguity_threshold": 0.1
    }
  ],
  "policies": [
    {
      "name": "MemoizationPolicy"
    },
    {
      "name": "TEDPolicy",
      "max_history": 5,
      "epochs": 10
    },
    {
      "name": "RulePolicy"
    }
  ],
                            "intents": [],
                            "entities": [],
                            "slots": {},
                            "actions": [],
                            "forms": {},
                            "e2e_actions": [],
                            "responses": {},
                            "session_config": {
                                "session_expiration_time": 60
                            },
                            "nlu": [
                                {
                                    "intent": "greet",
                                    "examples": "- hey\n- hello\n"
                                },
                                {
                                    "intent": "goodbye",
                                    "examples": "- bye\n- goodbye\n"
                                }
                            ],
                            "rules": [],
                            "stories": [],
                            "lookup":[]
                      }
    def data(self):
        return self.format

    def get_name(self):
      return self.format['name']
    def save_nlu(self):
        with open(f'config.json', 'w') as fp:
            json.dump(self.format, fp)

    def load_nlu(self,filename):
        with open(f'config.json') as json_file:
            self.format = json.load(json_file)
    def purge_nlu(self):
      self.format['nlu']=[]
      self.format['intents']=[]
      self.format['entities']=[]

    def create_training_phrase(self,phrase):
      return {
              "parts": [
                {
                  "text": phrase,
                  "entityType": '',
                  "alias": '',
                  "userDefined": False
                }
              ],
              "name": uuid.uuid4(),
              "type": 'EXAMPLE',
              "timesAddedCount": 0
            }


    def create_intent(self,displayName,trainingPhrases=[]):
        if displayName in self.format['intents']:
          return {}
        self.format['intents'].append(displayName) 
        dic = {
            "type":"intent",
            "name":f"projects/{os.getenv('BOT_ID')}/agent/intents/"+str(uuid.uuid4()),
            "displayName":displayName,
            "trainingPhrases": [],
            "parameters":[]
        }
        self.format['nlu'].append(dic)
        return dic
    
    def update_intent(self,updated_intent):
      for i in range(len(self.format['nlu'])):
        if self.format['nlu'][i]['name']== updated_intent['name']:
          self.format['intents'] = [intent for intent in self.format['intents'] if intent!=self.format['nlu'][i]['displayName']]
          self.format['intents'].append(updated_intent['displayName'])

          self.format['nlu'][i]['displayName'] = updated_intent['displayName']
          for k in range(len(updated_intent['trainingPhrases'])):
            training_phrase = updated_intent['trainingPhrases'][k]
            training_phrase['name'] = str(uuid.uuid4())
            updated_intent['trainingPhrases'][k] = training_phrase 
          self.format['nlu'][i]['trainingPhrases'] = updated_intent['trainingPhrases']
          self.format['nlu'][i]['parameters'] = updated_intent['parameters']
          return self.format['nlu'][i]
      return None

    def get_intent(self,name):
      for i in self.format['nlu']:
        if 'name' in i.keys(): 
          if i['name']==name:
            return i  

    def get_examples(self,synonym):
      arr = []
      for i in self.format['nlu']:
        if i['displayName']==synonym:
          return i
          for j in i['entities']:
            for k in j['synonyms']:
              arr.append(k)
      return arr

    def annotate(self,example, type="synonym"):
      if type == "synonym":
        for entity in self.format['entities']:
          if self.get_examples(entity):
            i = self.get_examples(entity)
            for j in i['entities']:
              for k in sorted(j['synonyms'],key=len,reverse=True):
                if k in example.split() or ( k in example and len(k.split())>1 )and( len(re.findall(r'\[.*\]\{.*\}', example))==0) :
                  example = annotate_example(example, k , entity, j['value'])
                  return example
        return example

      if type == "regex":
        regex_list = []
        for r in self.format['nlu']:
          if "kind" in r.keys():
            if r['kind']=='KIND_REGEXP':
              regex_list.append(r["displayName"])

        
        for reg in regex_list:
          regex_example_list = self.get_examples(reg)
          for reg_type in regex_example_list['entities']:
            for reg_code in reg_type['synonyms']:
              regex_search = re.search(reg_code, example)
      
              if regex_search is not None:
                return add_regex_annotation(example,regex_search.group(), reg)
        return example
    
    def get_entities(self):
      res = [nlu_item for nlu_item in self.format['nlu'] if nlu_item['type']=='entity']
      return res 
         
    def create_regex(self,regex_intent,examples=None):
      for i in range(len(self.format['nlu'])):
          if 'regex' in  self.format['nlu'][i].keys():
              if self.format['nlu'][i]['regex']== regex_intent:
                  for example in examples:
                          self.format['nlu'][i]['examples'].append(example)
                          self.format['nlu'][i]['examples'] = list(set(self.format['nlu'][i]['examples']))
                  return self.format['nlu'][i]

      
      dic = {
          "uuid":str(uuid.uuid4()),
          "regex":regex_intent,
          "examples": examples
      }
      self.format['entities'].append(regex_intent)
      self.format['nlu'].append(dic)
      return dic

    
    def list_regex_example(self, regex_entity):
      for r in self.format["nlu"]:
        if "regex" in r.keys():
          examples = r["examples"]
          return examples

    def add_synonyms(self,synonym_name,synonyms):
        if synonym_name in self.format["entities"]:
            for i in range(len(self.format['nlu'])):
                if 'synonym' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['synonym']== synonym_name:
                      for example in synonyms:
                          self.format['nlu'][i]['examples'].append(example)
                          self.format['nlu'][i]['examples'] = list(set(self.format['nlu'][i]['examples']))
                          return self.format['nlu'][i]
        self.format['entities'].append(synonym_name) 
        dic = {
            "uuid":str(uuid.uuid4()),
            "synonym":synonym_name,
            "examples": synonyms
        }
        self.format['nlu'].append(dic)
        return dic

    def add_entity(self,entity):
        if entity in self.format["entities"]:
          return {} 
        self.format["entities"].append(entity['displayName'])
        dic = {
            "type":"entity",
            "name":f"projects/{os.getenv('BOT_ID')}/agent/entityTypes/"+str(uuid.uuid4()),
            "entities": [],
            "displayName": entity['displayName'],
            "kind": entity['kind']
        }
        self.format['nlu'].append(dic)
        return dic

    def update_entity(self,updated_entity):
      for i in range(len(self.format['nlu'])):
        if self.format['nlu'][i]['name']== updated_entity['name']:
          self.format['entities'] = [entity for entity in self.format['entities'] if entity!=self.format['nlu'][i]['displayName']]
          self.format['entities'].append(updated_entity['displayName'])
          self.format['nlu'][i]['displayName'] = updated_entity['displayName']
          for k in range(len(updated_entity['entities'])):
            updated_entity['entities'][k] = updated_entity['entities'][k] 
          self.format['nlu'][i]['entities'] = updated_entity['entities']
          return self.format['nlu'][i]
      return None


    def delete_intent(self,name):
      for i in self.format['nlu']:
        if i['name']==name:
          self.format['intents'] = [intent for intent in self.format['intents'] if intent!=i['displayName']]
      self.format['nlu'] = [nlu_item for nlu_item in self.format['nlu'] if nlu_item['name']!=name]
      return {}
    
    def get_intent_by_name(self,name_of_intent):
      for i in self.format['nlu']:
        if i['type']=='intent':
          if i['displayName']==name_of_intent:
            return i
      return {}
    ## Legacy Code                 
    # def remove_entity_annotation(self,entity_name:str, example:str):
        
    # # expecting example as: how much do I have on my [credit card account]{"entity": "account", "value": "credit"}
  
    #     re_search = re.search(entity_name,example)
    #     if re_search  is not None:
    #         labled_text = re.findall(r"\[([a-zA-Z0-9 ._]*)\]",example)[0]
    #         to_remove = "[" + labled_text + "]"
    #         example = example.replace(to_remove, labled_text)
    #         example=re.sub("\{.*?\}","",example)

    #         return example

    # def remove_regex_annotation(self,regex_name:str, example:str):

    # # expecting example as how much do I have on my [credit card account](account_number)
    #     re_search = re.search(regex_name,example)
    #     if re_search  is not None:
    #         labled_text = re.findall(r"\[([a-zA-Z0-9 ._]*)\]",example)[0]
    #         to_remove = "[" + labled_text + "]"
    #         example = example.replace(to_remove, labled_text)
    #         example=re.sub("\(.*?\)","",example)

    #         return example
    def set_pipeline(self,pipeline):
      self.format['pipeline']=pipeline


    def delete_entity(self,name: str):
      #check in the domain first 
      for data in self.format["nlu"]:
        if data['name'] == name:
            self.format['entities'] = [entity for entity in self.format['entities'] if name!=data['name']]
      self.format['nlu'] = [nlu_item for nlu_item in self.format['nlu'] if nlu_item['name']!=name]
      return {}


    def create_training_data(self):
      training_data = {}
      training_data['version'] = "3.1"
      training_data['pipeline'] = self.format['pipeline']
      training_data['policies'] = self.format['policies']
      training_data['intents'] = self.format['intents']
      training_data['entities'] = self.format['entities']
      training_data['slots'] = self.format['slots']
      training_data['actions'] = self.format['actions']
      training_data['forms'] = self.format['forms']
      training_data['e2e_actions'] = self.format['e2e_actions']
      training_data['responses'] = self.format['responses']
      training_data['session_config'] = self.format['session_config']
      training_data['nlu'] = []
      for i in self.format['nlu']:
        nlu_item={}
        dic = {}
        if i['type']=="intent":
          nlu_item['intent'] = i['displayName']
          data ="- "
          for trainingPhrase in i['trainingPhrases']:
            example = self.annotate(trainingPhrase["parts"][0]["text"])
            example = self.annotate(example,type="regex")
            data = data + example +"\n- "
          data = data[:-3]
          nlu_item['examples'] = data
        else:
          if i['kind']=="KIND_MAP":
            nlu_item['synonym'] = i['displayName']
          else:
            nlu_item['regex'] = i['displayName']
          data = "- "
          for example in i['entities']:
            for j in example['synonyms']:
              data = data + j + "\n- "
          data = data[:-3]
          nlu_item['examples'] = data
        training_data['nlu'].append(nlu_item)
      return training_data

    def delete_regex(self,regex_name: str):    
      for data in self.format["nlu"]:
        if "intent" in data.keys():
          examples_list = self.get_examples(data["intent"],"intent")
          for example in range(len(examples_list)):
            if regex_name in examples_list[example]:
              examples_list[example] = self.remove_regex_annotation(regex_name, examples_list[example])
          data["examples"] = "- " + "\n- ".join([_example for _example in examples_list])
  
