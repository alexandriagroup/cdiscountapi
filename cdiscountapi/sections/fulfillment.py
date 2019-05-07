# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.fulfillment
    ---------------------------------

    Handles the supply order fulfillment.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from .base import BaseSection
from ..helpers import auto_refresh_token


class Fulfillment(BaseSection):
    """
    Allows to manage the fulfillment of the supply orders.

    Operations are included in the Fulfillment API section
    (https://dev.cdiscount.com/marketplace/?page_id=2222)
    """
    @auto_refresh_token
    def submit_fulfillment_supply_order(self, request):
        response = self.api.client.service.SubmitFulfilmentSupplyOrder(
            headerMessage=self.api.header,
            request=request
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def submit_fulfillment_on_demand_supply_order(self, order_list):
        """
        :param order_list: list of dict as:
            [{'OrderReference': 1703182124BNXCO,'ProductEan': 2009854780777}]

        """
        response = self.api.client.service.SubmitFulfilmentOnDemandSupplyOrder(
            headerMessage=self.api.header,
            request={'OrderLineList': order_list}
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_fulfillment_supply_order_report_list(self, **request):
        """
        To search supply order reports.

        :param int PageSize: [mandatory]
        :param date BeginCreationDate:
        :param date EndCreationDate:
        :param int PageNumber:
        :param list DepositIdList: list of ints

        Examples::

            response = api.fulfillment.get_fulfillment_supply_order_report_list(
                PageSize=10,
                BeginCreationDate=datetime.datetime(2019, 1, 1),
                EndCreationDate=datetime.datetime(2019, 1, 2),
            )

            response = api.fulfillment.get_fulfillment_supply_order_report_list(
                PageSize=10, DepositIdList=[1, 2, 3]
            )

        :return: supply order reports
        """
        request = self.update_with_valid_array_type(request, {'DepositIdList': 'int'})

        supply_order_report_request = self.api.factory.SupplyOrderReportRequest(**request)
        response = self.api.client.service.GetFulfilmentSupplyOrderReportList(
            headerMessage=self.api.header,
            request=supply_order_report_request
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_fulfillment_delivery_document(self, deposit_id):
        """
        To get pdf document data for a supply order delivery, in the form of a Base64-encoded string.

        :param int deposit_id: Unique identification number of the supply order request

        Usage::

            response = api.fulfillment.get_fulfillment_delivery_document(233575)

        :return: data for printing PDF documents, in the form of a Base64-encoded string.
        """
        response = self.api.client.service.GetFulfilmentDeliveryDocument(
            headerMessage=self.api.header,
            request={'DepositId': deposit_id}
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_fulfillment_supply_order(self, **request):
        """
        :param int PageSize: [mandatory]
        :param date BeginModificationDate:
        :param date EndModificationDate:
        :param int PageNumber:
        :param list SupplyOrderNumberList: list of strings

        Examples::

            response = api.fulfillment.get_fulfillment_supply_order_report_list(
                PageSize=10,
                BeginCreationDate=datetime.datetime(2019, 1, 1),
                EndCreationDate=datetime.datetime(2019, 1, 2),
            )

            response = api.fulfillment.get_fulfillment_supply_order_report_list(
                PageSize=10,
                SupplyOrderNumberList=['X', 'Y', 'Z']
            )

        :return: supply orders
        """
        request = self.update_with_valid_array_type(request, {'SupplyOrderNumberList': 'string'})

        supply_order_report_request = self.api.factory.SupplyOrderRequest(**request)
        response = self.api.client.service.GetFulfilmentSupplyOrder(
            headerMessage=self.api.header,
            request=supply_order_report_request
        )
        return serialize_object(response, dict)

    # TODO Make this method more robust
    @auto_refresh_token
    def submit_fulfillment_activation(self, request):
        """
        To ask for products activation (or deactivation)

        :param list ProductList:

            - Action *(str)*:
                - 'Activation'
                - 'Deactivation'
            - Length *(double/float64)*:
            - Width *(double/float64)*:
            - Height *(double/float64)*:
            - Weight *(double/float64)*:
            - ProductEAN *(str)*:
            - SellerProductReference *(str)*: [optional]

        Example::

            api.fulfillment.submit_fulfillment_activation(
                product_list = [
                    {
                        'Action': 'Activation',
                        'Height': 1,
                        'Length': 20,
                        'ProductEAN': '2009863600561'
                        'Weight': 50,
                        'Width': 10
                    },
                    {
                        'Action': 'Activation',
                        'Height': 1,
                        'Length': 20,
                        'ProductEAN': 'BZ34567891234',
                        'Weight': 20,
                        'Width': 10
            )

        :return: deposit id
        """
        response = self.api.client.service.SubmitFulfilmentActivation(
            headerMessage=self.api.header,
            request=request
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_fulfillment_activation_report_list(self, **request):
        """
        To get status and details about fulfillment products activation.

        :param str BeginDate:
        :param list DepositIdList: int list
        :param str EndDate:

        Usage::

            response = api.fulfillment.get_fulfillment_activation_report_list(
                BeginDate='2019-04-26T09:54:38:72'
            )

        """
        activation_report_request = self.api.factory.FulfilmentActivationReportRequest(**request)
        response = self.api.client.service.GetFulfilmentActivationReportList(
            headerMessage=self.api.header,
            request=activation_report_request
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_fulfillment_order_list_to_supply(self, **request):
        """
        To ask for fulfillment on demand order lines to supply.

        :param str OrderReference:
        :param str ProductEan:
        :param str Warehouse:

        Example::

            response = api.fulfillment.get_fulfillment_order_list_to_supply(
                ProductEan='2009863600561'
            )

        :return: fulfillment on demand order lines to supply answering the search criterion.
        """
        references = self.api.factory.FulfilmentOnDemandOrderLineFilter(**request)
        response = self.api.client.service.GetFulfilmentActivationReportList(
            headerMessage=self.api.header,
            request=references
        )
        return serialize_object(response, dict)

    @auto_refresh_token
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

    @auto_refresh_token
    def create_external_order(self, order):
        """
        create an order from another marketplace.

        :param order: A dictionary with the structure:

        Example::

            response = api.fufillment.create_external_order(
            {
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
            }

        :return: The response
        """
        response = self.api.client.service.CreateExternalOrder(
            headerMessage=self.api.header,
            request={'Order': order}
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_external_order_status(self, **request):
        response = self.api.client.service.GetExternalOrderStatus(
            headerMessage=self.api.header,
            request={
                'Corporation': request.get('Corporation'),
                'CustomerOrderNumber': request.get('CustomerOrderNumber')
            }
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_stock_list(self, **request):
        """
        List seller product

        :param list BarCodeList:
        :param str FulfilmentReferencement:
        :param str ShippableStock:
        :param str BlockedStock:
        :param str SoldOut:

        Example::

            response = api.fulfillment.get_product_stock_list(
                FulfilmentReferencement='All',
                ShippableStock='All',
                BlockedStock='All',
                SoldOut='All'
            )

        :return:
        """
        response = self.api.client.service.GetProductStockList(
            headerMessage=self.api.header,
            request=request
        )
        return serialize_object(response, dict)
