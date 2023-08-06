from kal.helper import json_load, json_dump


class BaseJson:
    filepath = None
    default_data = {}
    data = None

    @classmethod
    def get_default_data(cls):
        return cls.default_data

    @classmethod
    def initialize(cls):
        if not cls.filepath.exists():
            json_dump(cls.get_default_data(), cls.filepath)
        with cls.filepath.open() as f:
            cls.data = json_load(f)

    @classmethod
    def get(cls, key, default=None):
        return cls.data.get(key, default)


class WritableJson(BaseJson):
    @classmethod
    def set(cls, key, value):
        cls.data[key] = value
        return value

    @classmethod
    def bulk_set(cls, **kwargs):
        for key, value in kwargs.items():
            cls.set(key, value)
        return True

    @classmethod
    def delete(cls, key):
        return cls.data.pop(key, None)

    @classmethod
    def save(cls):
        with cls.filepath.open('w') as f:
            json_dump(cls.data, f)
