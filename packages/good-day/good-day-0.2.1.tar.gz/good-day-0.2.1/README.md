[![Python Package](https://github.com/markgzhou/good-day-gterminal/actions/workflows/python-ci.yml/badge.svg)](https://github.com/markgzhou/good-day-gterminal/actions/workflows/python-ci.yml) [![PyPI version](https://badge.fury.io/py/good-day.svg)](https://pypi.org/project/good-day/) [![wheel](https://img.shields.io/pypi/wheel/good-day)](https://pypi.org/project/good-day/)

```
┌───────────────────────────────────────────────────────────┐   
                         _____                (●>●)          
 _______________ _______|     |_     (͡°͜ʖ͡°)__/____ __   __ 
|       |       |       |  _    |   |      ||       |  | |  |
|    ___|  ___  |  ___  | | |    |  |  _    |   _   |  |_|  |
|   | __| |▀-▀| | |▀-▀| | |_|    |  | | |   |  |_|  |       |
|   ||  | |___| | |___| |        |  | |_|   |       |_     _|
|   |_| |       |       |________|  |       |   _   | |   |  
|_______|_______|_______| \(●●)/    |______||__| |__| |___|  

└───────────────────────────────────────────────────────────┘
```
# Good Day!
Welcome to Good Day!
`Good day begins.Happy coding!`


## 🔧 Install
```
$ pip install --upgrade good-day
```

## Usage
### Run in terminal
Run with confidence in the terminal with the following command:
```
$ good-day
```

## Development
### Test
```
python ./tests/unit_test/test_good_day.py -v
```
### Build
```
python setup.py sdist bdist_wheel
twine check dist/*
```
### Publish
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```