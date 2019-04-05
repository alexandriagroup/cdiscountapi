# -*- coding: utf-8 -*-

import re
import pytest
import vcr


def read_fixture(filename):
    with open('cdiscountapi/tests/samples/{}'.format(filename),
              'r', encoding='utf8') as f:
        return f.read()


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
def vcr_config():
    return {
        'filter_headers': [('Authorization', None)],
        'before_record_response': scrub_strings(),
        'decode_compressed_response': True
    }