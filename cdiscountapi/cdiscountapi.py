# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

from zeep import Client, helpers
import requests
import lxml


class Seller(object):
    """
    Seller section lets sellers retrieve information about their seller account
    and their performance indicator.
    """
    def __init__(self, api):
        self.api = api

    def get_seller_info(self):
        """
        This operation allows to obtain the information of the authenticated seller.
        :return: Information of the authenticated seller.
        :rtype: dict
        """
        response = self.api.client.service.GetSellerInformation(
            headerMessage=self.api.header
        )
        return helpers.serialize_object(response, dict)

    def get_seller_indicators(self):
        """
        This operation makes it possible to obtain performance indicators of
        the specified seller.
        :return: a dict with the data of the user
        :rtype: dict
        """
        response = self.client.service.GetSellerIndicators(
            headerMessage=self.header
        )
        return helpers.serialize_object(response, dict)


class Offers(object):
    """
    Offers section lets sellers retrieve informations about their offers.
    Operations are included in the Products API section
    """
    def __init__(self, api):
        self.api = api

    def get_offer_list(self, filters=None):
        """
        To search offers.
        :param filters: list of filters
        :return: offers answering the search criterion
        :rtype: dict
        """
        response = self.api.client.service.GetOfferList(
            headerMessage=self.api.header,
            offerFilter=filters,
        )
        return helpers.serialize_object(response, dict)

    def get_offer_list_paginated(self, filters):
        """
        Recovery of the offers page by page.
        :param filters: list of filters
        :return: offers answering the search criterion
        :rtype: dict
        """
        response = self.api.client.service.GetOfferListPaginated(
            headerMessage=self.api.header,
            offerFilter=filters,
        )
        return helpers.serialize_object(response, dict)

    def submit_offer_package(self, offers=None):
        """
        To import offers.
        :return: report message
        :rtype: dict
        """
        response = self.api.client.service.SubmitOfferPackage(
            headerMessage=self.api.header,
            offerPackageRequest=offers,
        )
        return helpers.serialize_object(response, dict)

    def get_offer_package_submission_result(self, packages):
        """
        This operation makes it possible to know the progress report of the offers import.

        :return: Offer report logs
        :rtype: dict
        """
        response = self.api.client.service.GetOfferPackageSubmissionResult(
            headerMessage=self.api.header,
            packageFilter=packages,
        )
        return helpers.serialize_object(response, dict)


class Products(object):

    def __init__(self, api):
        self.api = api

    def get_allowed_category_tree(self):
        """
        This operation allows the user API to know the categories of product which are accessible to her.
        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        :rtype: dict
        """
        response = self.api.client.service.GetAllowedCategoryTree(
            headerMessage=self.api.header
        )
        return helpers.serialize_object(response, dict)

    def get_all_allowed_category_tree(self):
        pass

    def get_product_list(self):
        pass

    def get_model_list(self):
        pass

    def get_all_model_list(self):
        pass

    def get_brand_list(self):
        pass

    def submit_product_package(self):
        pass

    def get_product_package_submission_result(self):
        pass

    def get_product_package_product_matching_file_data(self):
        pass

    def get_product_list_by_identifier(self):
        pass


class Orders(object):

    def __init__(self, api):
        self.api = api

    def get_order_list(self):
        pass

    def get_global_configuration(self):
        pass

    def validate_order_list(self):
        pass

    def create_refund_voucher(self):
        pass


class Fulfilment(object):

    def __init__(self, api):
        self.api = api

    def submit_fulfilmen_supply_order(self):
        pass

    def get_fulfilment_supply_order_report_list(self):
        pass

    def get_fulfilment_order_list_to_supply(self):
        pass

    def submit_fulfilment_on_demand_supply_order(self):
        pass

    def get_fulfilment_supply_order(self):
        pass

    def submit_offer_state_action(self):
        pass

    def submit_fulfilment_activation(self):
        pass

    def get_fulfilment_activation_report_list(self):
        pass

    def get_fulfilment_delivery_document(self):
        pass


class Relays(object):

    def __init__(self, api):
        self.api = api

    def get_parcel_shop_list(self):
        pass

    def submit_relays_file(self):
        pass

    def get_relays_file_submission_result(self):
        pass


class Discussions(object):

    def __init__(self, api):
        self.api = api

    def get_order_claim_list(self):
        pass

    def get_offer_question_list(self):
        pass

    def get_order_question_list(self):
        pass

    def close_discussion_list(self):
        pass


class WebMail(object):

    def __init__(self, api):
        self.api = api

    def generate_mail_discussion_guid(self):
        pass

    def get_discussion_mail_list(self):
        pass


class Connection(object):
    """A class to manage the interaction with the CdiscountMarketplace API"""

    wsdl = 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl'
    auth_url = ('https://sts.cdiscount.com/users/httpIssue.svc/'
                '?realm=https://wsvc.cdiscount.com/MarketplaceAPIService.svc')

    def __init__(self, login, password):
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
        # Instanciated sections.
        self.seller = Seller(self)
        self.offers = Offers(self)
        self.products = Products(self)
        self.orders = Orders(self)
        self.fulfilment = Fulfilment(self)
        self.relays = Relays(self)
        self.discussions = Discussions(self)
        self.webmail = WebMail(self)

    def get_token(self):
        response = requests.get(self.auth_url, auth=(self.login, self.password))
        return lxml.etree.XML(response.text).text
