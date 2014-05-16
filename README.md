Prioritizer
==================

Small app to cache data using redis and python.

First steps
------------
Install virtual env for the project -> http://www.virtualenv.org/en/latest/virtualenv.html#installation


    $ cd <VIRTUALENV_HOME>

    $ virtualenv prioritizer

    $ source prioritizer/bin/activate

Installing pip require packages

    $ cd project_path

    $ pip install -r pip-requires.txt
    
Running tests
-------------

    $ python -m unittest discover -p 'test*.py'

Observations
------------
In order to run the example redis should have been properly install in the server
http://redis.io/download

Note: Make sure redis-server is running
