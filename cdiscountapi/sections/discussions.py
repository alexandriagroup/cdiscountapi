# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.discussions
    ---------------------------------

    Handles the discussions.

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object


class Discussions(object):
    """
    There are 3 ways to get discussions: discussions id, the discussions
    status, and all messages.

    Thanks to the discussion Id and the method GetDiscussionMailList you can
    get an encrypted mail address to reply to a question or a claim.  You can
    close a discussion list with the method CloseDiscussionList and the
    Discussion id, you cannot close a discussion without having answered
    Operations are included in the Discussions API section.
    (https://dev.cdiscount.com/marketplace/?page_id=148)
    """

    def __init__(self, api):
        self.api = api

    def get_order_claim_list(self, **order_claim_filter):
        """
        Return the list of order claims
        """
        order_claim_filter = self.api.factory.OrderClaimFilter(
            **order_claim_filter
        )
        response = self.api.client.service.GetOrderClaimList(
            headerMessage=self.api.header,
            orderClaimFilter=order_claim_filter
        )
        return serialize_object(response, dict)

    def get_offer_question_list(self, **offer_question_filter):
        """
        Return the list of questions about offers with the specified criteria

        :param offer_question_filter: The keywords for the filter
        `offerQuestionFilter`:

        - BeginCreationDate
        - BeginModificationDate
        - EndCreationDate
        - EndModificationDate
        - StatusList
        - ProductEANList
        - ProductSellerReferenceList

        Example:
        >>> response = api.get_offer_question_list(
            StatusList={'DiscussionStateFilter': 'Open'}
            )

        :returns: An OfferQuestionListMessage dictionary.

        """
        offer_question_filter = self.api.factory.OfferQuestionFilter(
            **offer_question_filter
        )
        response = self.api.client.service.GetOfferQuestionList(
            headerMessage=self.api.header,
            offerQuestionFilter=offer_question_filter
        )
        return serialize_object(response, dict)

    def get_order_question_list(self, **order_question_filter):
        """
        Return the list of questions about orders with the specified criteria

        :param order_question_filter: The keywords for the filter
        `orderQuestionFilter`:

        - BeginCreationDate
        - BeginModificationDate
        - EndCreationDate
        - EndModificationDate
        - StatusList
        - ProductEANList
        - ProductSellerReferenceList

        Example:
        >>> response = api.get_order_question_list(
            StatusList={'DiscussionStateFilter': 'Open'}
            )

        :returns: An OrderQuestionListMessage dictionary.

        """
        order_question_filter = self.api.factory.OrderQuestionFilter(
            **order_question_filter
        )
        response = self.api.client.service.GetOrderQuestionList(
            headerMessage=self.api.header,
            orderQuestionFilter=order_question_filter
        )
        return serialize_object(response, dict)

    def close_discussion_list(self, discussion_ids):
        """
        Close a discussion list

        :type discussion_ids: list
        :param discussion_ids: The list of discussion_ids to close

        Example:
        >>> response = api.discussions.close_discussion_list([31, 4, 159])
        """
        arrays_factory = self.api.client.type_factory(
            'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
        )
        close_discussion_request = self.api.factory.CloseDiscussionRequest(
            DiscussionIds=arrays_factory.ArrayOflong(discussion_ids)
        )
        response = self.api.client.service.CloseDiscussionList(
            headerMessage=self.api.header,
            closeDiscussionRequest=close_discussion_request
        )
        return serialize_object(response, dict)

