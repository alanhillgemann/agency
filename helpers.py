from datetime import datetime
from schema import And, Const, Optional, Schema, SchemaError, Use


def validate_schema(data, type):
    '''Check data schema is valid'''
    if type == 'post-actor':
        schema = Schema({
            'name': And(Use(str), lambda s: 1 <= len(s) <= 120),
            'gender': And(Use(str), lambda s: 1 <= len(s) <= 120),
            'age': And(Use(int), lambda n: 1 <= n <= 99)
        })
    elif type == 'patch-actor':
        schema = Schema({
            Optional('name'): And(Use(str), lambda s: 1 <= len(s) <= 120),
            Optional('gender'): And(Use(str), lambda s: 1 <= len(s) <= 120),
            Optional('age'): And(Use(int), lambda n: 1 <= n <= 99)
        })
    elif type == 'post-movie':
        schema = Schema({
            'title': And(Use(str), lambda s: 1 <= len(s) <= 120),
            'release_date':
                And(Use(str), lambda d: datetime.strptime(
                    d, '%Y-%m-%dT%H:%M:%S.%fZ') > datetime.now())
        })
    elif type == 'patch-movie':
        schema = Schema({
            Optional('title'): And(Use(str), lambda s: 1 <= len(s) <= 120),
            Optional('release_date'):
                And(Use(str), lambda d: datetime.strptime(
                    d, '%Y-%m-%dT%H:%M:%S.%fZ') > datetime.now())
        })
    elif type == 'post-performance':
        schema = Schema({
            'actor_id': And(Use(int), lambda n: 1 <= n),
            'movie_id': And(Use(int), lambda n: 1 <= n)
        })
    try:
        schema.validate(data)
        return True
    except SchemaError:
        return False
