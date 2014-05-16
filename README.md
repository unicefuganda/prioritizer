Prioritizer
==================

Small app to cache data using redis and python.

First steps
------------
Install virtual env for the project -> http://www.virtualenv.org/en/latest/virtualenv.html#installation


    $ cd $VIRTUALENV_HOME

    $ virtualenv prioritizer

    $ source prioritizer/bin/activate

Installing pip require packages

    $ cd $PRIORITIZER_PATH

    $ pip install -r pip-requires.txt
    
Running tests
-------------

    $ python -m unittest discover -p 'test*.py'

Running Prioritizer Application
-------------------------------

    $ source $VIRTUALENV_HOME/prioritizer/bin/activate
    
    $ cd $PRIORITIZER_PATH

    $ python prioritizer.py

Running Gearman Throttle Application
------------------------------------

    $ source $VIRTUALENV_HOME/prioritizer/bin/activate
    
    $ cd $PRIORITIZER_PATH

    $ python throttle.py

Also it is necessary to have at least a worker running

    $ python run-worker.py


Observations
------------
In order to run the example redis should have been properly install in the server
http://redis.io/download

Note: Make sure redis-server is running

In order to run gearman throttle it is needed to install gearman in your server http://gearman.org/getting-started/

E.g. apt-get install gearman-job-server
