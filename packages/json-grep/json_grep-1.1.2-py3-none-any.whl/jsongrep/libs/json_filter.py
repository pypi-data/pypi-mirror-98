import collections
import json
import re


class JsonFilterException(Exception):
    pass


class JsonFilter:

    PARSED_KEY_CACHE = {}

    @classmethod
    def parse_key(cls, key: str)->tuple:
        if key in cls.PARSED_KEY_CACHE:
            return cls.PARSED_KEY_CACHE[key]

        rkey: str = None
        rvalue: str = None
        operator: str = None
        re_sign = re.search("([=~])", key)
        if re_sign:
            operator = re_sign.group()
        parsed_key: list = str(key).split(operator)
        rkey = parsed_key[0].strip()
        rvalue = parsed_key[1].strip() if len(parsed_key) > 1 else None
        cls.PARSED_KEY_CACHE[key] = (rkey, rvalue, operator)
        return rkey, rvalue, operator

    @classmethod
    def filter_keys_and_values(cls, line: str, keys: dict, is_value_operator_used: bool=False) -> dict:
        ret = {}
        is_value_matched = False
        try:
            json_data_tree = json.loads(line)
            json_data_flat = cls.flatten_dict(json_data_tree)
            if not isinstance(json_data_flat, dict):
                raise JsonFilterException("JSON data is not dict on line: {}".format(line))
            for ikey in keys:
                key, value, operator = cls.parse_key(ikey)
                if key in json_data_flat:
                    if not value:
                        ret[key] = json_data_flat[key]
                    elif operator == "=" and str(value) == str(json_data_flat[key]):
                        ret[key] = json_data_flat[key]
                        is_value_matched = True
                    elif operator == "~" and str(value) in str(json_data_flat[key]):
                        ret[key] = json_data_flat[key]
                        is_value_matched = True
                    else:
                        return None
        except Exception as ex:
            raise JsonFilterException("Error decoding JSON from line: {} caused by: {}".format(line, ex))
        if is_value_operator_used and not is_value_matched:
            return None
        return ret

    @classmethod
    def flatten_dict(cls, input_dict: dict, parent_key: str='')->dict:
        items = []
        for k, v in input_dict.items():
            new_key = "{}.{}".format(parent_key, k) if parent_key else "{}".format(k)
            if isinstance(v, collections.MutableMapping):
                items.extend(cls.flatten_dict(v, new_key).items())
            elif isinstance(v, collections.MutableSequence):
                new_v = dict(enumerate(v))
                items.extend(cls.flatten_dict(new_v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def format_result(data: dict, multiline_output: bool = False, values_only: bool = False) -> str:
        ret = ""
        for key, value in data.items():
            br_line = "\n" if multiline_output else " "
            if values_only:
                ret = "{}\33[33m{}\33[0m{}".format(ret, value, br_line)
            else:
                ret = "{}\"\33[32m{}\33[0m\": \"\33[36m{}\33[0m\"{}".format(ret, key, value, br_line)
        return "{}{}".format(ret, "\n")