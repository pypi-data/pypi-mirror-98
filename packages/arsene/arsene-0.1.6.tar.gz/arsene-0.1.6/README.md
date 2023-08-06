<p align="center">
  <img width="320" height="320" src="https://github.com/JeremyAndress/arsene/blob/master/docs/arsene.png?raw=true" alt='Arsene'>
</p>

<p align="center">
<em>Simple cache management to make your life easy.</em>
</p>

<p align="center">
<a href="https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml" target="_blank">
    <img src="https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml/badge.svg" alt="Test">
</a>

<a href="LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg" alt="MIT">
</a>

<a href="https://pypi.python.org/pypi/arsene" target="_blank">
    <img src="https://badge.fury.io/py/arsene.svg" alt="pypy">
</a>
</p>

---

### Requirements 
- Python 3.6+ 

### Installation
```sh
pip install arsene
```

### Quick Start
For the tutorial, you must install redis as dependency

```sh
pip install arsene[redis]
```


The simplest Arsene setup looks like this:

```python
from datetime import datetime
from arsene import Arsene, RedisModel

redis = RedisModel(host='localhost')

arsene = Arsene(redis_connection=redis)


@arsene.cache(key='my_secret_key', expire=2)
def get_user():
    return {
        'username': 'jak',
        'last_session': datetime(year=1999, month=2, day=3)
    }


# return and writes response to the cache
get_user()

# reads response to the cache
get_user()
# Response: {'username': 'jak', 'last_session': datetime.datetime(1999, 2, 3, 0, 0)}

# reads response to the cache
arsene.get(key='my_secret_key')

# delete key to the cache
arsene.delete(key='my_secret_key')
arsene.get(key='my_secret_key')
# Response: None

```