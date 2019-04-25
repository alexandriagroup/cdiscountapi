# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.sandbox
    -----------------------------

    Simulates the different processes involved in an order.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from .base import BaseSection


class Sandbox(BaseSection):
    """
    Allows create fake orders, simulate payments, simulate cancellations, get,
    validate fake orders and create refund vouchers after the shipment.

    Operations are included in the Sandbox API section.
    (https://dev.cdiscount.com/marketplace/?page_id=2224)
    """

    def create_fake_order(self, **request):
        """
        Create a fake order

        Usage::

            response = api.sandbox.create_fake_order(request={
            'NumberOfProducts': 1, ProductType: 'Variant',
            'PaymentMode': 'CB1X', 'Quantity': 1,
            'ShippingCode': 'Normal', 'Tenant': 'CDiscount'})
        """
        response = self.api.factory.

