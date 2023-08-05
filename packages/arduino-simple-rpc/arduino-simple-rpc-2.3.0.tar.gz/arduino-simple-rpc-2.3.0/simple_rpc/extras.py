_method_template = '''
def {name}(self{args}):
    """{doc}"""
    return self.call_method('{name}'{args})
'''


def _make_docstring(method: dict) -> str:
    """Make a docstring for a function.

    :arg method: Method object.

    :returns: Function docstring.
    """
    help_text = ''

    if method['doc']:
        help_text += method['doc']

    if method['parameters']:
        help_text += '\n'

    for parameter in method['parameters']:
        help_text += '\n:arg {} {}:'.format(
            parameter['typename'], parameter['name'])
        if parameter['doc']:
            help_text += ' {}'.format(parameter['doc'])

    if method['return']['fmt']:
        help_text += '\n\n:returns {}:'.format(method['return']['typename'])
        if method['return']['doc']:
            help_text += ' {}'.format(method['return']['doc'])

    return help_text


def make_function(method: dict) -> callable:
    """Make a member function for a method.

    :arg method: Method object.

    :returns: New member function.
    """
    context = {}

    exec(
        _method_template.format(
            name=method['name'],
            doc=_make_docstring(method),
            args=''.join(
                map(lambda x: ', ' + x['name'], method['parameters']))),
        context)

    return context[method['name']]


def json_utf8_decode(obj: object) -> object:
    """Decode all strings in an object to UTF-8.

    :arg obj: Object.

    :returns: Object with UTF-8 encoded strings.
    """
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    if isinstance(obj, list) or isinstance(obj, tuple):
        return [json_utf8_decode(item) for item in obj]
    return obj


def json_utf8_encode(obj: object) -> object:
    """Binary encode all strings in an object.

    :arg obj: Object.

    :returns: Object with binary encoded strings.
    """
    if isinstance(obj, str):
        return obj.encode('utf-8')
    if isinstance(obj, list) or isinstance(obj, tuple):
        return [json_utf8_encode(item) for item in obj]
    return obj


def dict_to_object(d: dict) -> object:
    """Convert a dictionary using UTF-8 to an object using binary strings.

    :arg d: Dictionary with UTF-8 encoded strings.

    :returns: Object with binary encoded strings.
    """
    return json_utf8_encode(list(d.items()))


def object_to_dict(obj: object) -> dict:
    """Convert an object using binary strings to a dictionary using UTF-8.

    :arg obj: Object with binary encoded strings.

    :returns: Dictionary with UTF-8 encoded strings.
    """
    return dict(json_utf8_decode(obj))
