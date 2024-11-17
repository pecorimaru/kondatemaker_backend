from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

def to_camel_case(string):
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

def convert_dict_to_camel_case(d):
    if isinstance(d, list):
        return [convert_dict_to_camel_case(i) if isinstance(i, (dict, list)) else i for i in d]
    return {to_camel_case(k): convert_dict_to_camel_case(v) if isinstance(v, (dict, list)) else v for k, v in d.items()}