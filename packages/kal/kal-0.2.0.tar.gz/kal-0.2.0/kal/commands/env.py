from .base import Command
from kal import path


class EnvCommand(Command):
    name = 'env'
    description = 'get kal envs'

    def handle(self):
        envs = {
            "SOURCE_DIR": path.SOURCE_DIR,
            "PROJECT_DIR": path.PROJECT_DIR,
            "USER_HOME_DIR": path.USER_HOME_DIR,
            "KAL_HOME_DIR": path.KAL_HOME_DIR,
            "DROPBOX_DIR": path.DROPBOX_DIR,
            "CONFIG_FILE": path.CONFIG_FILE,
            "STORAGE_FILE": path.STORAGE_FILE,
        }

        for name, env in envs.items():
            self.line("{}={}".format(name, env))
