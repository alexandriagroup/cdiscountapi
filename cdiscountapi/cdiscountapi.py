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
    CdiscountApiOrderError, CdiscountApiConnectionError
)


# HELPER FUNCTIONS
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


def create_order_line_list(orders, order_number):
    """
    <OrderLineList>
        <ValidateOrderLine>
            <AcceptationState>AcceptedBySeller</AcceptationState>
            <ProductCondition>New</ProductCondition>
            <SellerProductId>CHI8003970895435</SellerProductId>
        </ValidateOrderLine>
        <ValidateOrderLine>
            <AcceptationState>AcceptedBySeller</AcceptationState>
            <ProductCondition>New</ProductCondition>
            <SellerProductId>DOD3592668078117</SellerProductId>
        </ValidateOrderLine>
    </OrderLineList>
    """
    selected_orders = [order for order in orders if order['OrderNumber'] == order_number]
    if selected_orders == 1:
        selected_order = selected_orders[0]
    else:
        raise CdiscountApiOrderError(
            "Can't find the order_number {0} in the orders {1}".format(
                order_number, orders)
        )


def create_order_line(order, seller_product_id, acceptation_state):
    """
    <AcceptationState>AcceptedBySeller</AcceptationState>
    <ProductCondition>New</ProductCondition>
    <SellerProductId>CHI8003970895435</SellerProductId>
    """
    items = [item for item in order['OrderLineList'] if
             item['SellerProductId'] == seller_product_id]

    if len(items) == 1:
        product_condition = items[0]['ProductCondition']
    else:
        raise ValueError(
            "Can't find the seller_product_id {0} in the order {1}".format(
                seller_product_id, order)
        )
    return {'AcceptationState': acceptation_state,
            'ProductCondition': product_condition,
            'SellerProductId': seller_product_id}


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
        :param filters: list of filters
        :type filters: str
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

    def get_product_list(self, category=None):
        """
        Search products in the reference frame
        :param category: category code to filter results
        :type category: str
        :return: products corresponding to research
        :rtype: dict
        """
        if category:
            response = self.api.client.service.GetProductList(
                headerMessage=self.api.header,
                productFilter={'CategoryCode': category}
            )
            return helpers.serialize_object(response, dict)
        else:
            return {
                'ErrorMessage': None,
                'OperationSuccess': True,
                'ErrorList': None,
                'SellerLogin': self.api.login,
                'TokenId': self.api.token,
                'ProductList': {'Product': []}
            }

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

    def get_all_model_list(self):
        """
        Model categories opened on marketplace.
        :return: models and mandatory model properties
        :rtype: dict
        """
        api_all = self.Connection('AllData', 'pa$$word')
        response = api_all.client.service.GetAllModelList(
            headerMessage=api_all.header,
        )
        return helpers.serialize_object(response, dict)

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

    def get_product_package_submission_result(self, package_id=None):
        """
        Progress status of a product import.
        :param package_id: package id to filter results
        :type package_id: str
        :return: partial or complete report of package integration
        :rtype: dict
        """
        if package_id:
            response = self.api.client.service.GetProductPackageSubmissionResult(
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
                    'NumberOfErrors': 0,
                    'PackageId': 0,
                    'PackageIntegrationStatus': None,
                    'ProductLogList': {'ProductReportLog': []}
            }

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

    # TODO Use for accept_orders
    def validate_order_list(self, data):
        response = self.api.client.service.ValidateOrderList(
            headerMessage=self.api.header,
            validateOrderListMessage=data
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
