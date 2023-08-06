from cleo import argument

from .base import Command
from kal.utils.config import Config


class RunCommand(Command):
    name = 'run'
    description = 'Run docker container for local development'
    arguments = [
        argument('name', 'name of container'),
    ]

    def handle(self):
        name = self.argument('name')
        command = Config.docker(name)
        self.shell_call(command)


class PsCommand(Command):
    name = 'ps'
    description = 'show docker process managed by kal'

    def handle(self):
        self.shell_call('docker ps --filter name=\"kal-*\"')


class StopCommand(Command):
    name = 'stop'
    description = 'stop docker container'
    arguments = [
        argument('name', 'name of container'),
    ]

    def handle(self):
        name = self.argument('name')
        self.shell_call('docker stop kal-{}'.format(name))


class ListCommand(Command):
    name = 'list'
    description = 'all list of available containers'

    def handle(self):
        all_names = list(Config.get('docker', default={}).keys())
        self.line('\n'.join(all_names))


class DockerCommand(Command):
    name = 'docker'
    description = 'kal docker manager command'

    commands = [
        RunCommand(),
        PsCommand(),
        StopCommand(),
        ListCommand(),
    ]
