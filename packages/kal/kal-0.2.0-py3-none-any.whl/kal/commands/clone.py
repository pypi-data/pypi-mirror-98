from cleo import argument, option

from .base import Command
from kal.utils.github import url_parsing, clone


class CloneCommand(Command):
    name = 'clone'
    description = 'clone repository from github'
    arguments = [
        argument('repository', 'name of repository that you want to clone'),
        argument('target', 'target directory name', optional=True),
    ]
    options = [
        option('url', 'u', 'echo only url, not clone')
    ]

    def handle(self):
        clone_url = url_parsing(self.argument('repository'))
        if self.option('url'):
            self.line(clone_url)
            return 1
        clone(clone_url, self.argument('target'))
