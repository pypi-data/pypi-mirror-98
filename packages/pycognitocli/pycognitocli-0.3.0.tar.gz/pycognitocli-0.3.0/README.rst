============
pycognitocli
============

CLI for https://pypi.org/project/pycognito/

Try::

    pycognitocli -p "region_mypool" -a "myappid" -cs "myappsecret" token get -u "username" -pw 'password'

Or export following environment variables:

  - COGNITO_POOL_ID
  - COGNITO_APP_ID
  - COGNITO_APP_SECRET
  - COGNITO_USERNAME
  - COGNITO_PASSWORD

You do not have to give the password (or username) on command-line, the app can prompt for it

Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it (switch the 1234 port to the port from src/pycognitocli/defaultconfig.py)::

    docker build --ssh default --target devel_shell -t pycognitocli:devel_shell .
    docker create --name pycognitocli_devel -v `pwd`":/app" -it `echo $DOCKER_SSHAGENT` pycognitocli:devel_shell
    docker start -i pycognitocli_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i pycognitocli_devel /bin/bash -c "pre-commit install"
    docker exec -i pycognitocli_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run -it --rm -v `pwd`":/app" pycognitocli:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t pycognitocli:tox .
    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` pycognitocli:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for running the application (change the "1234" port and "myconfig.toml" for
config file)::

    docker build --ssh default --target production -t pycognitocli:latest .
    docker run -it --rm pycognitocli:latest pycognitocli -p "region_mypool" -a "myappid" -cs "myappsecret" token get -u "username" -pw 'password'


Local Development
-----------------

TLDR:

- Create and activate a Python 3.8 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.8` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go, try the following::

    pycognitocli --defaultconfig >config.toml
    pycognitocli -vv config.toml

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
