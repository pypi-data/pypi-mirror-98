import codecs
import os
import re

from setuptools import Command, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

version = '0.0.0'
changes = os.path.join(here, 'CHANGES.rst')
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group('version')
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()


install_requirements = []
tests_requirements = []


class VersionCommand(Command):
    description = 'print library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


if __name__ == '__main__':
    setup(
        name='movidesk-client',
        description='A simple client to access API of the Movidesk',
        version=version,
        long_description=long_description,
        long_description_content_type='text/x-rst',
        author='Daniel Bastos',
        author_email='contato@daniellbastos.com.br',
        url='https://github.com/daniellbastos/movidesk-client/',
        install_requires=install_requirements,
        tests_require=tests_requirements,
        keywords=['client', 'movidesk'],
        packages=['movidesk_client'],
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries',
        ],
        cmdclass={'version': VersionCommand},
    )
