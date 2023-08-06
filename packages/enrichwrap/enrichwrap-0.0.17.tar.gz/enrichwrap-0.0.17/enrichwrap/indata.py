import json
import os


def get_default_data():
    sampleloc = os.path.dirname(__file__) + '/samples'
    with open(sampleloc + '/sample_input.json') as json_user_data_file:
        return json.load(json_user_data_file)


def get_data(val=None):
    if val is not None:
        return json.load(val)
    return get_default_data()
