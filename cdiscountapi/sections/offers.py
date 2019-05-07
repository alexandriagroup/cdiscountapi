# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.offers
    ----------------------------

    Handles the offers.

    :copyright: © 2019 Alexandria
"""

from cdiscountapi.helpers import generate_package
from zeep.helpers import serialize_object
from .base import BaseSection
from ..helpers import auto_refresh_token
from tempfile import gettempdir
from shutil import make_archive


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
    def generate_offer_package(offers_dict):
        """
        Generate a zip offers package as cdiscount wanted.

        :param dict offers_dict: offers as you can see on tests/samples/offers/offers_to_submit.json

        Example::

            response = api.offers.submit_offer_package(
                offers_dict={
                    "OfferPackage": {
                        "-xmlns": "clr-namespace:Cdiscount.Service.OfferIntegration.Pivot;assembly=Cdiscount.Service.OfferIntegration",
                        "-xmlns:x": "http://schemas.microsoft.com/winfx/2006/xaml",
                        "-Name": "Nom fichier offres",
                        "-PurgeAndReplace": "false",
                        "-PackageType": "StockAndPrice",
                        "OfferPackage.Offers": {
                            "OfferCollection": {
                                "-Capacity": "1",
                                "Offer": {
                                    "-SellerProductId": "S53262149036",
                                    "-ProductEan": "9153262149367",
                                    "-Price": "19.95",
                                    "-Stock": "10"
                                }
                            }
                        },
                        "OfferPackage.OfferPublicationList": {
                            "OfferPublicationList": {
                                "-Capacity": "2",
                                "PublicationPool": [
                                    { "-Id": "1" },
                                    { "-Id": "16" }
                                ]
                            }
                        }
                    }
                },
            )
        :return: the id of package or -1
        """
        # Create a temporary package.
        tempdir = gettempdir()

        package = generate_package('offer', tempdir, offers_dict)

        return make_archive(package, 'zip', package)

    @auto_refresh_token
    def submit_offer_package(self, url):
        """
        To import offers.
        It is used to add new offers to the Cdiscount marketplace
        Or to modify/update offers that already exists.

        There is 2 ways to use it.

        1. You can generate a zip package with:
            api.offers.generate_offer_package(offer_list)

        2. You can generate the package yourself before uploading.

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
