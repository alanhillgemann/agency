from datetime import datetime
from schema import And, Const, Optional, Schema, SchemaError, Use


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
    elif type == 'post-movie':
        schema = Schema({
            'title': And(Use(str), len),
            'release_date':
                And(Use(str), lambda d: datetime.strptime(
                    d, '%Y-%m-%dT%H:%M:%S.%fZ') > datetime.now())
        })
    elif type == 'patch-movie':
        schema = Schema({
            Optional('title'): And(Use(str), len),
            Optional('release_date'):
                And(Use(str), lambda d: datetime.strptime(
                    d, '%Y-%m-%dT%H:%M:%S.%fZ') > datetime.now())
        })
    try:
        schema.validate(data)
        return True
    except SchemaError:
        return False
