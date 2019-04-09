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

from cdiscountapi.exceptions import (
    CdiscountApiConnectionError,
    CdiscountApiOrderError,
)


def check_element(element_name, dynamic_type):
    """
    Raise an exception if the is not in the dynamic_type

    Example
    >>> check_element('CarrierName', api.factory.ValidateOrder)
    """
    valid_elements = [x[0] for x in dynamic_type.elements]
    if element_name not in valid_elements:
        raise ValueError('{0} is not a valid element of {1}.'
                         ' Valid elements are {2}'.format(
                             element_name, dynamic_type.name, valid_elements)
                         )


# HELPER FUNCTIONS.
def generate_package_url(content_dict, url):
    """
    Generate and upload package and return the url
    :param content_dict: products or offers as you can see on tests/samples/products/products_to_submit.json
    :type content_dict: dict
    :param url: url to upload package
    :type url: str
    :return: url to find it
    :rtype: str
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
    :type package_type: str
    :param tempdir:  directory to create temporary files
    :type tempdir: str
    :param offer_dict: offers as you can see on
    tests/samples/products/products_to_submit.json or
    tests/samples/offers/offers_to_submit.json
    :type offer_dict: dict
    :rtype: str
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

    # Remove unzipped package.
    return zip_package


def generate_product_package(tempdir, product_dict):
    """
    Generate a zip product package as cdiscount wanted.
    :param tempdir: directory to create temporary files
    :type tempdir: str
    :param product_dict: products as you can see on tests/samples/products/products_to_submit.json
    :type product_dict: dict
    :return: zip package
    :rtype: str
    """
    return generate_package('product', tempdir, product_dict)


def generate_offer_package(tempdir, offer_dict):
    """
    Generate a zip offers package as cdiscount wanted.
    :param tempdir:  directory to create temporary files
    :type tempdir: str
    :param offer_dict: offers as you can see on tests/samples/offers/offers_to_submit.json
    :type offer_dict: dict
    :return: zip package
    :rtype: str
    """
    return generate_package('offer', tempdir, offer_dict)


# TODO find a way to upload package et get url
def upload_and_get_url(package, url):
    """
    Upload package and get url to download it.
    :param package: way to find zip package
    :type package: str
    :param url: where to upload zip package
    :type url: str
    :return: where to download zip package
    :rtype: str
    """

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
        Seller Information.
        :return: Information of the authenticated seller.
        :rtype: dict
        """
        response = self.api.client.service.GetSellerInformation(
            headerMessage=self.api.header
        )
        return helpers.serialize_object(response, dict)

    def get_seller_indicators(self):
        """
        Seller performance indicators.
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

    def get_offer_list(self, filters={}):
        """
        To search offers.
        :param filters: filters (ex: OfferPoolId, SKU)
        :type filters: dict
        :return: offers answering the search criterion
        :rtype: dict
        """
        response = self.api.client.service.GetOfferList(
            headerMessage=self.api.header,
            offerFilter=filters,
        )
        return helpers.serialize_object(response, dict)

    def get_offer_list_paginated(self, filters={}):
        """
        Recovery of the offers page by page.
        :param filters: list of filters
        :type filters: dict
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
        :type offers_dict: dict
        :param url: url to upload offers package
        :type url: str
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

    def get_offer_package_submission_result(self, packages={}):
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
        Categories which are accessible to the seller.
        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        :rtype: dict
        """
        response = self.api.client.service.GetAllowedCategoryTree(
            headerMessage=self.api.header
        )
        return helpers.serialize_object(response, dict)

    def get_all_allowed_category_tree(self):
        """
        All categories.
        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        :rtype: dict
        """
        api_all = Connection('AllData', 'pa$$word')
        response = api_all.client.service.GetAllAllowedCategoryTree(
            headerMessage=api_all.header
        )
        return helpers.serialize_object(response, dict)

    # TODO find why it doesn't work.
    def get_product_list(self, filters={}):
        """
        Search products in the reference frame
        :param filters: (ex:category code)
        :type filters: dict
        :return: products corresponding to research
        :rtype: dict
        """
        response = self.api.client.service.GetProductList(
            headerMessage=self.api.header,
            productFilter=filters,
        )
        return helpers.serialize_object(response, dict)

    def get_model_list(self, category=None):
        """
        Model categories allocated to the seller.
        :param category: category code to filter results
        :type category: str
        :return: models and mandatory model properties
        :rtype: dict
        """
        response = self.api.client.service.GetModelList(
            headerMessage=self.api.header,
            modelFilter=category
        )
        return helpers.serialize_object(response, dict)

    # TODO find a way to call it.
    def get_all_model_list(self):
        """
        Model categories opened on marketplace.
        :return: models and mandatory model properties
        :rtype: dict
        """
        # api_all = Connection('AllData', 'pa$$word')
        # response = api_all.client.service.GetAllModelList(
        #     headerMessage=api_all.header,
        # )
        # return helpers.serialize_object(response, dict)
        pass

    def get_brand_list(self):
        """
        Complete list of the brands
        :return: all brands
        :rtype: dict
        """
        response = self.api.client.service.GetBrandList(
            headerMessage=self.api.header,
        )
        return helpers.serialize_object(response, dict)

    def submit_product_package(self, products_dict, url):
        """
        To ask for the creation of products.

        :param products_dict: products as you can see on tests/samples/products/products_to_submit.json
        :type products_dict: dict
        :param url: url to upload offers package
        :type url: str
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

    # TODO find why it doesn't work.
    def get_product_package_submission_result(self, filters={}):
        """
        Progress status of a product import.
        :param filters: (ex: package id)
        :type filters: dict
        :return: partial or complete report of package integration
        :rtype: dict
        """
        response = self.api.client.service.GetProductPackageSubmissionResult(
            headerMessage=self.api.header,
            productPackageFilter=filters
        )
        return helpers.serialize_object(response, dict)

    def get_product_package_product_matching_file_data(self, package_id=None):
        """
        Information of the created products.
        :param package_id: package id to filter results
        :type package_id: str
        :return: information of the created products
        :rtype: dict
        """
        if package_id:
            response = self.api.client.service.GetProductPackageProductMatchingFileData(
                headerMessage=self.api.header,
                productPackageFilter=package_id
            )
            return helpers.serialize_object(response, dict)
        else:
            return {'ErrorMessage': None,
                    'OperationSuccess': True,
                    'ErrorList': None,
                    'SellerLogin': self.api.login,
                    'TokenId': self.api.token,
                    'PackageId': 0,
                    'ProductMatchingList': None}

    def get_product_list_by_identifier(self, ean_list=[]):
        """
        Obtain details for a list of products
        :param ean_list: list of EAN to filter
        :type ean_list: list
        :return: complete list of products
        :rtype: dict
        """
        if ean_list:
            response = self.api.client.service.GetProductPackageProductMatchingFileData(
                headerMessage=self.api.header,
                IdentifierRequest=ean_list
            )
            return helpers.serialize_object(response, dict)
        else:
            return {'ErrorMessage': None,
                    'OperationSuccess': True,
                    'ErrorList': None,
                    'SellerLogin': self.api.login,
                    'TokenId': self.api.token,
                    'NumberOfErrors': 0,
                    'ProductListByIdentifier': {
                        'ProductByIdentifier': []
                    }
            }


