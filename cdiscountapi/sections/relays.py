# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.relays
    ----------------------------

    Handles the relays.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from .base import BaseSection


class Relays(BaseSection):
    """
    Allows to get information about the different available relays and submit
    new ones.

    Operations are included in the Relays API section.
    (https://dev.cdiscount.com/marketplace/?page_id=108)
    """
    def get_parcel_shop_list(self):
        response = self.api.client.service.GetParcelShopList(
            headerMessage=self.api.header,
        )
        return serialize_object(response, dict)

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
        return serialize_object(response, dict)

    def get_relays_file_submission_result(self, **relays_file_filter):
        """
        Get the state of progress of the relays file submission.

        Usage::

            response = api.get_relays_file_submission_result(
            relays_file_filter={'RelaysFileId': relays_file_id}
            )

        where ``relays_file_id`` is the value of RelaysFileId returned by
        SubmitRelaysFile.

        :param relays_file_filter: The dictionary containing the ID referencing the relays file submitted.
        :returns: The response with the information about the integration of the relays specified.
        """
        relays_file_filter = self.api.factory.RelaysFileFilter(
            **relays_file_filter
        )
        response = self.api.client.service.GetRelaysFileSubmissionResult(
            headerMessage=self.api.header,
            relaysFileFilter=relays_file_filter
        )
        return serialize_object(response, dict)

