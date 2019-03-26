# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

from zeep import Client
from zeep.exceptions import XMLSyntaxError
from cdiscountapi.exceptions import (
    CdiscountApiConnectionError,
    CdiscountApiTypeError,
)


class CdiscountApi(object):
    """A class ton manage the interaction with the CdiscountMarketplace API"""
    def __init__(self, credentials):
        self.headers = {
                'wsdl': credentials['wsdl'],
                'token': credentials['token'],
                'login': credentials['login'],

                }

    def connection(self):
        try:
            return Client(self.headers['wsdl'])
        except XMLSyntaxError:
            return CdiscountApiConnectionError(f'impossible to connect')

    def get_seller_info(self):
        """
        Return the data for the user given (if empty, return the data for the main account).
        :param user_id: the ID
        :type user_id: int
        :return: a dict with the data of the user
        :rtype: dict
        """

        client = self.connection()
        data = {
            'Context': {
                'SiteID': 100
            },
            'Localization': {
                'Country': 'De',
            },
            'Security': {
                'DomainRightsList': {
                    'DomainRights': {
                        'Name': 'toto',
                        'SecurityDescriptorList': {
                            'SecurityDescriptor': {
                                'Authorization': 'None',
                                'FunctionIdentifier': 'toto',
                                'Version': 10,
                            }
                        }
                    },
                },
                'IssuerID': 14511,
                'SessionID': 45564,
                'SubjectLocality': {
                    'Address': 'ta maman',
                    'DnsName': 'toto',
                },
                'TokenId': self.headers('token'),
                'UserName': 'toto',
            },
            'Version': 100,
        }
        response = client.service.GetSellerInformation(headerMessage=data)

        if not isinstance(response, Client):
            raise CdiscountApiTypeError(f'response should be a zeep.Client type not a {type(response)}')

        return response

