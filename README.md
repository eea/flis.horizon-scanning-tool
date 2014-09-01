Horizon Scanning Tool
=====================

collectstatic before evrthng


Prerequisites - System packages
-------------------------------

These packages should be installed as superuser (root).

### Debian based systems ###

Install these before setting up an environment:

    apt-get install python-setuptools python-dev python-virtualenv git


### RHEL based systems ###
Install Python2.7 with PUIAS: https://gist.github.com/nico4/9616638

Run these commands:

    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7 -
    pip2.7 install virtualenv
    yum install git


Install dependencies
--------------------

We should use Virtualenv for isolated environments. The following commands will
be run as an unprivileged user in the product directory:

1.Clone the repository:


    git clone git@github.com:eea/horizon-scanning-tool.git -o origin gemet
    cd horizon-scanning-tool

2.1.Create & activate a virtual environment:


    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

2.2.Make sure setuptools >= 0.8 is installed:

    pip install -U setuptools

3.Install dependencies:


    pip install -r requirements-dep.txt

4.Create a local configuration file:


    cd hstool
    cp local_settings.py.example local_settings.py

    # Follow instructions in local_settings.py to adapt it to your needs.

5.Create initial database structure:


    ./manage.py syncdb

6.Load fixtures data into the database:


    ./manage.py loadfixtures

Build production
----------------

[TODO]

Build staging
-------------

[TODO]


Contacts
========


The project owner is Valentin Dumitru (valentin.dumitru at eaudeweb.ro)

Other people involved in this project are:

* Alex Eftimie (alex.eftimie at eaudeweb.ro)
* Mihai Zamfir (mihai.zamfir at eaudeweb.ro)


Resources
=========

[TODO]


Hardware
--------

[TODO]


Software
--------

[TODO]


Copyright and license
=====================
