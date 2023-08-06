import json
from io import StringIO


def dig(obj, *keys, default=None):
    current_value = None
    index = 0
    try:
        for key in keys:
            if type(key) is str and key.isdigit():
                key = int(key)
            if index == 0:
                current_value = obj[key]
            else:
                current_value = current_value[key]
            index += 1
        return current_value
    except KeyError:
        return default
    except IndexError:
        return default


def json_load(some, **kwargs):
    kwargs['encoding'] = 'utf-8'

    if type(some) is str:
        try:
            return json.loads(some, **kwargs)
        except ValueError as e:
            with open(some) as f:
                return json.load(f, **kwargs)
    else:
        return json.load(some, **kwargs)


def json_dump(obj, target=None, indent=2, ensure_ascii=False, **kwargs):
    kwargs['indent'] = indent
    kwargs['ensure_ascii'] = ensure_ascii

    if target is not None:
        if not isinstance(target, StringIO):
            with open(target, 'w') as f:
                json.dump(obj, f, **kwargs)
        else:
            json.dump(obj, target, **kwargs)

    json.dumps(obj, **kwargs)
