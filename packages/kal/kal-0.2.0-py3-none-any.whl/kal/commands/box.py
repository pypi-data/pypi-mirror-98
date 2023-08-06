import pend

from .base import Command
from kal import path


class BoxCommitCommand(Command):
    name = 'commit'
    description = 'Dropbox git commit and push'

    def handle(self):
        commands = [
            'cd {}'.format(path.DROPBOX_DIR),
            'git add -A',
            'git commit -m "Dropbox update {}. Coomit by kal"'.format(pend.now().strftime('%Y-%m-%d %H:%M:%S')),
            'git push origin master'
        ]

        self.shell_call(' && '.join(commands))


class BoxCommand(Command):
    name = 'box'
    description = 'Dropbox helper command'
    commands = [
        BoxCommitCommand()
    ]

    def handle(self):
        self.line_error('하위 명령어를 입력하세요')
        return 1
