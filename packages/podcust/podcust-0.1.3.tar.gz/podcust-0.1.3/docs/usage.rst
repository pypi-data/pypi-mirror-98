=====
Usage
=====


Using Transmission container image
-----------------------------------


To use transmission container image in production::

    $ podcust transmission deploy
    $ podcust transmission service setup
    $ podcust transmission service activate

Now the transmission container is up and running. It will automatically be stopped during shutdown
and will be restarted, and updated if possible, after boot.

To clear the system from a running image and all associated files::

    $ podcust transmission service deactivate
    $ podcust transmission service delete
    $ podcust transmission stop
    $ podcust transmission rm
    $ podcust transmission clear

Note: Container images stored by podman still need to be manually deleted.
