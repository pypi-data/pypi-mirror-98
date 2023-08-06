from setuptools import setup

setup(
    name='good-day',
    version='0.2.0',
    license='MIT',
    description='Module that makes you a good day',

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
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
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
