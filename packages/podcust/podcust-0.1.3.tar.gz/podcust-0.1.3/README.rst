================
Podman Custodian
================


.. image:: https://img.shields.io/pypi/v/podcust.svg
        :target: https://pypi.python.org/pypi/podcust

.. image:: https://github.com/Iolaum/podcust/workflows/CI/badge.svg
        :target: https://github.com/Iolaum/podcust/actions

.. image:: https://readthedocs.org/projects/podcust/badge/?version=latest
        :target: https://podcust.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Iolaum/podcust/shield.svg
     :target: https://pyup.io/repos/github/Iolaum/podcust/
     :alt: Updates



Python utility to manage specific deployed podman containers in Fedora.


* Free software: `Licensed`_ under the `Parity License`_
* Documentation:  `Read the Docs`_

.. _`Parity License`: https://paritylicense.com/
.. _`Read the Docs`: https://podcust.readthedocs.io
.. _`Licensed`: https://github.com/Iolaum/podcust/blob/main/License.md

Getting Started
---------------

From a Fedora Workstation installation::

    $ dnf copr enable iolaum/podcust 
    $ dnf install podcust

Features
--------

* Deployment and management of transmission_ `docker container image`_ from linuxserver.io
  `documented here`_.

.. _`transmission`: https://transmissionbt.com/about/
.. _`docker container image`: https://github.com/linuxserver/docker-transmission
.. _`documented here`: https://docs.linuxserver.io/images/docker-transmission

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project
template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
