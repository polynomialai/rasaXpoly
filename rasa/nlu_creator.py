import json
import uuid
import os
format = {
    "name": os.getenv('BOT_ID'),
    "last_trained" : None,
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
      "threshold": 0.2,
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
                            "intents": ["agent.init"],
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
                                    "type": "intent",
                                    "name": f"projects/{os.getenv('BOT_ID')}/agent/intents/{str(uuid.uuid4())}",
                                    "displayName": "agent.init",
                                    "trainingPhrases": [
                                        {
                                            "type": "EXAMPLE",
                                            "parts": [
                                                {
                                                    "text": "init",
                                                    "alias": "",
                                                    "userDefined": false,
                                                    "entityType": ""
                                                }
                                            ],
                                            "name": str(uuid.uuid4())
                                        },
                                        {
                                            "type": "EXAMPLE",
                                            "parts": [
                                                {
                                                    "text": "intialise",
                                                    "alias": "",
                                                    "userDefined": false,
                                                    "entityType": ""
                                                }
                                            ],
                                            "name": str(uuid.uuid4())
                                        },
                                        {
                                            "type": "EXAMPLE",
                                            "parts": [
                                                {
                                                    "text": "initialised",
                                                    "alias": "",
                                                    "userDefined": false,
                                                    "entityType": ""
                                                }
                                            ],
                                            "name": str(uuid.uuid4())
                                        }
                                    ],
                                    "parameters":[]
                                }
                            ],
                            "rules": [],
                            "stories": []
      }

with open("basicBot/config.json", "w") as outfile:
    json.dump(format, outfile)


    