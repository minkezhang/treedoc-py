# treedoc-py

## Installation

```
git clone ...
cd treedoc-py
virtualenv v
. ./v/bin/activate
pip install -r requirements.txt
```

## Testing

```
nosetests --cover-erase --with-coverage --cover-branches --cover-html --cover-html-dir=coverage --cover-package=src
```
