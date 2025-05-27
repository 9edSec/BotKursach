from pydantic import BaseModel, ValidationError

tuple_valid: tuple = ('student', 'teacher')

def validator_one_of_tuple(value: str) -> str:
    if value not in tuple_valid:
        raise ValueError(f'mast be one of {[i for i in tuple_valid]}')
    return value
