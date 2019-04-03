# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria
from shutil import (
    copytree,
    make_archive,
    rmtree,
)
from tempfile import gettempdir

import lxml
import requests
from dicttoxml import dicttoxml
from zeep import (
    Client,
    helpers,
)


def generate_package_url(content_dict, url):
    """
    Generate and upload package and return the url
    :param content_dict: dict of products or offers as you can see on tests/samples/products/products_to_submit.json
    :param url: url to upload package
    :return: url to find it
    """
    # Create a temporary package.
    tempdir = gettempdir()

    # Generate package according to content type.
    if 'Product' in content_dict.keys():
        package = generate_product_package(tempdir, content_dict)
    elif 'Offer' in content_dict.keys():
        package = generate_offer_package(tempdir, content_dict)

    # Generate zip package.
    zip_package = make_archive(package, 'zip', package)

    # Upload package and get url to download it.
    package_url = upload_and_get_url(zip_package, url)

    # Remove temporary package.
    rmtree(tempdir + '/uploading_package')
    return package_url


def generate_package(package_type, tempdir, offer_dict):
    """
    Generate a zip package for the offers or the products

    :param package_type: 'offer' or 'product'
    :param tempdir:  directory to create temporary files
    :param offer_dict: offers as you can see on
    tests/samples/products/products_to_submit.json or
    tests/samples/offers/offers_to_submit.json
    """
    if package_type not in ('offer', 'product'):
        raise ValueError('package_type must be either "offer" or "product".')

    # Create path.
    path = f'{tempdir}/uploading_package'

    # Copy tree package.
    package = copytree(f'{package_type}_package', path)
    xml_filename = package_type.capitalize() + 's.xml'

    # Add Products.xml from product_dict.
    with open(f"{package}/Content/{xml_filename}", "wb") as f:
        f.write(dicttoxml(offer_dict))

    # Make a zip from package.
    zip_package = make_archive(path, 'zip', path)

    # # Remove unzipped package.
    # rmtree(path)
    return zip_package


def generate_product_package(tempdir, product_dict):
    """
    Generate a zip product package as cidscount wanted.
    :param tempdir: directory to create temporary files
    :param product_dict: products as you can see on tests/samples/products/products_to_submit.json
    :return: zip package
    """
    return generate_package('product', tempdir, product_dict)


def generate_offer_package(tempdir, offer_dict):
    """
    Generate a zip offers package as cidscount wanted.
    :param tempdir:  directory to create temporary files
    :param offer_dict: offers as you can see on tests/samples/offers/offers_to_submit.json
    :return: zip package
    """
    return generate_package('offer', tempdir, offer_dict)


# TODO find a way to upload package et get url
def upload_and_get_url(package, url):

    return url + package


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
        response = self.api.client.service.GetSellerIndicators(
            headerMessage=self.api.header
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

    def submit_offer_package(self, offers_dict, url):
        """
        To ask for the creation of offers.

        :param offers_dict: offers as you can see on tests/samples/offers/offers_to_submit.json
        :param url: url to upload offers package
        :return: the id of package or -1
        :rtype: int
        """
        # Get url.
        package_url = generate_package_url(offers_dict, url)

        # Create request attribute.
        offer_package = {'ZipFileFullPath': package_url}

        # Send request.
        response = self.api.client.service.SubmitOfferPackage(
            headerMessage=self.api.header,
            offerPackageRequest=offer_package,
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
        Know the categories of product which are accessible to them.
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

    def submit_product_package(self, products_dict, url):
        """
        To ask for the creation of products.

        :param products_dict: products as you can see on tests/samples/products/products_to_submit.json
        :param url: url to upload offers package
        :return: the id of package or -1
        :rtype: int
        """
        # get url.
        package_url = generate_package_url(products_dict, url)

        # Create request attribute.
        product_package = {'ZipFileFullPath': package_url}

        # Send request.
        response = self.api.client.service.SubmitProductPackage(
            headerMessage=self.api.header,
            productPackageRequest=product_package
        )
        return helpers.serialize_object(response, dict)

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

    def __init__(self, login, password, preprod=False):
        self.preprod = preprod
        if self.preprod:
            domain = 'preprod-cdiscount.com'
        else:
            domain = 'cdiscount.com'

        self.wsdl = 'https://wsvc.{0}/MarketplaceAPIService.svc'.format(domain)
        self.auth_url = ('https://sts.{0}/users/httpIssue.svc/'
                         '?realm=https://wsvc.{0}/MarketplaceAPIService.svc'.format(domain))

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
