from . import shell
from kal.utils.config import Config


def url_parsing(repository_name, protocol='ssh'):
    split_names = repository_name.split('/')

    if len(split_names) == 1:
        username = Config.get('github', 'username')
        repository_name = "{}/{}".format(username, repository_name)
    else:
        username = split_names[0]
        repository_name = "{}/{}".format(username, "-".join(split_names[1:]))

    if repository_name.find('.git') < 0:
        repository_name += '.git'

    if protocol == 'ssh':
        repository_name = 'git@github.com:{}'.format(repository_name)
    elif protocol == 'https':
        repository_name = 'https://github.com/{}'.format(repository_name)
    else:
        raise ValueError('Invalid protocol name: {}'.format(protocol))

    return repository_name


def clone(url, target=None):
    command = 'git clone {}'.format(url)
    if target:
        command += ' {}'.format(target)

    return shell.call(command)
