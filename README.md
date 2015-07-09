domains
=======

domains is a Tool to create and manage domain records in the cloud.

domains is MIT licensed.

Installation
------------

Either pull the automatically updated [Docker](https://www.docker.com/) image:

    $ docker pull prologic/domains

Or install from the development repository:

    $ git clone https://github.com/prologic/domains.git
    $ cd domains
    $ pip install -r requirements.txt

Usage
-----

List domains in `domains.yml`:

``` sourceCode
$ domains list
myrandomdomains.com
```

Synchronoize domain configuration:

``` sourceCode
$ domains sync
Creating domain: myrandomdomains.com ... OK
```

After making modifications to `domains.yml`; check the status:

``` sourceCode
$ domains status
M        myrandomdomains.com
```

And resynchronize domain configuratino:

``` sourceCode
$ domains sync
Updating domain: myrandomdomains.com ... OK
```
