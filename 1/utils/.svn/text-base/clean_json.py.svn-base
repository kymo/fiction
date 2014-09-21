#encoding:utf-8
import string
def clean(json_str):
    unallowed_word = ['>', '<', '\'', '\"']
    new_json_str = ""
    for char in json_str:
        new_json_str += char if char not in unallowed_word else ''
    return new_json_str
