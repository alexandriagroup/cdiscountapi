# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

from zeep import Client, helpers
import requests
import lxml


class Seller(object):
    def __init__(self, api):
        self.api = api

    def get_seller_info(self):
        response = self.api.client.service.GetSellerInformation(headerMessage=self.api.header)
        return helpers.serialize_object(response, dict)


class CdiscountApi(object):
    """A class ton manage the interaction with the CdiscountMarketplace API"""

    wsdl = 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl'
    auth_url = ('https://sts.cdiscount.com/users/httpIssue.svc/'
                '?realm=https://wsvc.cdiscount.com/MarketplaceAPIService.svc')
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.client = Client(self.wsdl)
        self.seller = Seller(self)
        self.token = self.get_token()
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
                'TokenId': self.token,
                'UserName': '',
            },
            'Version': 1.0,
        }

    def get_token(self):
        response = requests.get(self.auth_url, auth=(self.login, self.password))
        return lxml.etree.XML(response.text).text

    def get_seller_indicators(self):
        """
        Return seller indicators message
        :return: a dict with the data of the user
        :rtype: dict
        """
        response = self.client.service.GetSellerIndicators(headerMessage=self.header)
        return helpers.serialize_object(response, dict)

