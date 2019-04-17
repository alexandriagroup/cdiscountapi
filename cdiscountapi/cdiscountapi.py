# -*- coding: utf-8 -*-
"""
    cdiscountapi.cdiscountapi
    -------------------------

    :copyright: © 2019 Alexandria
"""


import lxml
import requests
from zeep import Client
from zeep.plugins import HistoryPlugin

from cdiscountapi.exceptions import (
    CdiscountApiConnectionError,
)

from cdiscountapi.sections import (
    Seller, Offers, Products, Orders, Relays,
    Fulfillment, WebMail, Discussions
)


class Connection(object):
    """A class to manage the interaction with the CdiscountMarketplace API"""

    def __init__(self, login, password, preprod=False):
        self.preprod = preprod
        if self.preprod:
            domain = 'preprod-cdiscount.com'
        else:
            domain = 'cdiscount.com'

        self.wsdl = 'https://wsvc.{0}/MarketplaceAPIService.svc?wsdl'.format(domain)
        self.auth_url = ('https://sts.{0}/users/httpIssue.svc/'
                         '?realm=https://wsvc.{0}/MarketplaceAPIService.svc'.format(domain))

        self.login = login
        self.password = password
        self.history = HistoryPlugin()
        self.client = Client(self.wsdl, plugins=[self.history])
        self.factory = self.client.type_factory('http://www.cdiscount.com')

        if self.login is None or self.password is None:
            raise CdiscountApiConnectionError(
                'Please provide valid login and password'
            )

        self.token = self.get_token()
        self.header = {
            'Context': {
                'SiteID': 100,
                'CatalogID': 1
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

        # Instanciated sections.
        self.seller = Seller(self)
        self.offers = Offers(self)
        self.products = Products(self)
        self.orders = Orders(self)
        self.fulfillment = Fulfillment(self)
        self.relays = Relays(self)
        self.discussions = Discussions(self)
        self.webmail = WebMail(self)

    def get_token(self):
        response = requests.get(self.auth_url, auth=(self.login, self.password))
        return lxml.etree.XML(response.text).text

    def _analyze_history(self, attr, error_msg):
        if len(self.history._buffer) == 0:
            return error_msg

        envelope = getattr(self.history, attr)['envelope']
        return lxml.etree.tostring(envelope, pretty_print=True).decode('utf8')

    @property
    def last_request(self):
        """
        Return the last SOAP request
        """
        return self._analyze_history('last_sent', 'No request sent.')

    @property
    def last_response(self):
        """
        Return the last SOAP response
        """
        return self._analyze_history('last_received', 'No response received.')
