
wordpress_oauth
===============


.. image:: https://img.shields.io/pypi/v/package_name.svg
   :target: https://pypi.python.org/pypi/wordpress_oauth
   :alt: Latest PyPI version


Python REST API wrapper for WP-API/OAuth1

Usage
-----

.. code-block::

   import wordpress_oauth
   api = wordpress_oauth.Wordpress("~/.config/pywordpress_oauth/config.yml")
   image_path = "images/icon.png"
   result = api.upload_image(image_path)

This library asks auth setting on initial startup.

Installation
------------

.. code-block::

   pip install wordpress_oauth

Requirements
^^^^^^^^^^^^

`WP REST API - OAuth 1.0a Server <https://github.com/WP-API/OAuth1>`_

Compatibility
-------------

Licence
-------

Authors
-------

wordpress_oauth was written by `fx-kirin <fx.kirin@gmail.com>`_.
