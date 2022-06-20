def annotate_example(example : str, token : str,  entity : str, synonym: str) -> str:
    annotation_add = f'"entity": "{entity}", "value": "{synonym}"'
    annotation_add = "{"+ f"{annotation_add}" + "}"
    example = example.replace(token, f"[{token}]{annotation_add}" )
    return example

def add_regex_annotation(example : str, token : str, regex_entity : str) -> str:    
    example = example.replace(token, f"[{token}]({regex_entity})")
    return example

