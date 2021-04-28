from schema import And, Optional, Schema, SchemaError, Use

def validate_schema(data, type):
    '''Check data schema is valid'''
    if type == 'post-actor':
        schema = Schema({
            'name': And(Use(str), len),
            'gender': And(Use(str), len),
            'age': And(Use(int), lambda n: 1 <= n <= 99)
        })
    elif type == 'patch-actor':
        schema = Schema({
            Optional('name'): And(Use(str), len),
            Optional('gender'): And(Use(str), len),
            Optional('age'): And(Use(int), lambda n: 1 <= n <= 99)
        })
    try:
        schema.validate(data)
        return True
    except SchemaError:
        return False