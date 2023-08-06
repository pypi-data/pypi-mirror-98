from setuptools import find_namespace_packages, setup

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='sr.comp.cli',
    version='1.2.0',
    packages=find_namespace_packages(exclude=('tests',)),
    namespace_packages=['sr', 'sr.comp'],
    description="CLI tools for srcomp repositories",
    long_description=long_description,
    author="Student Robotics Competition Software SIG",
    author_email='srobo-devel@googlegroups.com',
    install_requires=[
        'python-dateutil >=2.2, <3',
        'paramiko >=1.10, <3',
        'sr.comp >=1.2, <2',
        'reportlab >=3.1.44, <3.5',
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
    setup_requires=[
        'Sphinx >=3.0.2, <4',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
