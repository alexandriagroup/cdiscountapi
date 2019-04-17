.. _quickstart:

Quickstart
==========

Create a connection to the server
---------------------------------

The first thing to do is to connect to the API::

  api = Connection(login, password)

After the connection is created, the token is available. You can get it with
the attribute ``token``.


Retrieve information about your seller account
----------------------------------------------

::

    seller_info = api.seller.get_seller_info()
