import ujson


class Configuration():

    def __init__(self, filename):
        raw_config = self.fetch_configuration(filename)
        self.configuration = self.parse_configuration(raw_config)


    def fetch_configuration(self, filename):
        with open(filename, 'r') as file:
            jsonString = file.read()
            raw_config = ujson.loads(jsonString)
            return raw_config


    def parse_configuration(self, raw_config):
        configuration = {}
        for header, section in raw_config.items():
            for key, value in section.items():
                configuration[key] = value
        return configuration

FILENAME = 'configuration.json'

configuration = Configuration(FILENAME)

print(configuration.configuration['name1.1'])