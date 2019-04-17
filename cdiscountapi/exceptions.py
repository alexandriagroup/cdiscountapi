# -*- coding: utf-8 -*-
"""
    cdiscountapi.exceptions
    -------------------------

    Define specific exceptions.

    :copyright: © 2019 Alexandria
"""


class CdiscountApiException(Exception):
    """"""
    pass


class CdiscountApiConnectionError(CdiscountApiException):
    """"""
    pass


class CdiscountApiTypeError(CdiscountApiException):
    """"""
    pass


class CdiscountApiOrderError(CdiscountApiException):
    """
    Raised when there's an error in the order
    """
