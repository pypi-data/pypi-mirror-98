How to contribute to Deprecated Library
=======================================

Thank you for considering contributing to Deprecated!

Support questions
-----------------

Please, don't use the issue tracker for this. Use one of the following
resources for questions about your own code:

* Ask on `Stack Overflow`_. Search with Google first using:
  ``site:stackoverflow.com deprecated decorator {search term, exception message, etc.}``

.. _Stack Overflow: https://stackoverflow.com/search?q=python+deprecated+decorator

Reporting issues
----------------

- Describe what you expected to happen.
- If possible, include a `minimal, complete, and verifiable example`_ to help
  us identify the issue. This also helps check that the issue is not with your
  own code.
- Describe what actually happened. Include the full traceback if there was an
  exception.
- List your Python, Deprecated versions. If possible, check if this
  issue is already fixed in the repository.

.. _minimal, complete, and verifiable example: https://stackoverflow.com/help/mcve

Submitting patches
------------------

- Include tests if your patch is supposed to solve a bug, and explain
  clearly under which circumstances the bug happens. Make sure the test fails
  without your patch.
- Try to follow `PEP8`_, but you may ignore the line length limit if following
  it would make the code uglier.

First time setup
~~~~~~~~~~~~~~~~

- Download and install the `latest version of git`_.
- Configure git with your `username`_ and `email`_::

        git config --global user.name 'your name'
        git config --global user.email 'your email'

- Make sure you have a `GitHub account`_.
- Fork Deprecated to your GitHub account by clicking the `Fork`_ button.
- `Clone`_ your GitHub fork locally::

        git clone https://github.com/{username}/deprecated.git
        cd deprecated

- Add the main repository as a remote to update later::

        git remote add tantale https://github.com/tantale/deprecated.git
        git fetch tantale

- Create a virtualenv::

        python3 -m venv env
        . env/bin/activate
        # or "env\Scripts\activate" on Windows

- Install Deprecated in editable mode with development dependencies::

        pip install -e ".[dev]"

.. _GitHub account: https://github.com/join
.. _latest version of git: https://git-scm.com/downloads
.. _username: https://help.github.com/articles/setting-your-username-in-git/
.. _email: https://help.github.com/articles/setting-your-commit-email-address-in-git/
.. _Fork: https://github.com/tantale/deprecated#fork-destination-box
.. _Clone: https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork

Start coding
~~~~~~~~~~~~

- Create a branch to identify the issue you would like to work on (e.g.
  ``2287-dry-test-suite``)
- Using your favorite editor, make your changes, `committing as you go`_.
- Try to follow `PEP8`_, but you may ignore the line length limit if following
  it would make the code uglier.
- Include tests that cover any code changes you make. Make sure the test fails
  without your patch. `Running the tests`_.
- Push your commits to GitHub and `create a pull request`_.
- Celebrate 🎉

.. _committing as you go: http://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes
.. _PEP8: https://pep8.org/
.. _create a pull request: https://help.github.com/articles/creating-a-pull-request/

Running the tests
~~~~~~~~~~~~~~~~~

Run the basic test suite with::

    pytest tests/

This only runs the tests for the current environment. Whether this is relevant
depends on which part of Deprecated you're working on. Travis-CI will run the full
suite when you submit your pull request.

The full test suite takes a long time to run because it tests multiple
combinations of Python and dependencies. You need to have Python 2.7,
3.4, 3.5, 3.6, PyPy 2.7 and 3.6 installed to run all of the environments (notice
that Python **2.6** and **3.3** are no more supported). Then run::

    tox

Running test coverage
~~~~~~~~~~~~~~~~~~~~~

Generating a report of lines that do not have test coverage can indicate
where to start contributing. Run ``pytest`` using ``coverage`` and generate a
report on the terminal and as an interactive HTML document::

    pytest --cov-report term-missing --cov-report html --cov=deprecated tests/
    # then open htmlcov/index.html

Read more about `coverage <https://coverage.readthedocs.io>`_.

Running the full test suite with ``tox`` will combine the coverage reports
from all runs.

``make`` targets
~~~~~~~~~~~~~~~~

Deprecated provides a ``Makefile`` with various shortcuts. They will ensure that
all dependencies are installed.

- ``make test`` runs the basic test suite with ``pytest``
- ``make cov`` runs the basic test suite with ``coverage``
- ``make test-all`` runs the full test suite with ``tox``

Generating the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation is automatically generated with ReadTheDocs for each git push on master.
You can also generate it manually using Sphinx.

To generate the HTML documentation, run::

    sphinx-build -b html -d dist/docs/doctrees docs/source/ dist/docs/html/


To generate the epub v2 documentation, run::

    sphinx-build -b epub -d dist/docs/doctrees docs/source/ dist/docs/epub/
