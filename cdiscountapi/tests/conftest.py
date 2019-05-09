# -*- coding: utf-8 -*-

from pathlib import Path
import os
import re
import datetime
import pytest
from functools import lru_cache
from ..cdiscountapi import Connection


VCR_CASSETTE_DIR = Path(__file__).parent.joinpath('cassettes')


def scrub_strings():
    def before_record_response(response):
        response['body']['string'] = re.sub(b'<ZipCode>.+</ZipCode>',
                                            b'<ZipCode>ZIP_CODE</ZipCode>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<SiretNumber>.+</SiretNumber>',
                                            b'<SiretNumber>SIRET_NUMBER</SiretNumber>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<Email>.+</Email>',
                                            b'<Email>EMAIL</Email>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<Login>.+</Login>',
                                            b'<Login>LOGIN</Login>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<MobileNumber>.+</MobileNumber>',
                                            b'<MobileNumber>MOBILE_NUMBER</MobileNumber>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<PhoneNumber>.+</PhoneNumber>',
                                            b'<PhoneNumber>PHONE_NUMBER</PhoneNumber>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<Address1>.+</Address1>',
                                            b'<Address1>ADDRESS1</Address1>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<Address2>.+</Address2>',
                                            b'<Address2>ADDRESS2</Address2>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<TokenId>.+</TokenId>',
                                            b'<TokenId>TOKEN_ID</TokenId>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<ShopName>.+</ShopName>',
                                            b'<ShopName>SHOP_NAME</ShopName>',
                                            response['body']['string'])
        response['body']['string'] = re.sub(b'<SellerLogin>.+</SellerLogin>',
                                            b'<SellerLogin>SELLER_LOGIN</SellerLogin>',
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
        'EcoPart': 0,
        'Vat': 19.6,
        'DeaTax': 0,
        'Stock': 1,
        'PreparationTime': 1,
        'DiscountList': [discount_component],
        'ShippingInformationList': [shipping_info1, shipping_info2]
    }
    return offer


@pytest.fixture
def valid_product():
    return {
        "BrandName": "BRAND",
        "SellerProductFamily": "SOJ50874",
        "SellerProductColorName": "Bleu Délavé",
        "Size": "38/34",
        "Description": ("Marque Deeluxe, Modèle Tanner Snow Bleu, Jeans Coupe"
                        " Droite Homme, Couleur Bleu Délavé, 100% Coton , Taille 28"),
        "LongLabel": "Nudie Average Joe organic vacation worn Jeans",
        "Model": "SOUMISSION CREATION PRODUITS_MK",
        'ProductKind': "Variant",
        "CategoryCode": "0R050A01",
        "SellerProductId": "120905783",
        "ShortLabel": "Jeans Deeluxe Tanner Snow Bleu",
        "Product.EanList": ["3606918243767"],
        "Product.ModelProperties": [{"Genre": "Homme - Garcon"}, {"Type de public": "Adulte"}],
        "Product.Pictures": [
            "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-1.jpg",
            "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-2.jpg",
            "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-3.jpg",
            "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-4.jpg",
        ]
    }
