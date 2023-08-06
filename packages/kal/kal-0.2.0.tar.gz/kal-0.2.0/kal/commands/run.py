from cleo import argument, option
from cleo.commands.base_command import CommandError

from kal.utils.config import Config
from .base import Command


class RunCommand(Command):
    name = 'run'
    description = 'run script in config'
    arguments = [
        argument('name', 'script name', optional=True),
        argument('exec', 'executer of script', optional=True)
    ]
    options = [
        option('list', 'l', 'list all runnable scripts')
    ]

    default_executer = '"${SHELL}"'

    def get_executer(self, name):
        runner = self.argument('exec')
        if runner:
            return runner
        config = Config.script(name)
        runner = config.get('exec')
        return runner or self.default_executer

    def run_script(self, name):
        config = Config.script(name)
        script_root = Config.script_root()
        if not config:
            raise CommandError('No such script: {}'.format(name))
        file = config.get('file')
        if not file:
            raise CommandError('Script does not have file')

        if script_root and file[0] != '/':
            file_path = script_root / file
        else:
            file_path = file

        runner = self.get_executer(name)
        command = '{} {}'.format(runner, file_path)
        self.line('Run command: {}'.format(command))
        self.shell_call(command)
        return True

    def full_file_path(self, file):
        script_root = Config.script_root()
        if script_root and file[0] != '/':
            file_path = script_root / file
        else:
            file_path = file

        return str(file_path)

    def handle(self):
        name = self.argument('name')

        if name:
            self.run_script(name)
        elif self.option('list'):
            script_config = Config.get('script', 'list', default=dict())
            table = self.table()
            table.set_header_row(['name', 'desc', 'script file'])
            for name, config in script_config.items():
                if not config:
                    table.add_row([name, '<error>Invalid</error>', '<error>Invalid</error>'])
                file = config.get('file', '')
                filepath = '' if not file else self.full_file_path(file)
                desc = config.get('desc', '')
                table.add_row([name, desc, filepath])
            table.render(self.io)
        else:
            self.line_error('올바른 명령어를 입력해주세요.')
