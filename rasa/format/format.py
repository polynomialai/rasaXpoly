import json
import datetime

from matplotlib.pyplot import annotate
from rasa.format.annotator import annotate_example, add_regex_annotation
import regex as re
class nlu_format:
    def __init__(self) -> None:
        self.format = {
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
      "epochs": 300
    },
    {
      "name": "RulePolicy"
    }
  ],
                            "policies": [],
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
                                },
                                {
                                    "regex": "account_number",
                                    "examples": "- \d{10,12}\n- \d{10,11}\n"
                                },          
                                {
                                    "intent": "inform",
                                    "examples": "- my account number is [1234567891](account_number)\n- This is my account number [1234567891](account_number)"
                                }        
                            ],
                            "rules": [],
                            "stories": []
                      }
    def data(self):
        return self.format

    def save_nlu(self):
        with open(f'../data/temp/{str(datetime.datetime.now())}.json', 'w') as fp:
            json.dump(self.format, fp)

    def load_nlu(self,filename):
        with open(f'../data/temp/{filename}.json') as json_file:
            self.format = json.load(json_file)

    def create_intent(self,intent,examples=None):
        if intent in self.format["intents"]:
            for i in range(len(self.format['nlu'])):
                if 'intent' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['intent']== intent:
                        self.format["nlu"][i]["examples"] = self.format["nlu"][i]["examples"] + "- ".join([self.annotate(example) +"\n" for example in examples])
                        return

        self.format['intents'].append(intent) 
        dic = {
            "intent":intent,
            "examples": "- "+"- ".join([self.annotate(example)+"\n" for example in examples])
        }
        self.format['nlu'].append(dic)

    def get_examples(self,value,_type):
      for i in self.format['nlu']:
        if _type in i.keys():
          if i[_type]==value:
            examples = i['examples']
            examples = "\n"+examples 
            examples = examples.split("\n-")
            examples = (" ".join(examples)).split()
            return examples

    def list_regex_example(self, regex_entity):
      for r in self.format["nlu"]:
        if "regex" in r.keys():
          examples = r["examples"]
          examples = "\n"+examples
          examples = examples.replace("\n-", ",")
          examples = ("".join(examples))

          examples = examples.split(",")
          ###  removing empty strings and \n in the examples
          examples.remove('')
          for _exp_idx in range(len(examples)):
              examples[_exp_idx] = examples[_exp_idx].replace('\n','')

          return examples

    def annotate(self,example, type="synonym"):
      if type == "entity":
        for entity in self.format['entities']:
          print("Entity is ",entity,"\n")
          for synonym in self.get_examples(entity,"synonym"):
            print("Synonym is ",synonym,"\n")
            if synonym in example:
              return annotate_example(example, synonym , entity, synonym)
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
              return add_regex_annotation(example,regex_search.group(), reg )
        return example
        
    def list_intent(self):
         return self.format["nlu"]
  
    def add_synonyms(self,synonym_name,synonyms):
        if synonym_name in self.format["entities"]:
            for i in range(len(self.format['nlu'])):
                if 'synonym' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['synonym']== synonym_name:
                        self.format["nlu"][i]["examples"] = self.format["nlu"][i]["examples"] + "- ".join([synonym+"\n" for synonym in synonyms])
                        return
        self.format['entities'].append(synonym_name) 
        dic = {
            "synonym":synonym_name,
            "examples": "- "+"- ".join([synonym+"\n" for synonym in synonyms])
        }
        self.format['nlu'].append(dic)
    
    def create_regex(self,regex_intent,examples=None):
        if regex_intent in self.format["regex"]:
            for i in range(len(self.format['nlu'])):
                if 'regex' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['regex']== regex_intent:
                        self.format["nlu"][i]["examples"] = self.format["nlu"][i]["examples"] + "- ".join([example +"\n" for example in examples])
                        return

        self.format['regex'].append(regex_intent) 
        dic = {
            "intent":regex_intent,
            "examples": "- "+"- ".join([example+"\n" for example in examples])
        }
        self.format['nlu'].append(dic)

    def add_entity(self,entities):
        dic = {   
                "entities": "- ".join([entity+"\n" for entity in entities ])
        }
        self.format["domain"].push(dic)

    def del_entity(self,entity):
        for i in self.format["domain"]:
            if i["entities"] == "- "+ entity:
                self.format["domain"].remove(i) 