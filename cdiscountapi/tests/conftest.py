# -*- coding: utf-8 -*-

from pathlib import Path
import re
import pytest


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
