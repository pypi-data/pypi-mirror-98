import pprint as pp
import json


def prettify_output(text):
    try:
        pp.pprint(json.loads(text.encode('utf8')))
    except:
        print(text)