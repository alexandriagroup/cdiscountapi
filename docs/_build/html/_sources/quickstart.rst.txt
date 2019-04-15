.. _quickstart:

Quickstart
==========

Create a connection to the server
---------------------------------

::

  >>> api = Connection(login, password)


Retrieve information about your seller account
----------------------------------------------

::
    >>> seller_info = api.seller.get_seller_info()



