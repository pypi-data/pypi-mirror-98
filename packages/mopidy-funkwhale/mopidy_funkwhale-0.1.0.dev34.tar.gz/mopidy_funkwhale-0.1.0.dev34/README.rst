================
mopidy-funkwhale
================

A small `Mopidy`_ backend extension to stream music from a Funkwhale server.


Features
--------

* Searching for tracks, albums and artists available in your Funkwhale instance
* Browse all libraries, artists and albums
* Browse your favorites
* Simple configuration

Installation
------------

We assume you have a Mopidy server available (version 3 or greater required).

.. code-block:: shell

    apt-get install libcairo2-dev libgirepository1.0-dev python3-dev
    sudo python3 -m pip install mopidy-funkwhale


.. note::

    Depending on your setup, you may want to run this comand with ``sudo`` or ``--user``


Configuration
-------------

To enable the extension, add the following to your ``mopidy.conf`` file::

    [funkwhale]
    enabled = true
    # URL of your funkwhale instance
    url = https://demo.funkwhale.audio
    # Application credentials (leave empty fo anonymous access)
    # If you don't now what to put here, just run `mopidy funkwhale login` for
    # the instructions
    client_id =
    client_secret =
    # If for some reason, you want to use the legacy password-based auth,
    # uncomment the variables below
    # username = demo
    # password = demo

    # duration of cache entries before they are removed, in seconds
    # 0 to cache forever, empty to disable cache
    cache_duration = 600

Of course, replace the demo values with your actual info (but you can
try using the demo server).

After that, reload your mopidy daemon, and you should be good!

Authorization
-------------

This plugin support the OAuth authorization workflow that is included in Funkwhale 0.19.

Run ``mopidy funkwhale login`` to perform authorization.

.. _Mopidy: https://www.mopidy.com/
.. _ncmpcpp: https://wiki.archlinux.org/index.php/ncmpcpp
.. _iris: https://github.com/jaedb/iris
