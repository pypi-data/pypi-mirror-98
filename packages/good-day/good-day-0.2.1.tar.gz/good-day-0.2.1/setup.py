from setuptools import setup
from codecs import open
from os import path

cwd = path.abspath(path.dirname(__file__))

with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='good-day',
    version='0.2.1',
    license='MIT',
    description='Module that makes you a good day',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Guanlong (Mark) Zhou',
    author_email='markgzhou@outlook.com',

    url='https://github.com/markgzhou/good-day-gterminal',
    keywords=['good day', 'good', 'day'],

    py_modules=['good_day'],
    entry_points={
        'console_scripts': [
            'good-day=good_day:main'
        ]
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
