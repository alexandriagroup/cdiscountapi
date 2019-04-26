# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.offers
    ----------------------------

    Handles the offers.

    :copyright: © 2019 Alexandria
"""

from cdiscountapi.helpers import generate_package_url
from zeep.helpers import serialize_object
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

        - SellerProductIdList is a list of seller product references
        - OfferPoolId is

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
        - OfferFilterCriterion:
            - 'NewOffersOnly'
            - 'UsedOffersOnly'
        - OfferPoolId (int) is the distribution website Id
        - OfferSortOrder:
            - ByPriceAscending
            - ByPriceDescending
            - BySoldQuantityDescending
            - ByCreationDateDescending
        - OfferStateFilter:
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
        :rtype: dict
        """
        offer_filter = self.api.factory.OfferFilterPaginated(**filters)
        response = self.api.client.service.GetOfferListPaginated(
            headerMessage=self.api.header,
            offerFilter=offer_filter,
        )
        return serialize_object(response, dict)

    @auto_refresh_token
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
        return serialize_object(response, dict)

    @auto_refresh_token
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
        return serialize_object(response, dict)
