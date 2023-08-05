from datetime import datetime

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

_now = datetime.now()
_version = '%s.%02d%02d.%02d%02d' % (_now.year, _now.month, _now.day, _now.hour, _now.minute)

with open('./aloha/_version.py', 'wt') as fp:
    fp.write('__version__ = "%s"\n' % _version)

setup(
    name='aloha',
    version=_version,
    author='QPod',
    author_email='45032326+QPod0@users.noreply.github.com',
    url='https://github.com/QPod/aloha',
    license='BSD',

    packages=find_packages(where="."),
    include_package_data=True,
    package_data={},
    platforms='Linux, Mac OS X, Windows',
    zip_safe=False,
    install_requires=[
        'pyhocon'
    ],
    extras_require={
        'build': ['Cython'],
        'service': ['tornado'],
        'db': ['sqlalchemy', 'psycopg2-binary', 'pymysql', 'elasticsearch', 'pymongo'],
        'data': ['pandas'],
        'report': ['openpyxl']
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'aloha = aloha.script.entry_points:main'
        ]
    },

    data_files=[],
    description='Aloha.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
