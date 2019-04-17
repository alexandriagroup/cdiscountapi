# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.orders
    ----------------------------

    Handles the orders.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from cdiscountapi.helpers import check_element, get_motive_id


class Orders(object):
    """
    Allows to list, validate or refund orders.

    Operations are included in the Orders API section.
    (https://dev.cdiscount.com/marketplace/?page_id=128)
    """

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

        Example::

            >>> response = api.orders.get_order_list(
                States=['CancelledByCustomer', 'Shipped']
            )

        - Recovery or not of the products of the order

        - Filter on date:
            - BeginCreationDate
            - EndCreationDate
            - BeginModificationDate
            - EndModificationDate

        Example::

            >>> response = api.orders.get_order_list(
                BeginCreationDate=datetime.datetime(2077, 1, 1)
            )

        - Order number list Liste (OrderReferenceList) Warning, this filter
          cannot be combined with others. If there is an order list, the other
          filters are unaccounted.

        Example::

            >>> response = api.orders.get_order_list(OrderReferenceList=['X1', 'X2'])

        - Filter on website thanks to the corporationCode.

        Example::

            >>> response = api.orders.get_order_list(CorporationCode='CDSB2C')

        - Filter by Order Type:
            - MKPFBC Orders (Marketplace fulfillment by Cdiscount)
            - EXTFBC Orders (External fulfillment by Cdiscount)
            - FBC Orders (Isfulfillment)

        Example::

            >>> response = api.get_order_list(OrderType='MKPFBC')

        - PartnerOrderRef filter from 1 to N external order (if it's a multiple
          search, separate PartnerOrderRefs by semicolon).
          PartnerOrderRef is the seller's reference

        Example::

            >>> response = api.get_order_list(PartnerOrderRef='SELLER_REF')

        - Recovery or not of the parcels of the order

        Example::

            >>> response = api.get_order_list(FetchParcels=True, OrderReferenceList=['X1'])
        """
        if 'States' in order_filter:
            order_filter.update(States=self.api.factory.ArrayOfOrderStateEnum(
                order_filter['States'])
            )

        if 'OrderReferenceList' in order_filter:
            arrays_factory = self.api.client.type_factory(
                'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
            )
            order_filter.update(OrderReferenceList=arrays_factory.ArrayOfstring(
                order_filter['OrderReferenceList'])
            )

        if 'FetchOrderLines' not in order_filter:
            order_filter.update(FetchOrderLines=True)

        order_filter = self.api.factory.OrderFilter(**order_filter)
        response = self.api.client.service.GetOrderList(
            headerMessage=self.api.header,
            orderFilter=order_filter,
        )
        return serialize_object(response, dict)

    def get_global_configuration(self):
        """
        Get cdiscount settings. This method allows to get a list of several
        settings:
        - Carrier list
        """
        response = self.api.client.service.GetGlobalConfiguration(
            headerMessage=self.api.header,
        )
        return serialize_object(response, dict)

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
        return serialize_object(
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
        :param data: The validation data for the orders. A list of dictionaries with the following structure::

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

        :param validate_order_list_message: The information about the orders to validate.

        There are two ways to create a `validate_order_list_message`:

        1. you can build the dictionary by yourself:

        Example::

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
                            ]})

        2. you can use `Orders.prepare_validations`:

        Example::

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
                )

        >>> api.orders.validate_order_list_message(**validate_order_list_message)

        """
        validate_order_list_message = self.api.factory.ValidateOrderListMessage(
            **validate_order_list_message
        )
        response = self.api.client.service.ValidateOrderList(
            headerMessage=self.api.header,
            validateOrderListMessage=validate_order_list_message
        )
        return serialize_object(response, dict)

    def create_refund_voucher(self, **request):
        """
        This method still allows refunding lines of an order whose state is
        "ShippedBySeller".

        An additional feature allows to make a commercial gesture on an order
        MKPCDS before and after shipping and on an order MKPFBC after shipping.

        Example::

            >>> response = api.orders.create_refund_voucher(
                CommercialGestureList=[{'Amount': 10, 'MotiveId': 'late_delivery'}],
                OrderNumber='ORDER_NUMBER_1',
                SellerRefundList={
                    'Mode': 'Claim',
                    'Motive': 'ClientClaim',
                    'RefundOrderLine': {'Ean': '4005274238223',
                                        'SellerProductId': '42382235',
                                        'RefundShippingCharges': True}
                    }
                )

        """
        # Check CommercialGestureList
        if 'CommercialGestureList' in request:
            commercial_gestures = request['CommercialGestureList']
            if isinstance(commercial_gestures, dict):
                commercial_gestures = [commercial_gestures]

            for commercial_gesture in commercial_gestures:
                motive_id = commercial_gesture.get('MotiveId')
                # MotiveId is a label
                if not isinstance(motive_id, int):
                    motive_id = get_motive_id(motive_id)

                commercial_gesture['MotiveId'] = motive_id
        else:
            commercial_gestures = None

        # Request
        request = self.api.factory.CreateRefundVoucherRequest(
            OrderNumber=request.get('OrderNumber'),
            CommercialGestureList=self.api.factory.ArrayOfRefundInformation(
                commercial_gestures
            ),
            SellerRefundList=self.api.factory.ArrayOfSellerRefundRequest(
                request.get('SellerRefundList')
            )
        )
        response = self.api.client.service.CreateRefundVoucher(
            headerMessage=self.api.header,
            request=request
        )
        return serialize_object(response, dict)

    def manage_parcel(self, parcel_actions_list=None, scopus_id=None):
        """
        Ask for investigation or ask for delivery certification.

        :param parcel_actions_list: The keywords from

            >>> api.manage_parcel(ParcelInfos=[
                {'ManageParcel': manage_parcel, 'ParcelNumber': parcel_number,
                 'Sku': sku},
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
        return serialize_object(response, dict)