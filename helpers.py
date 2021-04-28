from schema import And, Schema, SchemaError, Use

def validate_schema(data, type):
    '''Check data schema is valid'''
    if type is 'actor':
        schema = Schema({
            'name': And(Use(str), len),
            'gender': And(Use(str), len),
            'age': And(Use(int), lambda n: 1 <= n <= 99)
        })
    try:
        schema.validate(data)
        return True
    except SchemaError:
        return False