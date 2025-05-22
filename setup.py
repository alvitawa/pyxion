from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='pyxion',
    version='0.1.1',
    description='Python GUI app with editor and variable inspector',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pyxion=pyxion.main:main',
        ],
    },
)
