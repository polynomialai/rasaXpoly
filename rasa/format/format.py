import json
import datetime
from rasa.format.annotator import annotate_example
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
                                }
                            ],
                            "rules": [],
                            "stories": []
                      }
    def data(self):
        return self.format

    def save_nlu(self):
        with open(f'config.json', 'w') as fp:
            json.dump(self.format, fp)

    def load_nlu(self,filename):
        with open(f'config.json') as json_file:
            self.format = json.load(json_file)

    def create_intent(self,intent,examples=None):
        if intent in self.format["intents"]:
            for i in range(len(self.format['nlu'])):
                if 'intent' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['intent']== intent:
                        self.format["nlu"][i]["examples"] = self.format["nlu"][i]["examples"] + "- ".join([self.annotate(example) +"\n" for example in examples if self.annotate(example) not in self.format["nlu"][i]["examples"]])
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
            examples = examples.replace("\n-", ",")
            examples = ("".join(examples))

            examples = examples.split(",")
            ###  removing empty strings and \n in the examples
            examples.remove('')
            for _exp_idx in range(len(examples)):
                examples[_exp_idx] = examples[_exp_idx].replace('\n','').strip()
            return examples
       
    def annotate(self,example):
        for entity in self.format['entities']:
          for synonym in self.get_examples(entity,"synonym"):
            if synonym in example:
              return annotate_example(example, synonym , entity, synonym)
        return example
    def list_intent(self):
        return self.format["nlu"]
    
    def add_synonyms(self,synonym_name,synonyms):
        if synonym_name in self.format["entities"]:
            for i in range(len(self.format['nlu'])):
                if 'synonym' in  self.format['nlu'][i].keys():
                    if self.format['nlu'][i]['synonym']== synonym_name:
                        self.format["nlu"][i]["examples"] = self.format["nlu"][i]["examples"] + "- ".join([synonym+"\n" for synonym in synonyms if synonym not in self.format["nlu"][i]["examples"]])
                        return
        self.format['entities'].append(synonym_name) 
        dic = {
            "synonym":synonym_name,
            "examples": "- "+"- ".join([synonym+"\n" for synonym in synonyms])
        }
        self.format['nlu'].append(dic)

        # Annotate all the examples again 
        for i in range(len(self.format['nlu'])):
          if 'intent' in self.format['nlu'][i].keys():
            self.format['nlu'][i]['examples'] = '- '+"\n- ".join([self.annotate(example) for example in self.get_examples(self.format['nlu'][i]['intent'],"intent")])

    def add_entity(self,entities):
        dic = {   
                "entities": "- ".join([entity+"\n" for entity in entities ])
        }
        self.format["domain"].push(dic)

    def del_entity(self,entity):
        for i in self.format["domain"]:
            if i["entities"] == "- "+ entity:
                self.format["domain"].remove(i) 