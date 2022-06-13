def annotate_example(example : str, token : str,  entity : str, synonym: str) -> str:
    annotation_add = f'"entity": "{entity}", "value": "{synonym}"'
    example = example.replace(token, f"[{token}]" )+ "{"+ f"{annotation_add}" + "}"
    return example

def add_regex_annotation(example : str, token : str, regex_entity : str) -> str:    
    example = example.replace(token, f"[{token}]" )+ f"({regex_entity})"

    return example

print(add_regex_annotation("I am a boy","boy","gender"))


