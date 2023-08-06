import json
from pathlib import Path

from cookiecutter.main import cookiecutter

from kal import path
from kal.utils.config import Config
from kal.utils import github, shell


class Ocel:
    @property
    def default_path(self):
        return path.KAL_HOME_DIR / 'ocel'

    def __init__(self):
        ocel_path = Config.get('ocel', 'path')
        self.ocel_path = Path(ocel_path) if ocel_path else self.default_path
        if not self.ocel_path.exists():
            self.clone_ocel()

    def clone_ocel(self):
        github.clone(
            github.url_parsing('ocel'),
            target=self.ocel_path
        )

    def template_list(self, with_meta=False):
        if with_meta:
            result = {}
        else:
            result = []

        for f in self.ocel_path.glob('./*'):
            subdir = self.ocel_path / f
            if not subdir.is_dir():
                continue

            ocel_file = subdir / 'ocel.json'
            if not ocel_file.exists():
                continue

            if with_meta:
                with ocel_file.open() as file:
                    result[f.name] = json.load(file)
            else:
                result.append(f)

        return result

    def run(self, template, target=None):
        template_path = self.ocel_path / template
        output_dir = target or '.'
        return cookiecutter(template_path, output_dir=output_dir)

    def update(self):
        commands = [
            'cd {}'.format(self.ocel_path),
            'git pull origin master'
        ]
        shell.call('&&'.join(commands))
        return True
