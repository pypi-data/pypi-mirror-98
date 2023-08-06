from cleo import Application as BaseApplication

from kal import __version__
from kal.initialize import init
from . import commands as cmds


class Application(BaseApplication):
    def __init__(self, *args, **kwargs):
        init()
        super().__init__('kal', __version__)
        for command in self.get_default_commands():
            self.add(command)

    def get_default_commands(self):
        return [
            cmds.EnvCommand(),
            cmds.CloneCommand(),
            cmds.KSTCommand(),
            cmds.UTCCommand(),
            cmds.BoxCommand(),
            cmds.LinkCommand(),
            cmds.RunCommand(),
            cmds.DockerCommand(),
            cmds.OcelCommand(),
        ]
