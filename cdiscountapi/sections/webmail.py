# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.webmail
    -----------------------------

    Handles the email addresses of the customers.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object
from .base import BaseSection
from ..helpers import auto_refresh_token


class WebMail(BaseSection):
    """
    The WebMail API allows the seller to retrieve encrypted email address to
    contact a customer

    Methods::

        generate_discussion_mail_guid(order_id)
        get_discussion_mail_list(discussion_ids)

    Operations are included in the WebMail API section.
    (https://dev.cdiscount.com/marketplace/?page_id=167)
    """

    @auto_refresh_token
    def generate_discussion_mail_guid(self, order_id):
        """
        Generate an encrypted mail address from an order.

        This operation allows getting an encrypted mail address to contact a
        customer.

        :param str order_id: Order id for which an e-mail is to be sent.

        Usage::

            response = api.generate_discussion_mail_guid(order_id)

        """
        response = self.api.client.service.GenerateDiscussionMailGuid(
            headerMessage=self.api.header, request={"ScopusId": order_id}
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_discussion_mail_list(self, discussion_ids):
        """
        Get encrypted mail addresses from discussions.

        This operation allows getting an encrypted mail address to contact a
        customer.

        Usages::
            id = 113163877
            response = api.webmail.get_discussion_mail_list(id)

            ids = [113163877, 224274988]
            response = api.webmail.get_discussion_mail_list(ids)

        """
        request = self.api.factory.GetDiscussionMailListRequest(
            DiscussionIds=self.array_of("long", discussion_ids)
        )
        response = self.api.client.service.GetDiscussionMailList(
            headerMessage=self.api.header, request=request
        )
        return serialize_object(response, dict)
