# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.offers
    ----------------------------

    Handles the offers.

    :copyright: © 2019 Alexandria
"""

from shutil import make_archive

from zeep.helpers import serialize_object

from cdiscountapi.helpers import generate_package
from .base import BaseSection
from ..helpers import auto_refresh_token


class Offers(BaseSection):
    """
    Offers section lets sellers retrieve information about their offers.

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
        filters = self.update_with_valid_array_type(filters, {'SellerProductIdList': 'string'})

        offer_filter = self.api.factory.OfferFilter(**filters)
        response = self.api.client.service.GetOfferList(
            headerMessage=self.api.header,
            offerFilter=offer_filter,
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
        offer_filter = self.api.factory.OfferFilterPaginated(**filters)
        response = self.api.client.service.GetOfferListPaginated(
            headerMessage=self.api.header,
            offerFilter=offer_filter,
        )
        return serialize_object(response, dict)

    @staticmethod
    def generate_offer_package(output_dir, offers_list, pool_list=[], purge_and_replace=False):
        """
        Generate a zip offers package as cdiscount wanted.

        :param str output_dir: [mandatory] path to generate package
        :param list pool_list: [optional]
        :param bool purge_and_replace: [optional]
        :param list offers_list:

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
                - PreparationTime *(byte)*
            - Optional attributes:
                - Comment *(str)*
                - StrikedPrice *(float)*
                - PriceMustBeAligned *(int)*:
                    - 1: 'Empty',
                    - 2: 'Unknown',
                    - 3: 'Align',
                    - 4: 'DontAlign',
                - MinimumPriceForPriceAlignment *(float)*
                - ProductPackagingUnit *(str)*:
                    - 'None',
                    - 'Liter',
                    - 'Kilogram',
                    - 'SquareMeter',
                    - 'CubicMeter'
                - ProductPackagingValue *(float)*
                - BluffDeliveryMax *(int)*

        Example::

            response = api.offers.generate_offer_package(
                offers_list,
                pool_list=pool_list,
                purge_and_replace=purge_and_replace
            )

        :return: the id of package or -1
        """
        return generate_package('offer', output_dir, {
            'OfferCollection': offers_list,
            'OfferPublicationList': pool_list,
            'PurgeAndReplace': purge_and_replace
        })

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
            headerMessage=self.api.header,
            offerPackageRequest=offer_package,
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
            headerMessage=self.api.header,
            offerPackageFilter=package,
        )
        return serialize_object(response, dict)
