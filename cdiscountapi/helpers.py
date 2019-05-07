# -*- coding: utf-8 -*-
"""
    cdiscountapi.helpers
    --------------------

    Implements various helpers.

    :copyright: © 2019 Alexandria
"""


from copy import deepcopy
from functools import wraps
from shutil import (
    copytree,
    make_archive,
)

import zeep
from jinja2 import (
    Environment,
    FileSystemLoader,
)


def generate_package(package_type, path, data):
    """
    Generate a zip package for the offers or the products

    :param str package_type: 'offer' or 'product'
    :param str path:  directory to create temporary files
    :param dict data: offers or products as you can see on
    tests/samples/products/products_to_submit.json or
    tests/samples/offers/offers_to_submit.json
    """
    if package_type not in ('offer', 'product'):
        raise ValueError('package_type must be either "offer" or "product".')

    # Create path.
    path = f'{path}/uploading_package'

    # Copy tree package.
    package = copytree(f'{package_type}_package', path)
    xml_filename = package_type.capitalize() + 's.xml'

    # TODO Fix offer_dict
    # Add Products.xml from product_dict.
    with open(f"{package}/Content/{xml_filename}", "wb") as f:
        xml_generator = XmlGenerator(data)
        f.write(xml_generator.generate_offers())

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
           ],
           'PriceMustBeAligned': 'DontAlign',
           'ProductPackagingUnit': 'Kilogram',
           'OfferState': 'Active',
           'ProductCondition': 'New'
           }

        xml_generator = XmlGenerator()
        xml_generator.add_offers([offer])
        content = xml_generator.generate_offers()

    """
    def __init__(self, offers=[], preprod=False):
        self.preprod = preprod
        if self.preprod:
            domain = 'preprod-cdiscount.com'
        else:
            domain = 'cdiscount.com'

        self.wsdl = 'https://wsvc.{0}/MarketplaceAPIService.svc?wsdl'.format(domain)
        self.client = zeep.Client(self.wsdl)
        self.factory = self.client.type_factory('http://www.cdiscount.com')
        self.offers = []
        if offers:
            self.add_offers(offers)

    def add_offers(self, offers):
        """
        Add unique valid offers
        """
        for offer in offers:
            valid_offer = self.validate_offer(**offer)
            if valid_offer not in self.offers:
                self.offers.append(valid_offer)

    def validate_offer(self, **kwargs):
        """
        Return the valid offer as a `zeep.objects.Offer`

        Usage::

            xml_generator.validate_offer(offer)

        """
        new_kwargs = kwargs.copy()

        # We check the types of the lists in Offer
        if 'DiscountList' in kwargs:
            new_kwargs['DiscountList'] = self.factory.ArrayOfDiscountComponent([
                self.factory.DiscountComponent(**x) for x in new_kwargs['DiscountList']
            ])

        if 'ShippingInformationList' in kwargs:
            new_kwargs['ShippingInformationList'] = self.factory.ArrayOfShippingInformation([
                self.factory.ShippingInformation(**x) for x in new_kwargs['ShippingInformationList']
            ])

        if 'OfferPoolList' in kwargs:
            new_kwargs['OfferPoolList'] = self.factory.ArrayOfOfferPool([
                self.factory.OfferPool(**x) for x in new_kwargs['OfferPoolList']
            ])

        return self.factory.Offer(**new_kwargs)

    def extract_from_offer(self, offer, attr1, attr2):
        """
        Extract the elements of a list in Offer

        (ex: the ShippingInformation elements in ShippingInformationList,
        the DiscountComponent elements in DiscountList...)
        """
        if attr1 in offer:
            sub_record = getattr(offer, attr1, None)
            if sub_record:
                datum = sub_record[attr2]
                del offer[attr1]
                return datum
            else:
                return []
        else:
            return []

    def render_offers(self):
        loader = FileSystemLoader('cdiscountapi/templates')
        # env = Environment(loader=loader, autoescape=select_autoescape(['xml']))
        env = Environment(loader=loader)
        template = env.get_template('Offers.xml')
        offers = deepcopy(self.offers)
        extraction_mapping = {
            'shipping_information_list': ('ShippingInformationList', 'ShippingInformation'),
            'discount_list': ('DiscountList', 'DiscountComponent'),
            'offer_pool_list': ('OfferPoolList', 'OfferPool'),
        }

        offers_data = []
        for offer in offers:
            offers_datum = {}
            for key, (attr1, attr2) in extraction_mapping.items():
                if key not in offers_datum:
                    offers_datum[key] = []
                offers_datum[key].extend(self.extract_from_offer(offer, attr1, attr2))

            if 'attributes' not in offers_datum:
                offers_datum['attributes'] = ''

            # We keep only key:value pairs whose values are not None
            offers_datum['attributes'] += " ".join('{}="{}"'.format(k, v) for k, v in
                                                   offer.__values__.items() if v is not None)
            offers_data.append(offers_datum)
        return template.render(offers=offers_data)
