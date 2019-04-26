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


Validate an order
-----------------

In order to validate an order, you have to provide the information:

- about each item in the order (order line) and the corresponding AcceptationState,
- about the order and the OrderState.


Validate the shipment
---------------------

::

    shipped = {'CarrierName': 'Colissimo', 'OrderNumber': '1904241640CLE8Z',
               'OrderState': 'Shipped', 'TrackingNumber': 'TN1',
               'TrackingUrl':'http://www.colissimo.fr/portail_colissimo/suivre.do?language=fr_FR',
               'OrderLineList': [
               {'AcceptationState': 'ShippedBySeller',
                'SellerProductId': 'PRES1',
                'ProductCondition': 'AverageState'}]}

    validations = api.orders.prepare_validations([shipped])
    response = api.validate_order_list(**validations)
