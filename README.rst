.. _Docker: https://www.docker.com/
.. _factory: https://github.com/prologic/factory
.. _autodock: https://github.com/prologic/autodock


domains
=======

domains is a Tool to create and manage domain records in the cloud.

domains is MIT licensed.

Installation
------------

Either pull the automatically updated `Docker`_ image::
    
    $ docker pull prologic/domains

Or install from the development repository::
    
    $ git clone https://github.com/prologic/domains.git
    $ cd domains
    $ pip install -r requirements.txt


Usage
-----

List domains in ``domains.yml``:

.. code-block:: bash
    
    $ domains list
    myrandomdomains.com

Synchronoize domain configuration:
    
.. code-block:: bash
    
    $ domains sync
    Creating domain: myrandomdomains.com ... OK

After making modifications to ``domains.yml``; check the status:

.. code-block:: bash
    
    $ domains status
    M        myrandomdomains.com

And resynchronize domain configuratino:

.. code-block:: bash
    
    $ domains sync
    Updating domain: myrandomdomains.com ... OK
