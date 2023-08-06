from cleo import option, argument
from cleo.commands.base_command import CommandError

from kal.utils.ocel import Ocel
from .base import Command


class OcelCommand(Command):
    name = 'ocel'
    description = 'ocel command'
    arguments = [
        argument('template', 'name of template', optional=True),
        argument('target', 'target path', optional=True)
    ]
    options = [
        option('list', 'l', 'list of templates'),
        option('update', 'u', 'update ocel from github', )
    ]

    def handle(self):
        ls = self.option('list')
        update = self.option('update')
        template = self.argument('template')
        target = self.argument('target')
        ocel = Ocel()

        if template and (ls or update):
            raise CommandError('Invalid format of command')

        if template:
            ocel.run(template, target)
            self.line('Finished.')
        elif ls:
            template_list = ocel.template_list(True)
            table = self.table(['Name', 'Desc'])
            for name, meta in template_list.items():
                table.add_row([name, meta.get('desc', '')])
            table.render(self.io)
        elif update:
            ocel.update()
        else:
            raise CommandError('Invalid format of command')
