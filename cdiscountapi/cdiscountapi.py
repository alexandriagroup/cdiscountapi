# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

from xmltodict import parse  # Used for new requests.
from zeep import Client


class CdiscountApi(object):
    """A class ton manage the interaction with the CdiscountMarketplace API"""
    def __init__(self, token):
        self.wsdl = 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl'
        # self.token = token
        self.client = Client(self.wsdl)
        self.header = {
            'Context': {
                'SiteID': 100
            },
            'Localization': {
                'Country': 'Fr',
            },
            'Security': {
                'IssuerID': None,
                'SessionID': None,
                'TokenId': token,
                'UserName': '',
            },
            'Version': 1.0,
        }

    def get_seller_info(self):
        """
        Return the seller data
        :return: a dict with the data of the user
        :rtype: dict
        """
        response = self.client.service.GetSellerInformation(headerMessage=self.header)
        return response

    def get_seller_indicators(self):
        """
        Return seller indicators message
        :return: a dict with the data of the user
        :rtype: dict
        """

        response = self.client.service.GetSellerIndicators(headerMessage=self.header)
        return response

