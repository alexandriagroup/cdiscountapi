# -*- coding: utf-8 -*-
"""
    cdiscountapi.helpers
    --------------------

    Implements various helpers.

    :copyright: © 2019 Alexandria
"""


from functools import wraps
from shutil import (
    copytree,
    make_archive,
)

import zeep
from cdiscountapi.packages import OfferPackage, ProductPackage


# TODO Remove package_type. Determine package_type from the keys in data 
def generate_package(package_type, output_dir, data):
    """
    Generate a zip package for the offers or the products

    Usage::

        generate_package(package_type, output_dir, data)

    Example::

        # Generate Offer package:
        generate_package('offer', output_dir, {'OfferCollection': offers,
                                               'OfferPublicationList': offer_publications,
                                               'PurgeAndReplace': purge_and_replace})

        # Generate Product package:
        generate_package('product', output_dir, {'Products': products})

    :param str package_type: 'offer' or 'product'
    :param str output_dir:  directory to create temporary files
    :param dict data: offers or products as you can see on
    tests/samples/products/products_to_submit.json or
    tests/samples/offers/offers_to_submit.json
    """
    if package_type not in ('offer', 'product'):
        raise ValueError('package_type must be either "offer" or "product".')

    # Create path.
    path = f'{output_dir}/uploading_package'

    # Copy tree package.
    package = copytree(f'{package_type}_package', path)
    xml_filename = package_type.capitalize() + 's.xml'

    # TODO Fix offer_dict
    # Add Products.xml from product_dict.
    with open(f"{package}/Content/{xml_filename}", "wb") as f:
        xml_generator = XmlGenerator(data)
        f.write(xml_generator.render())

    # Make a zip from package.
    zip_package = make_archive(output_dir, 'zip', path)

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
           ],
           'PriceMustBeAligned': 'DontAlign',
           'ProductPackagingUnit': 'Kilogram',
           'OfferState': 'Active',
           'ProductCondition': 'New'
           }


        xml_generator = XmlGenerator(data1, preprod=preprod)
        content = xml_generator.render()

    """
    def __init__(self, data, preprod=False):
        if OfferPackage.has_required_keys(data):
            self.package = OfferPackage(data, preprod)
        elif ProductPackage.has_required_keys(data):
            self.package = ProductPackage(data, preprod)
        else:
            raise ValueError("package_type should be 'Offers.xml' or 'Products.xml'.")

    def add(self, data):
        self.package.add(data)

    def render(self):
        return self.package.render()