class Orders(object):

    def __init__(self, api):
        self.api = api

    def get_order_list(self, filters={}):
        """
        To search orders.

        This operation makes it possible to seek orders according to the
        following criteria:

        - The order state:
            - CancelledByCustomer
            - WaitingForSellerAcceptation
            - AcceptedBySeller
            - PaymentInProgress
            - WaitingForShipmentAcceptation
            - Shipped
            - RefusedBySeller
            - AutomaticCancellation (ex: no answer from the seller)
            - PaymentRefused
            - ShipmentRefusedBySeller
            - Waiting for Fianet validation "A valider Fianet" (None)
            - Validated Fianet
            - RefusedNoShipment
            - AvailableOnStore
            - NonPickedUpByCustomer
            - PickedUp
            - Filled

        - Recovery or not of the products of the order

        - Filter on date:
            - BeginCreationDate
            - EndCreationDate
            - BeginModificationDate
            - EndModificationDate

        - Order number list Liste (OrderReferenceList) Warning, this filter
        cannot be combined with others. If there is an order list, the other
        filters are unaccounted.

        - Filter on website thanks to the corporationCode.

        - Filter by Order Type:
            - MKPFBC Orders
            - EXTFBC Orders
            - FBC Orders(Isfulfillment)

        - PartnerOrderRef filter from 1 to N external order (if it's a multiple
        search, separate PartnerOrderRefs by semicolon).
        PartnerOrderRef is the seller's reference

        - Recovery or not of the parcels of the order
        """
        response = self.api.client.service.GetOrderList(
            headerMessage=self.api.header,
            orderFilter=filters,
        )
        return helpers.serialize_object(response, dict)

    def get_global_configuration(self):
        """
        Get cdiscount settings. This method allows to get a list of several
        settings:
        - Carrier list
        """
        response = self.api.client.service.GetGlobalConfiguration(
            headerMessage=self.api.header,
        )
        return helpers.serialize_object(response, dict)

    def _prepare_validation(self, data):
        """
        Return the validation data for an order.

        :type data: dict
        :param data: The information about the order to validate. (cf
        `Seller.prepare_validations`)
        """
        data = data.copy()

        # Check elements in ValidateOrder
        for element_name in data.keys():
            check_element(element_name, self.api.factory.ValidateOrder)

        # check elements ValidateOrderLine
        for i, validate_order_line in enumerate(data['OrderLineList']):
            for element_name in validate_order_line.keys():
                check_element(element_name, self.api.factory.ValidateOrderLine)

        data['OrderLineList'] = {
            'ValidateOrderLine': [x for x in data.pop('OrderLineList')]
        }
        return helpers.serialize_object(
            self.api.factory.ValidateOrder(**data), dict
        )

    def prepare_validations(self, data):
        """
        Return the dictionary used to validate the orders in
        `Orders.validate_order_list`

        This method tries to simplify the creation of the data necessary to
        validate the orders by letting the user provide a more intuitive data
        structure than the one required for the request.

        :type data: list
        :param data: The validation data for the orders. A list of dictionaries
        with the following structure:

        {
            'CarrierName': carrier_name,
            'OrderNumber': order_number,
            'OrderState': order_state,
            'TrackingNumber': tracking_number,
            'TrackingUrl': tracking_url,
            'OrderLineList': [
                {
                    'AcceptationState': acceptation_state,
                    'ProductCondition': product_condition,
                    'SellerProductId': seller_product_id,
                    'TypeOfReturn': type_of_return
                },
                ...
            ]
        }

        :rtype dict:
        :returns: The `validate_order_list_message` dictionary created with
        `data`
        """
        return {
            'OrderList': {
                'ValidateOrder': [self._prepare_validation(x) for x in data]
            }
        }

    # TODO Use for accept_orders
    def validate_order_list(self, validate_order_list_message):
        """
        Validate a list of orders

        :param validate_order_list_message: The information about the orders to
        validate.

        There are two ways to create `validate_order_list_message`:

        1. you can build the dictionary by yourself:

        Example:
        >>> api.validate_order_list(
            {'OrderList':
                {'ValidateOrder':
                    [{'CarrierName': carrier_name,
                      'OrderNumber': order_number,
                      'OrderState': order_state,
                      'TrackingNumber': tracking_number,
                      'TrackingUrl': tracking_url,
                      'OrderLineList': {
                          'ValidateOrderLine': [
                          {'AcceptationState': 'acceptation_state',
                           'ProductCondition': product_condition,
                           'SellerProductId': seller_product_id,
                           'TypeOfReturn': type_of_return},
                          ...
                          ]},
                    },
                    ...
                    ]}}
        )

        2. you can use `Orders.prepare_validations`

        Example:
        >>> validate_order_list_message = api.orders.prepare_validations(
                    [{'CarrierName': carrier_name,
                      'OrderNumber': order_number,
                      'OrderState': order_state,
                      'TrackingNumber': tracking_number,
                      'TrackingUrl': tracking_url,
                      'OrderLineList': [
                          {'AcceptationState': 'acceptation_state',
                           'ProductCondition': product_condition,
                           'SellerProductId': seller_product_id,
                           'TypeOfReturn': type_of_return},
                          ...
                          ]},
                        ...]

        >>> api.orders.validate_order_list_message(validate_order_list_message)
        """
        response = self.api.client.service.ValidateOrderList(
            headerMessage=self.api.header,
            validateOrderListMessage=validate_order_list_message
        )
        return helpers.serialize_object(response, dict)

    def create_refund_voucher(self):
        pass


class Fulfilment(object):

    def __init__(self, api):
        self.api = api

    def submit_fulfilment_supply_order(self):
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

        self.wsdl = 'https://wsvc.{0}/MarketplaceAPIService.svc?wsdl'.format(domain)
        self.auth_url = ('https://sts.{0}/users/httpIssue.svc/'
                         '?realm=https://wsvc.{0}/MarketplaceAPIService.svc'.format(domain))

        self.login = login
        self.password = password
        self.client = Client(self.wsdl)
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
        self.fulfilment = Fulfilment(self)
        self.relays = Relays(self)
        self.discussions = Discussions(self)
        self.webmail = WebMail(self)

    def get_token(self):
        response = requests.get(self.auth_url, auth=(self.login, self.password))
        return lxml.etree.XML(response.text).text
