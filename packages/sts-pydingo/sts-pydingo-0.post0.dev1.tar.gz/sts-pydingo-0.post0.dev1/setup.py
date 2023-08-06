from setuptools import setup

import versioneer

setup(name = 'sts-pydingo', description = 'Client library', author = 'See-Through Scientific',
    packages = ['pydingo'], version = versioneer.get_version(), cmdclass = versioneer.get_cmdclass()
)
