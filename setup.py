from setuptools import setup, find_packages

setup(
    name='varinspector',
    version='0.1.0',
    description='Python GUI app with editor and variable inspector',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=['pygments'],
    entry_points={
        'console_scripts': [
            'varinspector=varinspector.main:main',
        ],
    },
)
