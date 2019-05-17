# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import os
import re
import datetime
import pytest
from tempfile import gettempdir
from shutil import rmtree
from functools import lru_cache
from ..cdiscountapi import Connection


VCR_CASSETTE_DIR = Path(__file__).parent.joinpath('cassettes')


def scrub_strings():
    def before_record_response(response):
        substitutions = ['ZipCode', 'SiretNumber', 'Email', 'Login',
                         'MobilePhone', 'MobileNumber', 'PhoneNumber',
                         'Address1', 'Address2', 'Building', 'City', 'Country',
                         'FirstName', 'LastName', 'Street', 'TokenId',
                         'ShopName', 'SellerLogin', 'Civility',
                         'ShippingLastName', 'ShippingFirstName', 'Sender', 'Content']

        for substitution in substitutions:
            pattern = '<{0}>.+?</{0}>'.format(substitution)
            new_value = '<{0}>{1}</{0}>'.format(substitution, substitution.upper())
            response['body']['string'] = re.sub(pattern.encode('utf8'),
                                                new_value.encode('utf8'),
                                                response['body']['string'])
        return response
    return before_record_response


@pytest.fixture(scope='module')
def vcr_config(request):
    module_name = request.module.__name__.split('.')[-1]
    cassette_library_dir = str(VCR_CASSETTE_DIR.joinpath(module_name))
    return {
        'filter_headers': [('Authorization', None)],
        'before_record_response': scrub_strings(),
        'decode_compressed_response': True,
        'cassette_library_dir': cassette_library_dir
    }


@pytest.fixture
def vcr_cassette_name(request):
    """Name of the VCR cassette"""
    # f = request.function
    # Don't take into account the class
    # if hasattr(f, '__self__'):
    #     return f.__self__.__class__.__name__ + '.' + request.node.name
    return request.node.name


# We use a cache to prevent sending the request for each test
@pytest.fixture
@lru_cache(2)
def api():
    return Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                      os.getenv('CDISCOUNT_API_PASSWORD'),
                      header_message={
                          'Context': {
                              'SiteID': 100,
                              'CatalogID': 1
                          },
                          'Localization': {
                              'Country': 'Fr',
                          },
                          'Security': {
                              'UserName': '',
                          },
                          'Version': '1.0',
                      })


@pytest.fixture
def valid_offer():
    discount_component = {
        'DiscountValue': 5, 'Type': 1,
        'StartDate': datetime.datetime(2019, 4, 15),
        'EndDate': datetime.datetime(2019, 5, 15)
    }
    shipping_info1 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': {'Name': 'Standard'}
    }
    shipping_info2 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': {'Name': 'Tracked'}
    }
    offer = {
        'ProductEan': '978-1593274351',
        'SellerProductId': 'MY_SKU1',
        'ProductCondition': "6",
        'Price': 10,
        'DiscountList': {'DiscountComponent': [discount_component]},
        'ShippingInformationList': {'ShippingInformation': [shipping_info1, shipping_info2]},
        'ProductCondition': 4,
        'EcoTax': 0.10,
        'VatRate': 19.36,
        'DeaTax': 3.14,
        'Stock': 1,
    }
    return offer


@pytest.fixture
def valid_offer_for_package():
    """
    Valid information to create an offer in an offer package
    """
    discount_component = {
        'DiscountValue': 5, 'Type': 1,
        'StartDate': datetime.datetime(2019, 4, 15),
        'EndDate': datetime.datetime(2019, 5, 15)
    }
    shipping_info1 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': 'Standard'
    }
    shipping_info2 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': 'Tracked'
    }
    offer_for_package = {
        'ProductEan': '978-1593274351',
        'SellerProductId': 'MY_SKU1',
        'ProductCondition': "6",
        'Price': 10,
        'DiscountList': {'DiscountComponent': [discount_component]},
        'ShippingInformationList': {'ShippingInformation': [shipping_info1, shipping_info2]},
        'ProductCondition': 4,
        'EcoPart': 0.10,
        'Vat': 19.36,
        'DeaTax': 3.14,
        'Stock': 1,
        'PreparationTime': 1
    }
    return offer_for_package


@pytest.fixture
def valid_product_for_package():
    return {
        "BrandName": "Deeluxe",
        "SellerProductFamily": "SOJ50874",
        "SellerProductColorName": "Bleu Délavé",
        "Size": "38/34",
        "Description": "Marque Deeluxe, Modèle Tanner Snow Bleu, Jeans Coupe Droite Homme",
        "LongLabel": "Nudie Average Joe organic vacation worn Jeans",
        "Model": "SOUMISSION CREATION PRODUITS_MK",
        'ProductKind': "Variant",
        "CategoryCode": "0R050A01",
        "SellerProductId": "120905783",
        "ShortLabel": "Jeans Deeluxe Tanner Snow Bleu",
        "EanList": {'ProductEan': [{"Ean": "3606918243767"}]},
        "ModelProperties": [{"Genre": "Homme - Garçon"}, {"Type de public": "Adulte"}],
        "Pictures": {"ProductImage": [
            {"Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-1.jpg"},
            {"Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-2.jpg"},
            {"Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-3.jpg"},
            {"Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-4.jpg"},
        ]}
    }


@pytest.fixture
def valid_offers_for_package(valid_offer_for_package):
    """
    Valid information to create 2 offers in an offer package
    """
    valid_offer_for_package1 = deepcopy(valid_offer_for_package)
    valid_offer_for_package1['Price'] = 20
    valid_offer_for_package1['SellerProductId'] = 'MY_SKU2'
    return [valid_offer_for_package, valid_offer_for_package1]


@pytest.fixture
def valid_offer_package(valid_offers_for_package):
    """
    Return 2 valid offers to creae an offer package then remove 
    /tmp/uploading_package and /tmp/uploading_package.zip
    """
    output_dir = gettempdir()
    directory = '{}/uploading_package'.format(output_dir)
    zip_file = '{}/uploading_package.zip'.format(output_dir)

    yield valid_offers_for_package

    if os.path.exists(directory):
        rmtree(directory)
    if os.path.exists(zip_file):
        os.remove(zip_file)
