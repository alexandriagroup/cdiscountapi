# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.seller
    ----------------------------

    Handles the seller information.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from .base import BaseSection
from ..helpers import auto_refresh_token


class Seller(BaseSection):
    """
    Seller section lets sellers retrieve information about their seller account
    and their performance indicator.

    Methods::

        get_seller_info()
        get_seller_indicators()

    Operations are included in the Seller API section.
    (https://dev.cdiscount.com/marketplace/?page_id=36)
    """

    @auto_refresh_token
    def get_seller_info(self):
        """
        To get seller info as:
            - Delivery Modes
            - Offer Pool
            - Email
            - Login
            - Phone Number
            - Adress
            - Name
            - Relays
            - Shop Name/Url
            - SIRET
            - Seller Availability
            - Account State

        :return: Information of the authenticated seller.
        """
        response = self.api.client.service.GetSellerInformation(
            headerMessage=self.api.header
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_seller_indicators(self):
        """
        To get all rates about seller as:
            - Order Acceptation
            - Product Shipping
            - Order with claim
            - Order with refund
            - Preparation Deadline respected

        :return: a dict with the data of the user
        """
        response = self.api.client.service.GetSellerIndicators(
            headerMessage=self.api.header
        )
        return serialize_object(response, dict)
