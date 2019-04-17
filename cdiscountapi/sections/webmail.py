# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.webmail
    -----------------------------

    Handles the email addresses of the customers.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object


class WebMail(object):
    """
    The WebMail API allows the seller to retrieve encrypted email address to
    contact a customer

    Operations are included in the WebMail API section.
    (https://dev.cdiscount.com/marketplace/?page_id=167)
    """

    def __init__(self, api):
        self.api = api

    def generate_discussion_mail_guid(self, scopus_id=None):
        """
        Obtain an encrypted mail address.

        This operation allows getting an encrypted mail address to contact a
        customer about an order.

        Usage:
        >>> response = api.generate_discussion_mail_guid(scopus_id)
        """
        response = self.api.client.service.GenerateDiscussionMailGuid(
            headerMessage=self.api.header,
            request={'ScopusId': scopus_id}
        )
        return serialize_object(response, dict)

    def get_discussion_mail_list(self, discussion_ids):
        """
        Obtain an encrypted mail address about a discussion.

        This operation allows getting an encrypted mail address to contact a
        customer about a discussion (claim, retraction, questions).

        Usage:
        >>> response = api.webmail.generate_discussion_mail_guid(discussion_ids)
        """
        arrays_factory = self.api.client.type_factory(
            'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
        )
        request = self.api.factory.GetDiscussionMailListRequest(
            DiscussionIds=arrays_factory.ArrayOflong(discussion_ids)
        )
        response = self.api.client.service.GetDiscussionMailList(
            headerMessage=self.api.header,
            request=request
        )
        return serialize_object(response, dict)
