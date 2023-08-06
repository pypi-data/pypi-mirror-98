from pathlib import Path

from kal.base.json_obj import BaseJson
from kal import path
from kal.helper import dig


class Config(BaseJson):
    filepath = path.CONFIG_FILE

    @classmethod
    def get(cls, *keys, default=None):
        return dig(cls.data, *keys, default=default)

    @classmethod
    def link(cls, name):
        return cls.get('link', 'list', name, default=None)

    @classmethod
    def script(cls, name):
        return cls.get('script', 'list', name, default=None)

    @classmethod
    def script_root(cls):
        script_root = cls.get('script', 'root', default=None)
        if script_root:
            script_root = Path(script_root)
        return script_root


    @classmethod
    def link_root(cls):
        link_root = cls.get('link', 'root', default=None)
        if link_root:
            link_root = Path(link_root)
        return link_root

    @classmethod
    def docker(cls, name):
        return cls.get('docker', name, default=None)
