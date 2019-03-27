# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

from zeep import Client, helpers
import requests
import lxml


class CdiscountApi(object):
    """A class ton manage the interaction with the CdiscountMarketplace API"""
    def __init__(self, login, password):
        self.wsdl = 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl'
        self.auth_url = ('https://sts.cdiscount.com/users/httpIssue.svc/'
                         '?realm=https://wsvc.cdiscount.com/MarketplaceAPIService.svc')
        self.login = login
        self.password = password
        self.client = Client(self.wsdl)
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

    def get_seller_info(self):
        """
        Return the seller data
        :return: a dict with the data of the user
        :rtype: dict
        """
        response = self.client.service.GetSellerInformation(headerMessage=self.header)
        return helpers.serialize_object(response, dict)

    def get_seller_indicators(self):
        """
        Return seller indicators message
        :return: a dict with the data of the user
        :rtype: dict
        """
        response = self.client.service.GetSellerIndicators(headerMessage=self.header)
        return helpers.serialize_object(response, dict)

