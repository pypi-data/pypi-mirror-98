from distutils.core import setup

setup(
    name='pydecidim',
    version='0.1.1',
    packages=['pydecidim','pydecidim/api', 'pydecidim/model', 'pydecidim/tests'],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        "gql >= 2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)