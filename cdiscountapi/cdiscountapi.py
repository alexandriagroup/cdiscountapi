
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

    def get_offer_list(self, **filters):
        """
        To search offers.
        :param filters: filters (ex: OfferPoolId, SKU)
        :type filters: dict
        :return: offers answering the search criterion
        :rtype: dict
        """
        offer_filter = self.api.factory.OfferFilter(**filters)
        response = self.api.client.service.GetOfferList(
            headerMessage=self.api.header,
            offerFilter=offer_filter,
        )
        return helpers.serialize_object(response, dict)

    def get_offer_list_paginated(self, **filters):
        """
        Recovery of the offers page by page.
        :param filters: list of filters
        :type filters: dict
        :return: offers answering the search criterion
        :rtype: dict
        """
        offer_filter = self.api.factory.OfferFilterPaginated(**filters)
        response = self.api.client.service.GetOfferListPaginated(
            headerMessage=self.api.header,
            offerFilter=offer_filter,
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

    def get_offer_package_submission_result(self, package_id):
        """
        This operation makes it possible to know the progress report of the offers import.

        :return: Offer report logs
        :rtype: dict
        """
        package = self.api.factory.PackageFilter(package_id)
        response = self.api.client.service.GetOfferPackageSubmissionResult(
            headerMessage=self.api.header,
            offerPackageFilter=package,
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

    def get_product_list(self, category_code):
        """
        Search products in the reference frame
        :param category_code: code to filter products by category
        :type category_code: str
        :return: products corresponding to research
        :rtype: dict
        """
        filters = self.api.factory.ProductFilter(category_code)

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

    def get_product_package_product_matching_file_data(self, package_id):
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
                productPackageFilter={'PackageID': package_id}
            )
            return helpers.serialize_object(response, dict)

    def get_product_list_by_identifier(self, ean_list=[]):
        """
        Obtain details for a list of products
        :param ean_list: list of EAN to filter
        :type ean_list: list
        :return: complete list of products
        :rtype: dict
        """
        request = {'IdentifierType': 'EAN', 'ValueList': ean_list}
        response = self.api.client.service.GetProductListByIdentifier(
            headerMessage=self.api.header,
            identifierRequest=request
        )
        return helpers.serialize_object(response, dict)


class Orders(object):

    def __init__(self, api):
        self.api = api

    def get_order_list(self, **order_filter):
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
        order_filter = self.api.factory.OrderFilter(**order_filter)
        response = self.api.client.service.GetOrderList(
            headerMessage=self.api.header,
            orderFilter=order_filter,
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
    def validate_order_list(self, **validate_order_list_message):
        """
        Validate a list of orders

        :param validate_order_list_message: The information about the orders to
        validate.

        There are two ways to create `validate_order_list_message`:

        1. you can build the dictionary by yourself:

        Example:
        >>> api.validate_order_list(
            OrderList= {'ValidateOrder':
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
                        ]}
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

        >>> api.orders.validate_order_list_message(**validate_order_list_message)
        """
        validate_order_list_message = self.api.factory.ValidateOrderListMessage(
            **validate_order_list_message
        )
        response = self.api.client.service.ValidateOrderList(
            headerMessage=self.api.header,
            validateOrderListMessage=validate_order_list_message
        )
        return helpers.serialize_object(response, dict)

    def create_refund_voucher(self, **request):
        """
        This method still allows refunding lines of an order whose state is
        "ShippedBySeller".

        An additional feature allows to make a commercial gesture on an order
        MKPCDS before and after shipping and on an order MKPFBC after shipping.
        """
        request = self.api.factory.SellerRefundRequest(**request)
        response = self.api.client.service.CreateRefundVoucher(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)

    def manage_parcel(self, parcel_actions_list=None, scopus_id=None):
        """
        Ask for investigation or ask for delivery certification.

        :param parcel_actions_list: The keywords from

        >>> api.manage_parcel(ParcelInfos=[
            {'ManageParcel': manage_parcel, 'ParcelNumber': parcel_number, 'Sku': sku},
            ...
             ],
             scopus_id=scopus_id)

        where manage_parcel is either 'AskingForInvestigation' or
        'AskingForDeliveryCertification'.

        """
        # Handle properly the case where no information is provided for
        # parcel_actions_list
        if parcel_actions_list is not None:
            new_parcel_actions_list = []
            for parcel_infos in parcel_actions_list:
                new_parcel_infos = self.api.factory.ParcelInfos(parcel_infos)
                if not isinstance(new_parcel_infos.ManageParcel, list):
                    new_parcel_infos.ManageParcel = [new_parcel_infos.ManageParcel]
                new_parcel_actions_list.append(new_parcel_infos)
        else:
            new_parcel_actions_list = None

        manage_parcel_request = self.api.factory.ManageParcelRequest(
            ParcelActionsList=new_parcel_actions_list,
            ScopusId=scopus_id
        )

        response = self.api.client.service.ManageParcel(
            headerMessage=self.api.header,
            manageParcelRequest=manage_parcel_request
        )
        return helpers.serialize_object(response, dict)


class Fulfillment(object):

    def __init__(self, api):
        self.api = api

    def submit_fulfillment_supply_order(self, product_list):
        """
        :param request: list of dict as:
            [
                {
                "ExternalSupplyOrderId": int,
                "ProductEan": str,
                "Quantity": int,
                "SellerProductReference": int,
                "Warehouse": str,
                "WarehouseReceptionMinDate": date
                }
            ]
        :return:
        """
        for prod in product_list:
            for key in prod:
                check_element(key, self.api.factory.FulfilmentProductDescription)

        # req is based on arr keys.
        req = self.api.factory.FulfilmentSupplyOrderRequest
        # arr is composed by desc key.
        arr = self.api.factory.ArrayOfFulfilmentProductDescription

        request = req([arr(x) for x in product_list])
        response = self.api.client.service.SubmitFulfilmentSupplyOrder(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)

    def submit_fulfillment_on_demand_supply_order(self, order_list):
        """
        :param order_list: list of dict as
        [{'OrderReference': '1703182124BNXCO',
        'ProductEan': '2009854780777'}]
        :return:
        """
        response = self.api.client.service.SubmitFulfilmentOnDemandSupplyOrder(
            headerMessage=self.api.header,
            request={
                'OrderLineList': {
                    'FulfilmentOrderLineRequest': order_list
                }
            }
        )
        return helpers.serialize_object(response, dict)

    def get_fulfillment_supply_order_report_list(self, **request):
        """
        To search supply order reports.
        :param request:
            'BeginCreationDate': date,
            'DepositIdList': int list,
            'EndCreationDate': date,
            'PageNumber': int,
            'PageSize': int
        :return:supply order reports
        """
        supply_order_report_request = self.api.factory.SupplyOrderReportRequest(**request)
        response = self.api.client.service.GetFulfilmentSupplyOrderReportList(
            headerMessage=self.api.header,
            request=supply_order_report_request
        )
        return helpers.serialize_object(response, dict)

    def get_fulfillment_delivery_document(self, deposit_id):
        """
        :param deposit_id: Unique identification number of the supply order request
        :type deposit_id: int
        :return: data for printing PDF documents, in the form of a Base64-encoded string.
        """
        request = self.api.factory.FulfilmentDeliveryDocumentRequest(deposit_id)
        response = self.api.client.service.GetFulfilmentDeliveryDocument(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)

    def get_fulfillment_supply_order(self, **request):
        """
        :param request:
            'BeginModificationDate': date,
            'EndModificationDate': date,
            'PageNumber': int,
            'PageSize': int,
            'SupplyOrderNumberList': string list
        :return: supply orders
        """

        response = self.api.client.service.GetFulfilmentSupplyOrder(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)

    def submit_fulfillment_activation(self, request):
        """
        To ask for products activation (or deactivation)
        :param request:
            'ProductList': ProductActivationData list
        :return: deposit id
        """
        response = self.api.client.service.SubmitFulfilmentActivation(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)

    def get_fulfillment_activation_report_list(self, **request):
        """
        :param request:
            'BeginDate': date,
            'DepositIdList': int list,
            'EndDate': date
        """
        activation_report_request = self.api.factory.FulfilmentActivationReportRequest(**request)
        response = self.api.client.service.GetFulfilmentActivationReportList(
            headerMessage=self.api.header,
            request=activation_report_request
        )
        return helpers.serialize_object(response, dict)

    def get_fulfillment_order_list_to_supply(self, **request):
        """
        :param request:
            'OrderReference': str,
            'ProductEan': str,
            'Warehouse': str
        :return:
        """
        references = self.api.factory.FulfilmentOnDemandOrderLineFilter(**request)
        response = self.api.client.service.GetFulfilmentActivationReportList(
            headerMessage=self.api.header,
            request=references
        )
        return helpers.serialize_object(response, dict)

    def submit_offer_state_action(self, **request):
        """
        To set an offer online or offline
        :param request:
            'Action': 'Publish' or 'Unpublish'
            'SellerProductId': str
        :return:
        """
        seller_action = self.api.factory.OfferStateActionRequest(**request)
        response = self.api.client.service.SubmitOfferStateAction(
            headerMessage=self.api.header,
            offerStateRequest=seller_action
        )
        return helpers.serialize_object(response, dict)

    def create_external_order(self, order):
        """
        create an order from another marketplace.
        :param order: dict as {
                    'Comments': str,
                    'Corporation': str (ex:FNAC),
                    'Customer': customer info dict,
                    'CustomerOrderNumber': str,
                    'OrderDate': date,
                    'OrderLineList': {
                        'ExternalOrderLine': {
                            'ProductEan': str,
                            'ProductReference': str,
                            'Quantity': int
                        }
                    },
                    'ShippingMode': str,

        :return:
        """
        response = self.api.client.service.CreateExternalOrder(
            headerMessage=self.api.header,
            request={'Order': order}
        )
        return helpers.serialize_object(response, dict)

    def get_external_order_status(self, **request):
        response = self.api.client.service.GetExternalOrderStatus(
            headerMessage=self.api.header,
            request={
                'Corporation': request.get('Corporation'),
                'CustomerOrderNumber': request.get('CustomerOrderNumber')
            }
        )
        return helpers.serialize_object(response, dict)

    def get_product_stock_list(self, **request):
        """

        :param request:
            "BarCodeList": str list
            "FulfilmentReferencement"
        :return:
        """
        response = self.api.client.service.GetProductStockList(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)


class Relays(object):

    def __init__(self, api):
        self.api = api

    def get_parcel_shop_list(self):
        response = self.api.client.service.GetParcelShopList(
            headerMessage=self.api.header,
        )
        return helpers.serialize_object(response, dict)

    def submit_relays_file(self, **relays_file_request):
        """
        Send information about relays in a file

        Example
        >>> response = api.relays.submit_relays_file(
                relays_file_request=RelaysFileURI=relays_file_uri
            )

        where relays_file_uri is the URI to a XLSX file

        :type relays_file_request: dict
        :param relays_file_request: A dictionary pointing to a XLSX file
        with information about relays

        :returns: The response with the RelaysFileId for the file.

        """
        relays_file_request = self.api.factory.RelaysFileIntegrationRequest(
            **relays_file_request
        )
        response = self.api.client.service.SubmitRelaysFile(
            headerMessage=self.api.header,
            relaysFileRequest=relays_file_request
        )
        return helpers.serialize_object(response, dict)

    def get_relays_file_submission_result(self, **relays_file_filter):
        """
        Get the state of progress of the relays file submission.

        Usage:
        >>> response = api.get_relays_file_submission_result(
        relays_file_filter={'RelaysFileId': relays_file_id}
        )

        where relays_file_id is the value of RelaysFileId returned by
        SubmitRelaysFile.

        :param relays_file_filter: The dictionary containing the ID referencing
        the relays file submitted.

        :returns: The response with the information about the integration of
        the relays specified.
        """
        relays_file_filter = self.api.factory.RelaysFileFilter(
            **relays_file_filter
        )
        response = self.api.client.service.GetRelaysFileSubmissionResult(
            headerMessage=self.api.header,
            relaysFileFilter=relays_file_filter
        )
        return helpers.serialize_object(response, dict)


class Discussions(object):
    """
    There are 3 ways to get discussions: discussions id, the discussions
    status, and all messages.

    Thanks to the discussion Id and the method GetDiscussionMailList you can
    get an encrypted mail address to reply to a question or a claim.  You can
    close a discussion list with the method CloseDiscussionList and the
    Discussion id, you cannot close a discussion without having answered
    Operations are included in the Discussions API section.
    (https://dev.cdiscount.com/marketplace/?page_id=148)
    """

    def __init__(self, api):
        self.api = api

    def get_order_claim_list(self, **order_claim_filter):
        """
        Return the list of order claims
        """
        order_claim_filter = self.api.factory.OrderClaimFilter(
            **order_claim_filter
        )
        response = self.api.client.service.GetOrderClaimList(
            headerMessage=self.api.header,
            orderClaimFilter=order_claim_filter
        )
        return helpers.serialize_object(response, dict)

    def get_offer_question_list(self, **offer_question_filter):
        """
        Return the list of questions about offers with the specified criteria

        :param offer_question_filter: The keywords for the filter
        `offerQuestionFilter`:

        - BeginCreationDate
        - BeginModificationDate
        - EndCreationDate
        - EndModificationDate
        - StatusList
        - ProductEANList
        - ProductSellerReferenceList

        Example:
        >>> response = api.get_offer_question_list(
            StatusList={'DiscussionStateFilter': 'Open'}
            )

        :returns: An OfferQuestionListMessage dictionary.

        """
        offer_question_filter = self.api.factory.OfferQuestionFilter(
            **offer_question_filter
        )
        response = self.api.client.service.GetOfferQuestionList(
            headerMessage=self.api.header,
            offerQuestionFilter=offer_question_filter
        )
        return helpers.serialize_object(response, dict)

    def get_order_question_list(self, **order_question_filter):
        """
        Return the list of questions about orders with the specified criteria

        :param order_question_filter: The keywords for the filter
        `orderQuestionFilter`:

        - BeginCreationDate
        - BeginModificationDate
        - EndCreationDate
        - EndModificationDate
        - StatusList
        - ProductEANList
        - ProductSellerReferenceList

        Example:
        >>> response = api.get_order_question_list(
            StatusList={'DiscussionStateFilter': 'Open'}
            )

        :returns: An OrderQuestionListMessage dictionary.

        """
        order_question_filter = self.api.factory.OrderQuestionFilter(
            **order_question_filter
        )
        response = self.api.client.service.GetOrderQuestionList(
            headerMessage=self.api.header,
            orderQuestionFilter=order_question_filter
        )
        return helpers.serialize_object(response, dict)

    def close_discussion_list(self, discussion_ids):
        """
        Close a discussion list

        :type discussion_ids: list
        :param discussion_ids: The list of discussion_ids to close

        Example:
        >>> response = api.discussions.close_discussion_list([31, 4, 159])
        """
        arrays_factory = self.api.client.type_factory(
            'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
        )
        close_discussion_request = self.api.factory.CloseDiscussionRequest(
            DiscussionIds=arrays_factory.ArrayOflong(discussion_ids)
        )
        response = self.api.client.service.CloseDiscussionList(
            headerMessage=self.api.header,
            closeDiscussionRequest=close_discussion_request
        )
        return helpers.serialize_object(response, dict)


class WebMail(object):
    """
    The WebMail API allows the seller to retrieve encrypted email address to
    contact a customer
    """

    def __init__(self, api):
        self.api = api

    def generate_discussion_mail_guid(self, scopus_id=None):
        """
        Obtain an encrypted mail address.

        This operation allows getting an encrypted mail address to contact a
        customer about an order.

        Usage:
        >>> response = api.generate_discussion_mail_guid(scopus_id)
        """
        response = self.api.client.service.GenerateDiscussionMailGuid(
            headerMessage=self.api.header,
            request={'ScopusId': scopus_id}
        )
        return helpers.serialize_object(response, dict)

    def get_discussion_mail_list(self, discussion_ids):
        """
        Obtain an encrypted mail address about a discussion.

        This operation allows getting an encrypted mail address to contact a
        customer about a discussion (claim, retraction, questions).

        Usage:
        >>> response = api.webmail.generate_discussion_mail_guid(discussion_ids)
        """
        arrays_factory = self.api.client.type_factory(
            'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
        )
        request = self.api.factory.GetDiscussionMailListRequest(
            DiscussionIds=arrays_factory.ArrayOflong(discussion_ids)
        )
        response = self.api.client.service.GetDiscussionMailList(
            headerMessage=self.api.header,
            request=request
        )
        return helpers.serialize_object(response, dict)


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
        self.fulfillment = Fulfillment(self)
        self.relays = Relays(self)
        self.discussions = Discussions(self)
        self.webmail = WebMail(self)

    def get_token(self):
        response = requests.get(self.auth_url, auth=(self.login, self.password))
        return lxml.etree.XML(response.text).text
