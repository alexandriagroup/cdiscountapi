# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.relays
    ----------------------------

    Handles the relays.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from .base import BaseSection
from ..helpers import auto_refresh_token


class Relays(BaseSection):
    """
    Allows to get information about the different available relays and submit
    new ones.

    Methods::

        get_parcel_shop_list()
        submit_relays_file(relays_file_uri)
        get_relays_file_submission_result(relays_file_ids)

    Operations are included in the Relays API section.
    (https://dev.cdiscount.com/marketplace/?page_id=108)
    """

    @auto_refresh_token
    def get_parcel_shop_list(self):
        """
        To get a list of relays known.

        Usage::

            response = api.relays.get_parcel_shop_list()

        """
        response = self.api.client.service.GetParcelShopList(
            headerMessage=self.api.header
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def submit_relays_file(self, relays_file_uri):
        """
        Send information about relays in a file

        :param str relays_file_uri: A link pointing to a XLSX file with information about relays

        Usage::

            response = api.relays.submit_relays_file(
                'http://spreadsheetpage.com/downloads/xl/worksheet%20functions.xlsx'
            )

        where relays_file_uri is the URI to a XLSX file

        :returns: The response with the RelaysFileId for the file.

        """
        relays_file_request = self.api.factory.RelaysFileIntegrationRequest(
            relays_file_uri
        )
        response = self.api.client.service.SubmitRelaysFile(
            headerMessage=self.api.header, relaysFileRequest=relays_file_request
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_relays_file_submission_result(self, relays_file_ids):
        """
        Get the state of progress of the relays file submission.

        :param list relays_file_ids: IDs referencing the relays file submitted.

        Usage::

            response = api.get_relays_file_submission_result([15645,52486])

        where ``relays_file_id`` is the value of RelaysFileId returned by
        `SubmitRelaysFile <https://dev.cdiscount.com/marketplace/?page_id=112>`_.

        :returns: The response with the information about the integration of the specified relays.

        """
        relays_file_filter = self.api.factory.RelaysFileFilter(relays_file_ids)
        response = self.api.client.service.GetRelaysFileSubmissionResult(
            headerMessage=self.api.header, relaysFileFilter=relays_file_filter
        )
        return serialize_object(response, dict)
