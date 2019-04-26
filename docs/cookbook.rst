.. cookbook:

========
Cookbook
========

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

