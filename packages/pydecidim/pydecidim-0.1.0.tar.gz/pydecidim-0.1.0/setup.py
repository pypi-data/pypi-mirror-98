from distutils.core import setup

setup(
    name='pydecidim',
    version='0.1.0',
    packages=['api', 'model', 'tests'],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        "gql >= 2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)