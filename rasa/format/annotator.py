def annotate_example(example : str, token : str,  entity : str, synonym: str) -> str:
    annotation_add = f'"entity": "{entity}", "value": "{synonym}"'
    print("Token in ",token,"\n")
    example = example.replace(token, f"[{token}]" )+ "{"+ f"{annotation_add}" + "}"
    print(example)
    return example

def add_regex_annotation(example : str, token : str, regex_entity : str) -> str:    

    example = example.replace(token, f"[{token}]" )+ f"({regex_entity})"
    
   
    return example
