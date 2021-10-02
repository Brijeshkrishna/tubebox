from setuptools import setup,find_packages
from io import open

version = "1.0.0"


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(
    name='tubebox',
    version=version,
    description='Python youtube scaper',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='brijeshkrishna',
    author_email='brijeshkrishna@gmail.com',
    url='https://github.com/brijeshkrishna/tubebox',
    packages=['tubebox'],
    license='MIT',
    keywords=['tubebox', 'youtube','youtube-scaper','scaper','python'],
    install_requires=['requests','bs4','gunlink','lxml','numpy','pydantic'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        
    ]
)
