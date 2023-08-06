from setuptools import find_namespace_packages, setup

with open('README.rst') as f:
    long_description = f.read()

with open('setup-requirements.txt') as f:
    setup_requires = f.readlines()

setup(
    name='sr.comp.cli',
    version='1.3.0',
    project_urls={
        'Documentation': 'https://srcomp-cli.readthedocs.org/',
        'Code': 'https://github.com/PeterJCLaw/srcomp-cli',
        'Issue tracker': 'https://github.com/PeterJCLaw/srcomp-cli/issues',
    },
    packages=find_namespace_packages(exclude=('tests',)),
    namespace_packages=['sr', 'sr.comp'],
    description=(
        "Command line tools for interacting with the state of the Student "
        "Robotics Competition"
    ),
    long_description=long_description,
    author="Student Robotics Competition Software SIG",
    author_email='srobo-devel@googlegroups.com',
    install_requires=[
        'python-dateutil >=2.2, <3',
        'paramiko >=1.10, <3',
        'sr.comp >=1.2, <2',
        'reportlab >=3.1.44, <3.6',
        'requests >=2.5.1, <3',
        'ruamel.yaml >=0.13.0, <0.16',
        'simplejson >=3.6, <4',
        'mido >=1.1, <2',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'srcomp = sr.comp.cli.command_line:main',
        ],
    },
    setup_requires=setup_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
