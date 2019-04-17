# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.fulfillment
    ---------------------------------

    Handles the supply order fulfillment.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object


class Fulfillment(object):
    """
    Allows to manage the fulfillment of the supply orders.

    Operations are included in the Fulfillment API section
    (https://dev.cdiscount.com/marketplace/?page_id=2222)
    """

    def __init__(self, api):
        self.api = api

    def submit_fulfillment_supply_order(self, request):
        response = self.api.client.service.SubmitFulfilmentSupplyOrder(
            headerMessage=self.api.header,
            request=request
        )
        return serialize_object(response, dict)

    def submit_fulfillment_on_demand_supply_order(self, order_list):
        """
        :param order_list: list of dict as
        [{'OrderReference': 1703182124BNXCO,
        'ProductEan': 2009854780777}]
        :return:
        """
        response = self.api.client.service.SubmitFulfilmentOnDemandSupplyOrder(
            headerMessage=self.api.header,
            request={'OrderLineList': order_list}
        )
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

    def get_fulfillment_delivery_document(self, deposit_id):
        """
        :param deposit_id: Unique identification number of the supply order request
        :type deposit_id: int
        :return: data for printing PDF documents, in the form of a Base64-encoded string.
        """
        response = self.api.client.service.GetFulfilmentDeliveryDocument(
            headerMessage=self.api.header,
            request={'DepositId': deposit_id}
        )
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

    def get_external_order_status(self, **request):
        response = self.api.client.service.GetExternalOrderStatus(
            headerMessage=self.api.header,
            request={
                'Corporation': request.get('Corporation'),
                'CustomerOrderNumber': request.get('CustomerOrderNumber')
            }
        )
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)
