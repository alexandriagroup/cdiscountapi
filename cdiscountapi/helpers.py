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


def generate_package(package_type, tempdir, offer_dict):
    """
    Generate a zip package for the offers or the products

    :param package_type: 'offer' or 'product'
    :type package_type: str
    :param tempdir:  directory to create temporary files
    :type tempdir: str
    :param offer_dict: offers as you can see on
    tests/samples/products/products_to_submit.json or
    tests/samples/offers/offers_to_submit.json
    :type offer_dict: dict
    :rtype: str
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
        f.write(dicttoxml(offer_dict))

    # Make a zip from package.
    zip_package = make_archive(path, 'zip', path)

    # Remove unzipped package.
    return zip_package


# TODO find a way to upload package et get url
def upload_and_get_url(package, url):
    """
    Upload package and get url to download it.
    :param package: way to find zip package
    :type package: str
    :param url: where to upload zip package
    :type url: str
    :return: where to download zip package
    :rtype: str
    """

    return url + package


def generate_offer_package(tempdir, offer_dict):
    """
    Generate a zip offers package as cdiscount wanted.
    :param tempdir:  directory to create temporary files
    :type tempdir: str
    :param offer_dict: offers as you can see on tests/samples/offers/offers_to_submit.json
    :type offer_dict: dict
    :return: zip package
    :rtype: str
    """
    return generate_package('offer', tempdir, offer_dict)


def generate_product_package(tempdir, product_dict):
    """
    Generate a zip product package as cdiscount wanted.
    :param tempdir: directory to create temporary files
    :type tempdir: str
    :param product_dict: products as you can see on tests/samples/products/products_to_submit.json
    :type product_dict: dict
    :return: zip package
    :rtype: str
    """
    return generate_package('product', tempdir, product_dict)


def generate_package_url(content_dict, url):
    """
    Generate and upload package and return the url

    :param content_dict: products or offers as you can see on tests/samples/products/products_to_submit.json
    :type content_dict: dict

    :param url: url to upload package
    :type url: str

    :return: url to find it
    :rtype: str
    """
    # Create a temporary package.
    tempdir = gettempdir()

    # Generate package according to content type.
    if 'Product' in content_dict.keys():
        package = generate_product_package(tempdir, content_dict)
    elif 'Offer' in content_dict.keys():
        package = generate_offer_package(tempdir, content_dict)

    # Generate zip package.
    zip_package = make_archive(package, 'zip', package)

    # Upload package and get url to download it.
    package_url = upload_and_get_url(zip_package, url)

    # Remove temporary package.
    rmtree(tempdir + '/uploading_package')
    return package_url


def check_element(element_name, dynamic_type):
    """
    Raise an exception if the is not in the dynamic_type

    Example
    >>> check_element('CarrierName', api.factory.ValidateOrder)
    """
    valid_elements = [x[0] for x in dynamic_type.elements]
    if element_name not in valid_elements:
        raise ValueError('{0} is not a valid element of {1}.'
                         ' Valid elements are {2}'.format(
                             element_name, dynamic_type.name, valid_elements)
                         )


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