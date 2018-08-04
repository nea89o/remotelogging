from setuptools import find_packages, setup

find_packages
with open('remotelogging/version.py') as fp:
    _loc, _glob = {}, {}
    exec(fp.read(), _loc, _glob)
    version = {**_loc, **_glob}['version']

with open('requirements.txt') as fp:
    requirements = fp.read().splitlines()

with open('requirements-server.txt') as fp:
    server_requirements = fp.read().splitlines()

with open('README.md') as fp:
    readme = fp.read()

if not version:
    raise RuntimeError('Version is not set in remotelogging/version.py')

setup(
    name="remotelogging",
    author="romangraef",
    url="https://github.com/romangraef/remotelogging",
    version=str(version),
    install_requires=requirements,
    long_description=readme,
    setup_requires=['pytest-runner', 'pytest-pylint'],
    tests_require=['pytest', 'pylint'],
    license="MIT",
    extras_require={
        'setup': server_requirements,
    },
    packages=['remotelogging'],
    description="Python remote logging server and library",
    classifiers=[
        'Topic :: Logging',
    ]
)
