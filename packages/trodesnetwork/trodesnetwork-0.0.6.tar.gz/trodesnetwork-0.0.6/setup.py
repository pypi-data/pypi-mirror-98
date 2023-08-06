from setuptools import setup

setup(
    name="trodesnetwork",
    version="0.0.6",
    description="A library to connect to Trodes over a network",
    packages=["trodesnetwork"],
    install_requires=[
        'pyzmq >=18.0.0,<20.0.0',
        'msgpack'
    ]
)

