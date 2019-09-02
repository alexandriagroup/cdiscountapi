# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.offers
    ----------------------------

    Handles the offers.

    :copyright: © 2019 Alexandria
"""

from zeep.helpers import serialize_object

from cdiscountapi.helpers import generate_package
from .base import BaseSection
from ..helpers import auto_refresh_token


class Offers(BaseSection):
    """
    Offers section lets sellers retrieve information about their offers.

    Methods::

        get_offer_list(**filters)
        get_offer_list_paginated(**filters)
        generate_offer_package(package_name,
                               offers_list,
                               offer_publication_list=offer_publication_list,
                               purge_and_replace=purge_and_replace)
        submit_offer_package(url)
        get_offer_package_submission_result(package_id)

    Operations are included in the Products API section
    (https://dev.cdiscount.com/marketplace/?page_id=84)
    """

    @auto_refresh_token
    def get_offer_list(self, **filters):
        """
        To search offers.

        This operation seeks offers according to the
        following criteria:

        - SellerProductIdList: list of seller product references
        - OfferPoolId (int) is the distribution website Id

        Example::

            response = api.offers.get_offer_list(
                SellerProductIdList=['REF1', 'REF2', 'REF3'],
                OfferPoolId=1
            )

        :return: offers answering the search criterion
        """
        filters = self.update_with_valid_array_type(
            filters, {"SellerProductIdList": "string"}
        )

        offer_filter = self.api.factory.OfferFilter(**filters)
        response = self.api.client.service.GetOfferList(
            headerMessage=self.api.header, offerFilter=offer_filter
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_offer_list_paginated(self, **filters):
        """
        Recovery of the offers page by page.

        - PageNumber (int) [mandatory]
        - OfferFilterCriterion (str):
            - 'NewOffersOnly'
            - 'UsedOffersOnly'
        - OfferPoolId (int) is the distribution website Id
        - OfferSortOrder (str):
            - ByPriceAscending
            - ByPriceDescending
            - BySoldQuantityDescending
            - ByCreationDateDescending
        - OfferStateFilter (str):
            - WaitingForProductActivation
            - Active
            - Inactive
            - Archived
            - Fulfillment
        - SellerProductIdList (list of str)

        Example::

            response = api.offers.get_offer_list_paginated(
                PageNumber=1,
                OfferFilterCriterion='NewOffersOnly',
                OfferSortOrder='BySoldQuantityDescending',
                OfferStateFilter='Active'
            )

        :return: offers answering the search criterion
        """
        filters = self.update_with_valid_array_type(
            filters, {"SellerProductIdList": "string"}
        )

        offer_filter = self.api.factory.OfferFilterPaginated(**filters)
        response = self.api.client.service.GetOfferListPaginated(
            headerMessage=self.api.header, offerFilter=offer_filter
        )
        return serialize_object(response, dict)

    @staticmethod
    def generate_offer_package(
            package_name,
            package_path,
            offers_list,
            package_type="Full",
            offer_publication_list=[],
            purge_and_replace=False,
            overwrite=True
    ):
        """
        Generate a zip offers package as cdiscount wanted.

        :param str package_name: The name of the package
        :param str package_path: [mandatory] the full path to the offer package (without .zip)
        :param str package_type: [optional] The type of package ("Full" or
        "StockAndPrice")
        (default: "Full")
        :param list offer_publication_list: [optional]
        :param bool purge_and_replace: [optional]
        :param bool overwrite: [optional] Determine if an existing package is
        overwritten when a new one with the same name is created (default: True)
        :param list offers_list: list of dict [{offer, shipping}, ...]:

            -Offer:
                - Mandatory attributes:
                    - ProductEan *(str)*
                    - SellerProductId *(str)*
                    - ProductCondition *(int)*:
                        - 1: 'LikeNew',
                        - 2: 'VeryGoodState',
                        - 3: 'GoodState',
                        - 4: 'AverageState',
                        - 5: 'Refurbished',
                        - 6: 'New',
                    - Price *(float)*
                    - EcoPart *(float)*
                    - Vat *(float)*
                    - DeaTax *(float)*
                    - Stock *(int)*
                    - PreparationTime *(int)*
                - Optional attributes:
                    - Comment *(str)*
                    - StrikedPrice *(float)*
                    - PriceMustBeAligned *(str)*:
                        - 'Empty',
                        - 'Unknown',
                        - 'Align',
                        - 'DontAlign',
                    - MinimumPriceForPriceAlignment *(float)*
                    - ProductPackagingUnit *(str)*:
                        - 'None',
                        - 'Liter',
                        - 'Kilogram',
                        - 'SquareMeter',
                        - 'CubicMeter'
                    - ProductPackagingValue *(float)*
                    - BluffDeliveryMax *(int)*

            -ShippingInformation:
                - AdditionalShippingCharges *(float)*
                - DeliveryMode *(DeliveryModeInformation)*
                    - 'STD' ('Standart')
                    - 'TRK' ('Tracking')
                    - 'REG' ('Registered')
                    - 'COL' ('Collissimo')
                    - 'RCO' ('Relay Colis')
                    - 'REL' ('Mondial Relay')
                    - 'SO1' ('So Colissimo')
                    - 'MAG' ('in shop')
                    - 'LV1'
                    - 'LV2'
                    - 'LV'
                    - 'FST'
                    - 'EXP'
                    - 'RIM'
                - ShippingCharges *(float)*

        Example::

            response = api.offers.generate_offer_package(
                package_name,
                package_path,
                offers_list,
                offer_publication_list=offer_publication_list,
                purge_and_replace=purge_and_replace
            )

        :returns: None
        """
        return generate_package(
            "offer",
            package_path,
            {
                "OfferCollection": offers_list,
                "OfferPublicationList": offer_publication_list,
                "PurgeAndReplace": purge_and_replace,
                "Name": package_name,
                "PackageType": package_type
            },
            overwrite=overwrite
        )

    @auto_refresh_token
    def submit_offer_package(self, url):
        """
        To import offers.
        It is used to add new offers to the Cdiscount marketplace
        or to modify/update offers that already exists.

        .. note::

            The wanted zip package could be generate by calling

            ``api.offers.generate_offer_package(offer_list)``

        Then you'll have to get an url to download zip package
        Finally, you can use submit_offer_package(url)

        Examples::

            api.offers.submit_offer_package(url)

        :return: the id of package or -1
        """
        offer_package = self.api.factory.OfferPackageRequest(url)

        # Send request.
        response = self.api.client.service.SubmitOfferPackage(
            headerMessage=self.api.header, offerPackageRequest=offer_package
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_offer_package_submission_result(self, package_id):
        """
        This operation makes it possible to know the progress report of the offers import.

        :param long package_id: id of package we want to know the progress
        :return: Offer report logs
        """
        package = self.api.factory.PackageFilter(package_id)
        response = self.api.client.service.GetOfferPackageSubmissionResult(
            headerMessage=self.api.header, offerPackageFilter=package
        )
        return serialize_object(response, dict)
