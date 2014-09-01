import json
import yaml


class BaseParser(object):
    loader = None
    dumper = None
    verbose_name = None

    @classmethod
    def parse(cls, stream, media_type=None, encoding='utf-8'):

        try:
            data = stream.read().decode(encoding)
            return cls.loader(data)
        except ValueError as exc:
            raise ValueError('{} parse error - {}'.format(cls.verbose_name, exc))

    @classmethod
    def render(cls, data, encoding='utf8'):
        return bytearray(cls.dumper(data), encoding=encoding)


class JSONParser(BaseParser):
    """
    JSON-serialized data.
    """

    media_type = 'application/json'
    loader = json.loads
    dumper = json.dumps
    verbose_name = 'JSON'


class YAMLParser(BaseParser):

    media_type = 'application/yaml'
    loader = yaml.safe_load
    dumper = yaml.dump
    verbose_name = 'YAML'

