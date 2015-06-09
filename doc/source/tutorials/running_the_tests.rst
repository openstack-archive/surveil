
Running the tests
-----------------

Using tox
`````````

Surveil is tested and supported on Python 2.7 and Python 3.4. The project uses tox to manage tests.

The following command will run the tests for Python 3.4, Python 2.7, Flake8 and Docs: ::

    tox

You can also run only one set of tests by specifying the tox environment to run (see tox.ini for more details): ::

    tox -epy27

Building the docs
`````````````````

To build the docs, simply run ``tox -edocs``. The docs will be available in the ``doc/build/html`` folder. After every commit, docs are automatically built on readthedocs and hosted on `surveil.readthedocs.org <http://surveil.readthedocs.org/>`_.

Integration tests
`````````````````

Integration tests are ran nightly on `test.savoirfairelinux.net <https://test.savoirfairelinux.com/job/Surveil>`_. You can run them on your machine with ``tox -eintegration``. Before you launch the command, make sure that you don't have any other Surveil containers running as they may interfere with the integration tests. Integration tests will create muliple containers on your machine.
