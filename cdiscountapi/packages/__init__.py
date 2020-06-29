# -*- coding: utf-8 -*-
"""
    cdiscountapi.packages
    ---------------------

    Implements the Offers.xml and Products.xml content generation.

    :copyright: © 2019 Alexandria
"""


# Python imports
from copy import deepcopy
import os

# Third-party imports
import zeep
from jinja2 import Environment, FileSystemLoader

from cdiscountapi.packages.validator import (
    OfferValidator,
    ProductValidator,
    DiscountComponentValidator,
    ShippingInformationValidator,
    ProductEanValidator,
    ProductImageValidator,
)


class BasePackage(object):
    required_keys = []

    def __init__(self, preprod=False):
        self.preprod = preprod
        if self.preprod:
            domain = "preprod-cdiscount.com"
        else:
            domain = "cdiscount.com"

        self.wsdl = "https://wsvc.{0}/MarketplaceAPIService.svc?wsdl".format(domain)
        self.client = zeep.Client(self.wsdl)
        self.factory = self.client.type_factory("http://www.cdiscount.com")
        self.data = []

    def validate(self, **kwargs):
        raise NotImplementedError

    def generate(self):
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
    required_keys = ["OfferCollection"]

    def __init__(self, data, preprod=False):
        super().__init__(preprod=preprod)
        self.check_offer_publication_list(data.get("OfferPublicationList"))
        self.purge_and_replace = data.get("PurgeAndReplace", False)
        self.name = data.get("Name", "A package")
        self.package_type = data.get("PackageType", "Full")
        self.add(data["OfferCollection"])

    def check_offer_publication_list(self, ids):
        """
        The offer_publication_list should be a list of integers representing
        the id of the marketplaces if it exists.
        """
        if not ids:
            self.offer_publication_list = []
            return None

        msg = (
            "The value OfferPublicationList should be a list of"
            " integers representing the ids of the marketplaces."
        )

        if not isinstance(ids, (list, tuple)):
            raise TypeError(msg)

        for _id in ids:
            if not isinstance(_id, int):
                raise TypeError(msg)

        self.offer_publication_list = [{"Id": _id} for _id in ids]

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
        Return the valid offer

        Usage::

            offer_package.validate(**kwargs)

        """
        new_kwargs = kwargs.copy()

        # We validate the lists in Offer
        if "DiscountList" in kwargs:
            new_kwargs["DiscountList"] = {
                "DiscountComponent": [
                    DiscountComponentValidator.validate(x)
                    for x in new_kwargs["DiscountList"]["DiscountComponent"]
                ]
            }

        if "ShippingInformationList" in kwargs:
            new_kwargs["ShippingInformationList"] = {
                "ShippingInformation": [
                    ShippingInformationValidator.validate(x)
                    for x in new_kwargs["ShippingInformationList"][
                        "ShippingInformation"
                    ]
                ]
            }

        return OfferValidator.validate(new_kwargs["Offer"])

    def generate(self):
        loader = FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "..", "templates")
        )
        env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template("Offers.xml")
        offers = deepcopy(self.data)
        extraction_mapping = {
            "shipping_information_list": (
                "ShippingInformationList",
                "ShippingInformation",
            ),
            "discount_list": ("DiscountList", "DiscountComponent"),
        }

        offers_data = []
        for offer in offers:
            offers_datum = {}
            for key, (attr1, attr2) in extraction_mapping.items():
                # Only add  if the user provided the attribute
                if attr1 in offer:
                    if key not in offers_datum and attr1 in offer:
                        offers_datum[key] = []
                    offers_datum[key].extend(self.extract_from(offer, attr1, attr2))

            if "attributes" not in offers_datum:
                offers_datum["attributes"] = ""

            # We keep only key:value pairs whose values are not None
            offers_datum["attributes"] += " ".join(
                '{}="{}"'.format(k, v) for k, v in offer.items() if v is not None
            )
            offers_data.append(offers_datum)
        return template.render(
            offers=offers_data,
            offer_publication_list=self.offer_publication_list,
            purge_and_replace=self.purge_and_replace,
            package_type=self.package_type,
            name=self.name
        )


class ProductPackage(BasePackage):
    required_keys = ["ProductCollection"]

    def __init__(self, data, preprod=False):
        super().__init__(preprod=preprod)
        self.name = data.get("Name", "A package")
        self.add(data["ProductCollection"])

    def add(self, products):
        for product in products:
            valid_product = self.validate(**product)
            if valid_product not in self.data:
                self.data.append(valid_product)

    def extract_from(self, product, attr1, attr2):
        """
        Extract the elements of a list from Offer

        (ex: the ShippingInformation elements in ShippingInformationList,
        the DiscountComponent elements in DiscountList...)
        """
        if attr1 in product:
            sub_record = product.get(attr1, None)
            if sub_record:
                datum = sub_record[attr2]
                del product[attr1]
                return datum
            else:
                return []
        else:
            return []

    def validate(self, **kwargs):
        new_kwargs = kwargs.copy()
        if "EanList" in kwargs:
            new_kwargs["EanList"] = {
                "ProductEan": [
                    ProductEanValidator.validate(x)
                    for x in new_kwargs["EanList"]["ProductEan"]
                ]
            }

        if "Pictures" in kwargs:
            new_kwargs["Pictures"] = {
                "ProductImage": [
                    ProductImageValidator.validate(x)
                    for x in new_kwargs["Pictures"]["ProductImage"]
                ]
            }

        return ProductValidator.validate(new_kwargs["Product"])

    def generate(self):
        loader = FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "..", "templates")
        )
        env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template("Products.xml")
        products = deepcopy(self.data["Products"])
        extraction_mapping = {
            "EanList": ("EanList", "ProductEan"),
            "Pictures": ("Pictures", "ProductImage"),
        }

        products_data = []
        for product in products:
            prod = product['Product']
            products_datum = {}
            for key, (attr1, attr2) in extraction_mapping.items():
                if key not in products_datum:
                    products_datum[key] = []
                products_datum[key].append(self.extract_from(prod, attr1, attr2))

            if "ModelProperties" in prod:
                products_datum["ModelProperties"] = prod["ModelProperties"]
                del prod["ModelProperties"]

            if "attributes" not in products_datum:
                products_datum["attributes"] = ""

            # We keep only key:value pairs whose values are not None
            products_datum["attributes"] += " ".join(
                '{}="{}"'.format(k, v) for k, v in prod.items() if v is not None
            )
            products_data.append(products_datum)
        capacity = sum(len(p['Pictures']) for p in products_data)
        return template.render(
            products=products_data, capacity=capacity, name=self.name
        )
