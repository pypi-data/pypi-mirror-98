from setuptools import find_packages, setup

from huscy_project import __version__


entry_points = {
    'console_scripts': [
        'huscy=huscy_project.bin.huscy:main',
    ],
}

extras_require = {
    'testing': [
        'tox',
    ],
}

install_requires = [
    # public dependencies
    'Django',
    'django-auth-ldap',
    'django-cors-headers',
    'django-guardian',
    'psycopg2',

    # local dependencies
    'huscy.appointments',
    'huscy.attributes',
    'huscy.bookings',
    'huscy.project_documents',
    'huscy.project_ethics',
    'huscy.projects',
    'huscy.pseudonyms',
    'huscy.recruitment',
    'huscy.rooms',
    'huscy.subjects',
    'huscy.users',
]

setup(
    name='huscy-project',
    version=__version__,

    description='integration project for some apps',

    author='Alexander Tyapkov, Mathias Goldau, Stefan Bunde',
    author_email='tyapkov@gmail.com, goldau@cbs.mpg.de, stefanbunde+git@posteo.de',

    packages=find_packages(),
    include_package_data=True,

    entry_points=entry_points,
    install_requires=install_requires,
    extras_require=extras_require,
)
