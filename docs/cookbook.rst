.. cookbook:

========
Cookbook
========

..  TODO Add a note on ProductCondition (int in the OfferPackage).

------
Offers
------

We'll assume we want to create an offer with the following parameters and values:

================= ================
Parameter          Value
================= ================
SellerProductId    SKU
ProductCondition   AverageState
ProductEan         978-1593274351
Price              35
Stock              10
PreparationTime    1
================= ================

with 3 delivery modes: Standard, Tracked and Registered.

.. note::

    - cdiscount.com id: 1
    - cdiscountpro.com id: 16


Submit an offer package on cdiscount.com and cdiscountpro.com
-------------------------------------------------------------

Create the offer package with :py:meth:`Offers.generate_offer_package`::

    offer = {
        'ProductEan': '978-1593274351',
        'SellerProductId': 'SKU',
        'ProductCondition': 4,
        'Price': 35,
        'ShippingInformationList': {
            'ShippingInformation': [
                {'ShippingCharges': 2, 'DeliveryMode': 'Standard', 'AdditionalShippingCharges': 0},
                {'ShippingCharges': 3, 'DeliveryMode': 'Registered', 'AdditionalShippingCharges': 0},
                {'ShippingCharges': 4, 'DeliveryMode': 'Tracked', 'AdditionalShippingCharges': 0},
                ]
        },
        'Stock': 10,
        'PreparationTime': 1
    }

    offer_package_path = api.offers.generate_offer_package(
        'books_offers',
        [offer_package],
        offer_publication_list=[1, 16]
    )

Upload the package *books_offers.zip* on a server then submit it with
:py:meth:`Offers.submit_product_package` by specifying the url of the package::

    response = api.offers.submit_product_package('http://www.myserver/books_offers.zip')


Update an offer on cdiscount.com
--------------------------------


Purge the inventory for on cdiscount.com
----------------------------------------

.. 
  To remove some offers from your inventory, use the keyword `purge_and_replace`
  in :py:meth:`Offers.generate_offer_package`::

      offer = {
          'ProductEan': '978-1593274351',
          'SellerProductId': 'SKU',
          'ProductCondition': 4,
          'Price': 35,
          'ShippingInformationList': {
              'ShippingInformation': [
                  {'ShippingCharges': 2, 'DeliveryMode': 'Standard', 'AdditionalShippingCharges': 0},
                  {'ShippingCharges': 3, 'DeliveryMode': 'Registered', 'AdditionalShippingCharges': 0},
                  {'ShippingCharges': 4, 'DeliveryMode': 'Tracked', 'AdditionalShippingCharges': 0},
                  ]
          },
          'Stock': 10,
          'PreparationTime': 1
      }

      offer_package_path = api.offers.generate_offer_package(
          'books_to_remove_from_offers',
          [offer_package],
          offer_publication_list=[1, 16]
      )


------
Orders
------

We'll assume there is an order with one order line with the following parameters and values:

================ ============
Parameter        Value
================ ============
OrderNumber      ORDER_NUMBER
SellerProductId  SKU
ProductCondition AverageState
================ ============

Accept the order
----------------

::

    accepted_by_seller = {'CarrierName': 'Colissimo',
                          'OrderState': 'AcceptedBySeller',
                          'OrderNumber': 'ORDER_NUMBER', 
                          'OrderLineList': [{
                          'AcceptationState': 'AcceptedBySeller',
                          'SellerProductId': 'SKU',
                          'ProductCondition': 'AverageState'}]}
    validations = api.orders.prepare_validations([accepted_by_seller])
    response = api.orders.validate_order_list(**validations)


Refuse the shipment of an order
-------------------------------

After the order is accepted if, for some reason, you can't ship it to your
customer, you can refuse the shipment::

    shipment_refused_by_seller = {'OrderNumber': 'ORDER_NUMBER',
                                  'OrderState': 'ShipmentRefusedBySeller',
                                  'OrderLineList': [{
                                  'AcceptationState': 'ShipmentRefusedBySeller',
                                  'SellerProductId': 'SKU',
                                  'ProductCondition': 'AverageState'}]}      

    validations = api.orders.prepare_validations([shipment_refused_by_seller])
    response = api.orders.validate_order_list(**validations)


Refund the customer
-------------------

::
    
    response = api.orders.create_refund_voucher(
        OrderNumber='ORDER_NUMBER',
        SellerRefundList={'Mode': 'Claim', 'Motive': 'ClientClaim',
            'RefundOrderLine': {'Ean': None, 'SellerProductId': 'SKU'
                                'RefundShippingCharges': False}}
    )

A commercial gesture is also possible by adding the keyword ``CommercialGestureList``::

    response = api.orders.create_refund_voucher(
        OrderNumber='ORDER_NUMBER',
        CommercialGestureList=[{'Amount': 10, 'MotiveId': 'late_delivery'}],
        SellerRefundList={'Mode': 'Claim', 'Motive': 'ClientClaim',
            'RefundOrderLine': {'Ean': None, 'SellerProductId': 'SKU',
                                'RefundShippingCharges': False}}
    )

