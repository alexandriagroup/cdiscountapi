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
from zeep.helpers import serialize_object

from cdiscountapi.exceptions import CdiscountApiConnectionError

from cdiscountapi.sections import (
    Seller,
    Offers,
    Products,
    Orders,
    Relays,
    Fulfillment,
    WebMail,
    Discussions,
)

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
import yaml


# CONSTANTS
DEFAULT_SITE_ID = 100
DEFAULT_CATALOG_ID = 1
DEFAULT_VERSION = "1.0"


class Connection(object):
    """A class to manage the interaction with the CdiscountMarketplace API

    :param str login: The login
    :param str password: The password
    :param bool preprod: Whether we use the preprod (True) or the production environment (False)
                         (default value: False)
    :param dict header_message: The header message
    :param str config: The path to a YAML config file

    Usage::

        api = Connection(login, password, preprod, header_message=header_message, config=config)

    """

    def __init__(self, login, password, preprod=False, header_message={}, config=""):
        self.preprod = preprod
        if self.preprod:
            domain = "preprod-cdiscount.com"
        else:
            domain = "cdiscount.com"

        self.wsdl = "https://wsvc.{0}/MarketplaceAPIService.svc?wsdl".format(domain)
        self.auth_url = (
            "https://sts.{0}/users/httpIssue.svc/"
            "?realm=https://wsvc.{0}/MarketplaceAPIService.svc".format(domain)
        )

        self.login = login
        self.password = password
        self.history = HistoryPlugin()
        self.client = Client(self.wsdl, plugins=[self.history])
        self.factory = self.client.type_factory("http://www.cdiscount.com")

        if self.login is None or self.password is None:
            raise CdiscountApiConnectionError("Please provide valid login and password")

        self.token = self.get_token()

        if header_message != {} and config != "":
            raise CdiscountApiConnectionError(
                "You should provide header_message or config. Not both."
            )

        if header_message:
            self.header = self.create_header_message(header_message)
        elif config:
            config_path = Path(config)
            if config_path.exists():
                conf = yaml.load(config_path.read_text(), Loader=yaml.FullLoader)
                self.header = self.create_header_message(conf)
            else:
                raise CdiscountApiConnectionError(
                    "Can't find the configuration file {}".format(config)
                )
        else:
            raise CdiscountApiConnectionError(
                "You must provide header_message or config."
            )

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

        envelope = getattr(self.history, attr)["envelope"]
        return lxml.etree.tostring(envelope, pretty_print=True).decode("utf8")

    @property
    def last_request(self):
        """
        Return the last SOAP request
        """
        return self._analyze_history("last_sent", "No request sent.")

    @property
    def last_response(self):
        """
        Return the last SOAP response
        """
        return self._analyze_history("last_received", "No response received.")

    def create_header_message(self, data):
        messages_factory = self.client.type_factory(
            "http://schemas.datacontract.org/2004/07/"
            "Cdiscount.Framework.Core.Communication.Messages"
        )

        # Set default values if they are not provided
        if "Context" in data:
            data["Context"].setdefault("SiteID", DEFAULT_SITE_ID)
            data["Context"].setdefault("CatalogID", DEFAULT_CATALOG_ID)
        else:
            data["Context"] = {
                "SiteID": DEFAULT_SITE_ID,
                "CatalogID": DEFAULT_CATALOG_ID,
            }

        if "Security" in data:
            data["Security"].setdefault("TokenId", self.token)
        else:
            data["Security"] = {"UserName": "", "TokenId": self.token}

        if "Version" not in data:
            data["Version"] = DEFAULT_VERSION

        return serialize_object(messages_factory.HeaderMessage(**data), dict)
