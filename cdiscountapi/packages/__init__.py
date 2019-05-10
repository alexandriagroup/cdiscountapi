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

from cdiscountapi.packages.validator import (
    OfferValidator,
    DiscountComponentValidator,
    ShippingInformationValidator
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
            sub_record = offer.get(attr1, None)
            if sub_record:
                datum = sub_record[attr2]
                del offer[attr1]
                return datum
            else:
                return []
        else:
            return []

    def validate(self, **kwargs):
        """
        Return the valid offer as a `zeep.objects.Offer`

        Usage::

            offer_package.validate(**kwargs)

        """
        new_kwargs = kwargs.copy()

        # We validate the lists in Offer
        if 'DiscountList' in kwargs:
            new_kwargs['DiscountList'] = {
                'DiscountComponent': [DiscountComponentValidator.validate(x) for x in
                new_kwargs['DiscountList']['DiscountComponent']
            ]}

        if 'ShippingInformationList' in kwargs:
            new_kwargs['ShippingInformationList'] = {
                'ShippingInformation': [ShippingInformationValidator.validate(x) for x in
                new_kwargs['ShippingInformationList']['ShippingInformation']
            ]}

        return OfferValidator.validate(new_kwargs)

    def render(self):
        loader = FileSystemLoader('cdiscountapi/templates')
        env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('Offers.xml')
        offers = deepcopy(self.data)
        extraction_mapping = {
            'shipping_information_list': ('ShippingInformationList', 'ShippingInformation'),
            'discount_list': ('DiscountList', 'DiscountComponent'),
        }

        # TODO Handle OfferPublicationList
        # 'offer_publication_list': ('OfferPublicationList', 'PublicationPool'),

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
                                                   offer.items() if v is not None)
            offers_data.append(offers_datum)
        return template.render(offers=offers_data)


class ProductPackage(BasePackage):
    required_keys = ['Products']

    def __init__(self, data, preprod=False):
        super().__init__(preprod=preprod)
        self.add(data['Products'])

    def add(self, products):
        for product in products:
            valid_product = self.validate(**product)
            if valid_product not in self.data:
                self.data.append(valid_product)

    def validate(self, **kwargs):
        return kwargs

    def render(self):
        loader = FileSystemLoader('cdiscountapi/templates')
        env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('Products.xml')
        products = deepcopy(self.data)
