# -*- coding: utf-8 -*-
"""
    cdiscountapi.packages
    ---------------------

    Implements the Offers.xml and Products.xml content generation.

    :copyright: © 2019 Alexandria
"""


# Python imports
from copy import deepcopy

# Third-party imports
import zeep
from jinja2 import (
    Environment,
    FileSystemLoader,
)


class BasePackage(object):
    required_keys = []

    def __init__(self, preprod=False):
        self.preprod = preprod
        if self.preprod:
            domain = 'preprod-cdiscount.com'
        else:
            domain = 'cdiscount.com'

        self.wsdl = 'https://wsvc.{0}/MarketplaceAPIService.svc?wsdl'.format(domain)
        self.client = zeep.Client(self.wsdl)
        self.factory = self.client.type_factory('http://www.cdiscount.com')
        self.data = []

    def validate(self, **kwargs):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    @classmethod
    def has_required_keys(cls, data):
        """
        Return True if the data passed to the package have the required keys
        """
        for required_key in cls.required_keys:
            if required_key not in data.keys():
                return False
        return True


class OfferPackage(BasePackage):
    required_keys = ['OfferCollection']

    def __init__(self, data, preprod=False):
        super().__init__(preprod=preprod)
        self.check_offer_publication_list(data.get('OfferPublicationList'))
        self.purge_and_replace = data.get('PurgeAndReplace', False)
        self.add(data['OfferCollection'])

    def check_offer_publication_list(self, ids):
        """
        The offer_publication_list should be a list of integers representing
        the id of the marketplaces if it exists.
        """
        if not ids:
            self.offer_publication_list = []
            return None

        msg = ("The value OfferPublicationList should be a list of"
               " integers representing the ids of the marketplaces.")

        if not isinstance(ids, (list, tuple)):
            raise TypeError(msg)

        for _id in ids:
            if not isinstance(_id, int):
                raise TypeError(msg)

        self.offer_publication_list = ids

    def add(self, offers):
        for offer in offers:
            valid_offer = self.validate(**offer)
            if valid_offer not in self.data:
                self.data.append(valid_offer)

    def extract_from(self, offer, attr1, attr2):
        """
        Extract the elements of a list from Offer

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

    @staticmethod
    def validate_offer(data):
        offer_attributes = {
            'ProductEan': 'Mandatory',
            'SellerProductId': 'Mandatory',
            'ProductCondition': 'Mandatory',
            'Price': 'Mandatory',
            'EcoPart': 'Mandatory',
            'Vat': 'Mandatory',
            'DeaTax': 'Mandatory',
            'Stock': 'Mandatory',
            'PreparationTime': 'Mandatory',
            'Comment': 'Optional',
            'StrikedPrice': 'Optional',
            'PriceMustBeAligned': 'Optional',
            'MinimumPriceForPriceAlignment': 'Optional',
            'ProductPackagingUnit': 'Optional',
            'ProductPackagingValue': 'Optional',
            'BluffDeliveryMax': 'Optional'
        }
        offer = {}
        for attr in offer_attributes.keys():
            if offer_attributes[attr] == 'Mandatory':
                try:
                    offer[attr] = data[attr]
                except KeyError:
                    raise KeyError(f'Missing element {attr}')
            if offer_attributes[attr] == 'Optional':
                offer[attr] = data.get(attr, None)

        return offer

    def validate(self, **kwargs):
        """
        Return the valid offer as a `zeep.objects.Offer`

        Usage::

            offer_package.validate(**kwargs)

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

        return self.validate_offer(**new_kwargs)

    def render(self):
        loader = FileSystemLoader('cdiscountapi/templates')
        env = Environment(loader=loader)
        template = env.get_template('Offers.xml')
        offers = deepcopy(self.data)
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
                offers_datum[key].extend(self.extract_from(offer, attr1, attr2))

            if 'attributes' not in offers_datum:
                offers_datum['attributes'] = ''

            # We keep only key:value pairs whose values are not None
            offers_datum['attributes'] += " ".join('{}="{}"'.format(k, v) for k, v in
                                                   offer.__values__.items() if v is not None)
            offers_data.append(offers_datum)
        return template.render(offers=offers_data)


class ProductPackage(BasePackage):
    required_keys = ['Products']

    def __init__(self, data, preprod=False):
        super().__init__(preprod=preprod)
        self.add(data['Products'])

    def add(self, data):
        pass

    @staticmethod
    def validate_product(data):
        product_attributes = {
            'BrandName': 'Mandatory',
            'Description': 'Mandatory',
            'LongLabel': 'Mandatory',
            'Model': 'Mandatory',
            'Navigation': 'Mandatory',
            'ProductKind': 'Mandatory',
            'SellerProductId': 'Mandatory',
            'ShortLabel': 'Mandatory',
            'Width': 'Optional',
            'Weight': 'Optional',
            'Length': 'Optional',
            'Height': 'Optional',
            'Size': 'Optional',
            'SellerProductFamily': 'Optional',
            'SellerProductColorName': 'Optional',
            'ManufacturerPartNumber': 'Optional',
            'ISBN': 'Optional',
            'EncodedMarketingDescription': 'Optional'
        }
        product = {}
        for attr in product_attributes.keys():
            if product_attributes[attr] == 'Mandatory':
                try:
                    product[attr] = data[attr]
                except KeyError:
                    raise KeyError(f'Missing element {attr}')
            if product_attributes[attr] == 'Optional':
                product[attr] = data.get(attr, None)

        return product

    def validate(self, **kwargs):
        pass

