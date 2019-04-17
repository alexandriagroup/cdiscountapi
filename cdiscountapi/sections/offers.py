# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.offers
    ----------------------------

    Handles the offers.

    :copyright: © 2019 Alexandria
"""

from cdiscountapi.helpers import generate_package_url
from zeep.helpers import serialize_object


class Offers(object):
    """
    Offers section lets sellers retrieve informations about their offers.

    Operations are included in the Products API section
    (https://dev.cdiscount.com/marketplace/?page_id=84)
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
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

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
