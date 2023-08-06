SERIALIZERS = dict(json=True, yaml=True)

try:
    import json
except ImportError:
    SERIALIZERS['json'] = False

try:
    import yaml
except ImportError:
    SERIALIZERS['yaml'] = False


class BaseSerializer:
    """
    Base Serializer
    """

    content_types = None
    key = None

    def get_content_type(self):
        """."""
        if self.content_types is None:
            raise NotImplementedError()
        return self.content_types[0]

    def loads(self, data):
        raise NotImplementedError()

    def dumps(self, data):
        raise NotImplementedError()


class JsonSerializer(BaseSerializer):
    """
    JSON Serializer
    """

    content_types = [
        'application/json',
        'application/x-javascript',
        'text/javascript',
        'text/x-javascript',
        'text/x-json',
    ]
    key = 'json'

    def loads(self, data):
        return json.loads(data)

    def dumps(self, data):
        return json.dumps(data)


class YamlSerializer(BaseSerializer):
    """
    YAML Serializer
    """

    content_types = [
        'text/yaml',
        'text/x-yaml',
        'application/yaml',
        'application/x-yaml',
    ]
    key = 'yaml'

    def loads(self, data):
        return yaml.safe_load(str(data))

    def dumps(self, data):
        return yaml.dump(data)


class Serializer(object):
    """
    Automatically serialize content by content type
    """

    def __init__(self, default=None, serializers=None):
        if default is None:
            default = 'json' if SERIALIZERS['json'] else 'yaml'

        if serializers is None:
            serializers = [x() for x in [JsonSerializer, YamlSerializer] if SERIALIZERS[x.key]]

        self.serializers = {}

        for serializer in serializers:
            self.serializers[serializer.key] = serializer

        self.default = default

    def get_serializer(self, name=None, content_type=None):
        if name is None and content_type is None:
            return self.serializers[self.default]
        else:
            for x in self.serializers.values():
                for c_type in x.content_types:
                    if content_type == c_type:
                        return x
        raise Exception('Unknown serializer class')

    def loads(self, data, format=None):
        s = self.get_serializer(format)
        return s.loads(data)

    def dumps(self, data, format=None):
        s = self.get_serializer(format)
        return s.dumps(data)

    def get_content_type(self, format=None):
        s = self.get_serializer(format)
        return s.get_content_type()
