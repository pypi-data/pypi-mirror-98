"""
    Module with classes to encapsulate abstract objects and helper methods over those objects
"""

# -- helper
import json
import re

PATTERN_DATE_FORMAT = re.compile(r'((?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2}))')


def get_obj_attr(object, item, missing_value=None, join_with=None, transform=None):
    """
    Returns the value of an object's attribute, checking if it exists. It can provide a predefined default value,
    in case it's an array can be joined with supplied char, and can be even transformed with supplied lambda function
    :param object: The object to look for the attribute
    :param item: The name of the field to retrieve
    :param missing_value: Default value in case it doesn't exists
    :param join_with: If the field value is an array, join the items with supplied char
    :param transform: Apply supplied transformation to the field, or to each member of the field if it's
    an array. The supplied function, must consider the type of data that the field value should contain, that is,
    we can not apply an upper() to an integer, for example.
    :return: The value of the field, or the default value if it doesn't exists and, optionally, transformed with
    supplied function or if it's an array, a single value with it's items joined
    """
    # traverse fields if several are provided joined by a dot
    fields = item.split('.')
    item = fields[-1]

    for _child in fields[:-1]:
        if hasattr(object, _child):
            object = getattr(object, _child)
        else:
            return missing_value

    if not hasattr(object, item):
        return missing_value

    value = getattr(object, item)

    if not isinstance(value, list):
        if transform:
            return transform(value)
        else:
            return value
    else:
        if transform and join_with:
            assert isinstance(join_with, str), f'{join_with} must be a string'
            return join_with.join([transform(x) for x in value])
        elif transform:
            return list(map(transform, value))
        elif join_with:
            return join_with.join(value)
        else:
            return value


# -- model classes to handle data easier

class DictionaryField:
    """
    Encapsulates any object field with nested elements
    """

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(value, dict):
                value = DictionaryField(**value)
            setattr(self, name, value)

    def serialize(self, *skip_fields, as_json=False):
        """
        Serialize current object as json
        :param skip_fields: A list of fieldnames separated by colon to be skipped from serialized output
        :param as_json: Serialize object as json representation
        :return: A valid serialized object as a dictionary
        """
        skip_fields = list(skip_fields) or []
        skip_fields.append('logger')

        serialized_dict = dict()
        for k, v in self.__dict__.items():
            if k in skip_fields:
                continue
            if isinstance(v, DictionaryField):
                serialized_dict[k] = v.serialize(*skip_fields)
            elif isinstance(v, list):
                list_dict = []
                for elem in v:
                    # if a list element is serializable, serialize it
                    if isinstance(elem, DictionaryField):
                        list_dict.append(elem.serialize(*skip_fields))
                    else:
                        list_dict.append(elem)
                serialized_dict[k] = list_dict
            else:
                serialized_dict[k] = v
        if as_json:
            return json.dumps(serialized_dict)
        return serialized_dict
