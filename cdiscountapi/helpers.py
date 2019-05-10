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

        xml_generator = XmlGenerator(data, preprod=preprod)
        content = xml_generator.render()

    Example::

        # Render the content of Offers.xml
        shipping_info1 = {
            'AdditionalShippingCharges': 1,
            'DeliveryMode': 'RelaisColis',
            'ShippingCharges': 1,
         }

        shipping_info2 = {
            'AdditionalShippingCharges': 5.95,
            'DeliveryMode': 'Tracked',
            'ShippingCharges': 2.95
        }

        discount_component = {
            'StartDate': datetime.datetime(2019, 11, 23),
            'EndDate': datetime.datetime(2019, 11, 25),
            'Price': 85,
            'DiscountValue': 1,
            'Type': 1
        }

        offer = {
            'ProductEan': 1,
            'SellerProductId': 1,
            'ProductCondition': '6'
            'Price': 100,
            'EcoPart': 0,
            'Vat': 0.19,
            'DeaTax': 0,
            'Stock': 1,
            'Comment': 'Offer with discount Tracked or RelaisColis'
            'PreparationTime': 1,
            'PriceMustBeAligned': 'Align',
            'ProductPackagingUnit': 'Kilogram',
            'ProductPackagingValue': 1,
            'MinimumPriceForPriceAlignment': 80,
            'StrikedPrice': 150,
            'DiscountList': {'DiscountComponent': [discount_component]},
            'ShippingInformationList': {'ShippingInformation': [shipping_info1, shipping_info2]}
           }

        offers_xml = XmlGenerator({'OfferCollection': [offer],
                                   'PurgeAndReplace': False,
                                   'OfferPublicationList': [1, 16]},
                                   preprod=preprod)
        content = offers_xml.render()

        # Render the content of Products.xml
        products_xml = XmlGenerator({'Products': [product]}, preprod=preprod)
        content = products_xml.render()

    """
    def __init__(self, data, preprod=False):
        if OfferPackage.has_required_keys(data):
            self.package = OfferPackage(data, preprod)
        elif ProductPackage.has_required_keys(data):
            self.package = ProductPackage(data, preprod)
        else:
            msg = ("The data should be a dictionary with the keys {offers} for"
                   "Offers.xml and {products} for Products.xml".format(
                       offers=OfferPackage.required_keys,
                       products=ProductPackage.required_keys))
            raise ValueError(msg)

        self.data = self.package.data

    def add(self, data):
        self.package.add(data)

    def render(self):
        return self.package.render()
