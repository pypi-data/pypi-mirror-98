import subprocess


def call(command, output=None, **kwargs):
    if output is not None:
        output = getattr(subprocess, output.upper())

    return subprocess.run(command, shell=True, stdout=output, encoding='utf-8')
