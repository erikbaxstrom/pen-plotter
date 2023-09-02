import ujson
# import re

with open('configuration.json', 'r') as file:
    jsonString = file.readlines()
    # json_string = re.sub(r'(?<!^)(?=[A-Z])', '_', jsonString).lower()
    print(jsonString)