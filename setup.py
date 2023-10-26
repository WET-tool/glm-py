from setuptools import setup

import versioneer

# see pyproject.toml for static project metadata
setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)