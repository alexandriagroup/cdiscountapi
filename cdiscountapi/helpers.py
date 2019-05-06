# -*- coding: utf-8 -*-
"""
    cdiscountapi.helpers
    --------------------

    Implements various helpers.

    :copyright: © 2019 Alexandria
"""


from shutil import (
    make_archive,
    rmtree,
    copytree
)
from tempfile import gettempdir
from dicttoxml import dicttoxml
import zeep
from functools import wraps


def generate_package(package_type, tempdir, offer_dict):
    """
    Generate a zip package for the offers or the products

    :param str package_type: 'offer' or 'product'
    :param str tempdir:  directory to create temporary files
    :param dict offer_dict: offers as you can see on
    tests/samples/products/products_to_submit.json or
    tests/samples/offers/offers_to_submit.json
    """
    if package_type not in ('offer', 'product'):
        raise ValueError('package_type must be either "offer" or "product".')

    # Create path.
    path = f'{tempdir}/uploading_package'

    # Copy tree package.
    package = copytree(f'{package_type}_package', path)
    xml_filename = package_type.capitalize() + 's.xml'

    # Add Products.xml from product_dict.
    with open(f"{package}/Content/{xml_filename}", "wb") as f:
        f.write(XmlGenerator(offer_dict))

    # Make a zip from package.
    zip_package = make_archive(path, 'zip', path)

    # Remove unzipped package.
    return zip_package


def check_element(element_name, dynamic_type):
    """
    Raise an exception if the is not in the dynamic_type

    Example
    >>> check_element('CarrierName', api.factory.ValidateOrder)
    """
    valid_elements = [x[0] for x in dynamic_type.elements]
    if element_name not in valid_elements:
        raise TypeError(
            f'{element_name} is not a valid element of {dynamic_type.name}.'
            f' Valid elements are {valid_elements}'
        )


# TODO Damien: voir car l'utilisateur peut écrire
#  "Shipping Fees" ou "ShippingFees" au lieu de "shipping_fees"
def get_motive_id(label):
    label_to_motive_id = {
        'compensation_on_missing_stock': 131,
        'product_delivered_damaged': 132,
        'product_delivered_missing': 132,
        'error_of_reference': 133,
        'error_of_color': 133,
        'error_of_size': 133,
        'fees_unduly_charged_to_the_customer': 134,
        'late_delivery': 135,
        'product_return_fees': 136,
        'shipping_fees': 137,
        'warranty_period_passed': 138,
        'rights_of_withdrawal_passed': 138,
        'others': 139,
    }
    if label not in label_to_motive_id:
        raise KeyError("Please choose a valid label ({})".format(
            list(label_to_motive_id))
        )
    return label_to_motive_id[label]


# TODO Make sure the exceptions is well chosen for an outdated token
def auto_refresh_token(func):
    """
    Refresh the token when it's outdated and resend the request
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except zeep.exceptions.Fault:
            print('Refreshing token...')
            self.api.token = self.api.get_token()
            self.api.header['Security']['TokenId'] = self.api.token
            print('Resending request...')
            return func(*args, **kwargs)
    return wrapper


class XmlGenerator(object):
    """
    Generate offers or products to upload

    Usage::

        shipping_info =

        discount_component = [{
        'DiscountValue': 1,
        'EndDate': 1,
        'Price': 1,
        'StartDate': 1,
        'Type': 1
        }]

        offer_pool = [
            {
                'Id': 1,
                'Published': True
            },
            {
                'Id': 16
            }
        ]

        offer = {
            'CreationDate': 1,
            'LastUpdateDate': 1,
            'Price': 1,
            'ProductEan': 1,
            'ProductId': 1,
            'SellerProductId': 1,
            'Stock': 1, 'VatRate': 0.19,
            'DiscountList': discount_component,
                 'OfferPoolList': offer_pool,
                 'ShippingInformationList': [
                    {
                        'AdditionalShippingCharges': 1,
                        'DeliveryMode': 'RelaisColis',
                        'MaxLeadTime': 1,
                        'MinLeadTime': 1,
                        'ShippingCharges': 1,
                    },
                    {
                        'AdditionalShippingCharges': 5.95,
                        'DeliveryMode': 'Tracked',
                        'ShippingCharges': 2.95
                    }
                ]
                 'PriceMustBeAligned': 'DontAlign',
                 'ProductPackagingUnit': 'Kilogram',
                 'OfferState': 'Active',
                 'ProductCondition': 'New'
                 }

        generator = XmlGenerator()
        generator.add_offers([offer])
        generator.save()

    """
    def __init__(self, preprod=False):
        self.preprod = preprod
        if self.preprod:
            domain = 'preprod-cdiscount.com'
        else:
            domain = 'cdiscount.com'

        self.wsdl = 'https://wsvc.{0}/MarketplaceAPIService.svc?wsdl'.format(domain)
        self.client = zeep.Client(self.wsdl)
        self.factory = self.client.type_factory('http://www.cdiscount.com')
        self.offers = []

    def add_offers(self, offers):
        self.offers.append([self.validate_offer(offer) for offer in offers])

    def validate_offer(self, **kwargs):
        new_kwargs = kwargs.copy()

        # We check the types of the lists in Offer
        if 'DiscountList' in kwargs:
            new_kwargs['DiscountList'] = self.factory.ArrayOfDiscountComponent([
                self.factory.DiscountComponent(x) for x in new_kwargs['DiscountList']
            ])

        if 'ShippingInformationList' in kwargs:
            new_kwargs['ShippingInformationList'] = self.factory.ArrayOfShippingInformation([
                self.factory.ShippingInformation(x) for x in new_kwargs['ShippingInformationList']
            ])

        if 'OfferPoolList' in kwargs:
            new_kwargs['OfferPoolList'] = self.factory.ArrayOfOfferPool([
                self.factory.OfferPool(x) for x in new_kwargs['OfferPoolList']
            ])

        return self.factory.Offer(**new_kwargs)

    def save(self):
        pass
