import json
import datetime

class nlu_format:
    def __init__(self) -> None:
        self.format = {
                            "pipeline": [
                                    {
                                    "name": "SpacyNLP",
                                    "model": "en_core_web_sm",
                                    },
                                    {
                                    "name": "SpacyTokenizer",
                                    "intent_split_symbol": "_",
                                    "token_pattern": "None"
                                    },
                                    {
                                    "name": "RegexFeaturizer"
                                    },
                                    {
                                    "name": "CountVectorsFeaturizer",
                                    "analyzer": "char_wb",
                                    "min_ngram": 1,
                                    "max_ngram": 4
                                    },
                                    {
                                    "name": "SpacyFeaturizer",
                                    "pooling": "mean"
                                    },
                                    {
                                    "name": "LogisticRegressionClassifier",
                                    "max_iter": 500,
                                    "solver": "lbfgs",
                                    "tol": 0.0001,
                                    "random_state": 42
                                    },
                                    {
                                    "name": "CRFEntityExtractor",
                                    "features": [
                                        [
                                        "low",
                                        "title",
                                        "upper"
                                        ],
                                        [
                                        "bias",
                                        "low",
                                        "prefix5",
                                        "prefix2",
                                        "suffix5",
                                        "suffix3",
                                        "suffix2",
                                        "upper",
                                        "title",
                                        "digit",
                                        "pattern",
                                        "text_dense_features"
                                        ],
                                        [
                                        "low",
                                        "title",
                                        "upper"
                                        ]
                                    ],
                                    "max_iterations": 100,
                                    "L1_c": 0.1,
                                    "L2_c": 0.1,
                                    "featurizers": []
                                    },
                                    {
                                    "name": "EntitySynonymMapper"
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
        with open(f'../data/temp/{str(datetime.datetime.now())}.json', 'w') as fp:
            json.dump(self.format, fp)

    def load_nlu(self,filename):
        with open(f'../data/temp/{filename}.json') as json_file:
            self.format = json.load(json_file)

    def create_intent(self,intent,examples=None):
        for i in range(len(self.format["nlu"])):
            if self.format["nlu"][i]["intent"]==intent:
                self.format["nlu"][i]["examples"] = self.format["nlu"][i]["examples"] + "- ".join([example+"\n" for example in examples])
                return
        self.format['intents'].append(intent) 
        dic = {
            "intent":intent,
            "examples": "- "+"- ".join([example+"\n" for example in examples])
        }
        self.format['nlu'].append(dic)

    def list_intent(self):
        return self.format["nlu"]
    
    def add_entity(self,entities):
        dic = {   
                "entities": "- ".join([entity+"\n" for entity in entities ])
        }
        self.format["domain"].push(dic)

    def del_entity(self,entity):
        for i in self.format["domain"]:
            if i["entities"] == "- "+ entity:
                self.format["domain"].remove(i) 