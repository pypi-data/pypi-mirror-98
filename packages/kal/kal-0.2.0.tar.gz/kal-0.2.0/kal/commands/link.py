from cleo import argument, option
from cleo.commands.base_command import CommandError

from kal.utils.config import Config
from .base import Command


class LinkCommand(Command):
    name = 'ln'
    description = 'link file creator'
    arguments = [
        argument('name', description='name of link in config json', optional=True),
    ]
    options = [
        option('list', 'l', description='show list of link config'),
        option('no-input', description='Run with no confirm')
    ]

    def generate_link(self, source, target):
        link_root = Config.link_root()
        if type(source) is not str or type(target) is not str:
            raise CommandError('Type error: source is not str type')

        if link_root and source[0] != '/':  # 루트에서 시작하면 그냥 넘어가기
            source_path = link_root / source
        else:
            source_path = source

        command = 'ln -sf {} {}'.format(
            source_path, target,
        )
        self.line(command)
        self.shell_call(command)
        return True

    def create_link(self, name, no_input=False):
        if name == 'all':
            link_config = Config.get('link', 'list', default=dict())
            if not no_input:
                if not self.confirm('전체 링크 작업을 실행하시겠습니까?', default=True):
                    self.line_error('실행 거부')
                    return False
            for name in link_config.keys():
                self.create_link(name, no_input=True)
            self.line('Done')
        else:
            link_path = Config.link(name)
            if not link_path:
                raise CommandError('link config not found: {}'.format(name))
            if not no_input:
                if not self.confirm('{} 링크 작업을 실행하시겠습니까?'.format(name), default=True):
                    self.line_error('실행 거부')
                    return False

            if type(link_path[0]) is str:
                if len(link_path) == 2:
                    return self.generate_link(link_path[0], link_path[1])
            elif type(link_path[0]) in (list, tuple, set):
                for i in link_path:
                    if len(i) != 2:
                        raise CommandError('Invalid format of link config: {}'.format(name))
                    self.generate_link(i[0], i[1])
                return True

            raise CommandError('Invalid format of link config: {}'.format(name))

    def add_list_row(self, table, name, config):
        if len(config) != 2:
            table.add_row([name, '<error>Invalid</error>', '<error>Invalid</error>'])
        else:
            table.add_row([name, *config])

    def handle(self):
        name = self.argument('name')

        if name:
            self.create_link(name, self.option('no-input'))
        elif self.option('list'):
            link_config = Config.get('link', 'list', default=dict())
            table = self.table()
            table.set_header_row(['name', 'source', 'target'])
            for name, config in link_config.items():
                if not config:
                    table.add_row([name, '<error>Invalid</error>', '<error>Invalid</error>'])
                if type(config[0]) in (list, tuple, set):
                    self.add_list_row(table, name, config[0])
                    for t in config[1:]:
                        self.add_list_row(table, '', t)
                elif type(config[0]) is str:
                    self.add_list_row(table, name, config)
                else:
                    table.add_row([name, '<error>Invalid</error>', '<error>Invalid</error>'])
            table.render(self.io)
        else:
            self.line_error('올바른 명령어를 입력해주세요.')
