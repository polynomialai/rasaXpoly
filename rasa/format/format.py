import json
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
                            "stories": []
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
      self.format['entites']=[]

    def create_intent(self,intent,examples=None):
        if intent in self.format["intents"]:
            for i in range(len(self.format['nlu'])):
                if 'intent' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['intent']== intent:
                        for example in examples:
                          self.format['nlu'][i]['examples'].append(example)
                          self.format['nlu'][i]['examples'] = list(set(self.format['nlu'][i]['examples']))
                        return self.format["nlu"][i]
        
        self.format['intents'].append(intent) 
        dic = {
            "uuid":str(uuid.uuid4()),
            "intent":intent,
            "examples": [example for example in examples]
        }
        self.format['nlu'].append(dic)
        return dic

    def get_intent(self,uuid):
      for i in self.format['nlu']:
        if 'uuid' in i.keys(): 
          if i['uuid']==uuid:
            return i  

    def get_examples(self,value,_type):
      for i in self.format['nlu']:
        if _type in i.keys():
          if i[_type]==value:
            return i['examples']
       
    def annotate(self,example, type="synonym"):
      if type == "synonym":
        for entity in self.format['entities']:
          if self.get_examples(entity,"synonym"):
            for synonym in self.get_examples(entity,"synonym"):
              if synonym in example:
                example = annotate_example(example, synonym , entity, synonym)
        return example

      if type == "regex":
        regex_list = []
        for r in self.format['nlu']:
          if "regex" in r.keys():
            regex_list.append(r["regex"])

        
        for reg in regex_list:
          regex_example_list = self.list_regex_example(regex_entity=reg)
          for reg_code in regex_example_list:
            regex_search = re.search(reg_code, example)
            if regex_search is not None:
              return add_regex_annotation(example,regex_search.group(), reg)
        return example

    def list_intent(self):
        return self.format["nlu"]
    
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

    def add_entity(self,entities):
        self.format["entities"].append(entites)
        return {}

    def delete_intent(self,uuid):
      for i in self.format['nlu']:
        if i['uuid']==uuid:
          self.format['intents'] = [intent for intent in self.format['intents'] if intent!=i['intent']]
      self.format['nlu'] = [nlu_item for nlu_item in self.format['nlu'] if nlu_item['uuid']!=uuid]
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

    def delete_entity(self,uuid: str):
      #check in the domain first 
      for data in self.format["nlu"]:
        if data['uuid'] == uuid:
          if 'regex' in data.keys():
            self.format['entites'] = [entity for entity in self.format['entites'] if entity!=data['regex']]
          else:
            self.format['entites'] = [entity for entity in self.format['entites'] if entity!=data['synonym']]
          break    
      self.format['nlu'] = [nlu_item for nlu_item in self.format['nlu'] if nlu_item['uuid']!=uuid]
      return {}


    def create_training_data(self):
      training_data = {}
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
        if 'intent' in i.keys():
          nlu_item['intent'] = i['intent']
          data ="- "
          for example in i['examples']:
            example = self.annotate(example)
            example = self.annotate(example,type="regex")
            data = data + example +"\n- "
          data = data[:-3]
          nlu_item['examples'] = data
        else:
          if'synonym' in i.keys():
            nlu_item['synonym'] = i['synonym']
          else:
            nlu_item['regex'] = i['regex']
          data = "- "
          for example in i['examples']:
            data = data + example + "\n- "
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

      # self.format['nlu']['entites'] = [entity for entity in format['nlu']['entites'] if entity!=entity_name]  
