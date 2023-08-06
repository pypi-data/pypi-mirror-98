[![CircleCI branch](https://img.shields.io/circleci/project/github/mkeshav/pace-maker/master.svg)](https://circleci.com/gh/mkeshav/pace-maker/tree/master)
[![PyPI version](https://badge.fury.io/py/pacemaker-mkeshav.svg)](https://badge.fury.io/py/pacemaker-mkeshav)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pacemaker-mkeshav.svg)](https://badge.fury.io/py/pacemaker-mkeshav)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mkeshav_pace-maker&metric=alert_status)](https://sonarcloud.io/dashboard?id=mkeshav_pace-maker)

# Pace Maker 
There are times in your life when you have to call legacy api's that can handle like 2 reqs/sec. There is no point hammering the old man and killing him. 

This library will help you pace calls to the old man, so his heart keeps ticking. 

Combining this library with backoff(https://github.com/litl/backoff) can do wonders.

# Install
python3 -m pip install pacemaker-mkeshav

# Usage
```
    from pacemaker import pace_me

    # Function that will yield data that the process function needs
    def data_gen(n=3):
        for i in range(n):
            yield [x for x in range(n)]

    # Will make 3 requests to that url/sec using 1 token everytime process method is called. What data_gen function yields should be the first argument
    @pace_me(data_gen, rate_per_second=3, n=6)
    def process(data, url):
        r = requests.post(url, data=data)
```
# Run tests
- All tests (`docker-compose run --rm test`)
