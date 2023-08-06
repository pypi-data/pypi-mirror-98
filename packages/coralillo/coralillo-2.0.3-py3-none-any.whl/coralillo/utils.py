import re


# from https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def snake_case(string):
    ''' Takes a string that represents for example a class name and returns
    the snake case version of it. It is used for model-to-key conversion '''
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)

    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camelCase(string):
    ''' Takes a string that represents the redis key version of a model name
    and returns its camel case version. It is used for key-to-model
    conversion. '''
    return ''.join(s[0].upper() + s[1:] for s in string.split('_'))


def parse_embed(embed_array):
    if not embed_array:
        return []

    fields = {}

    for item in embed_array:
        pieces = item.split('.', maxsplit=1)

        if pieces[0] not in fields:
            fields[pieces[0]] = None

        if len(pieces) == 2:
            if fields[pieces[0]] is None:
                fields[pieces[0]] = []

            fields[pieces[0]].append(pieces[1])

    return sorted(map(
        lambda item: list(item),
        fields.items()
    ), key=lambda x: x[0])
