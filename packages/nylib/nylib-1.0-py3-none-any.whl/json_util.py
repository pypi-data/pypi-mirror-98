import json
# import file_util
import sys, os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# print(sys.path)

from pylib import file_util


def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
        # if it's anything else, return it in its original form
    return data


# json格式化
def format_json(json_str):
    return format_obj(json.loads(json_str))


def format_obj(json_obj):
    return json.dumps(json_obj, indent=4, sort_keys=False, ensure_ascii=False)


def compress_json_file(file):
    content = file_util.read_content(file)
    jsn = json.loads(content)
    jstring = json.dumps(jsn)
    jstring = jstring.replace("\"", "\\\"")
    return jstring


def read_json_file(file):
    if os.path.exists(file):
        str = file_util.read_content(file)
        return json.loads(str)
    return {}


if __name__ == '__main__':
    import fire

    fire.Fire()
