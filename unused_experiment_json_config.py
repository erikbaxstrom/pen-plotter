import ujson
# import re

# with open('configuration.json', 'r') as file:
#     jsonString = file.read()
#     # json_string = re.sub(r'(?<!^)(?=[A-Z])', '_', jsonString).lower()
#     # print(type(jsonString))
#     parsed = ujson.loads(jsonString)
#     print(parsed)







# new code

def fetch_configuration(filename):
    with open(filename, 'r') as file:
        jsonString = file.read()
        raw_config = ujson.loads(jsonString)
        return raw_config



def parse_configuration(raw_config):

    configuration = {}
    print('raw_config', raw_config)
    for header, section in raw_config.items():
        print('this is header, section', header, section)
        for key, value in section:
            print('this is key,val', key, value)
            configuration[key] = value
    print(configuration)
    return configuration


raw_config = fetch_configuration('configuration.json')
# print('jsonstring', type(jsonString), jsonString[0:10])
configuration = parse_configuration(raw_config)