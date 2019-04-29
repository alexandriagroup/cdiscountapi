# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.products
    ------------------------------

    Handles the products.

    :copyright: © 2019 Alexandria
"""

from cdiscountapi.helpers import generate_package_url
from zeep.helpers import serialize_object
from .base import BaseSection
from ..helpers import auto_refresh_token


class Products(BaseSection):
    """
    Allows to get information about products and submit new products on Cdiscount.

    Operations are included in the Products API section.
    (https://dev.cdiscount.com/marketplace/?page_id=220)
    """
    @auto_refresh_token
    def get_allowed_category_tree(self):
        """
        Categories which are accessible to the seller.

        Example::

            response = api.products.get_allowed_category_tree()

        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        :rtype: dict
        """
        response = self.api.client.service.GetAllowedCategoryTree(
            headerMessage=self.api.header
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_all_allowed_category_tree(self):
        """
        All categories.

        Example::

            response = api.products.get_all_allowed_category_tree()

        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        :rtype: dict
        """
        from ..cdiscountapi import Connection
        api_all = Connection('AllData', 'pa$$word', header_message=self.header)
        response = api_all.client.service.GetAllAllowedCategoryTree(
            headerMessage=api_all.header
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_list(self, category_code):
        """
        Search products in the reference frame

        Example::

            response = api.products.get_product_list("13380D0501")

        :param category_code: code to filter products by category
        :type category_code: str

        :return: products corresponding to research
        :rtype: dict
        """
        filters = self.api.factory.ProductFilter(category_code)

        response = self.api.client.service.GetProductList(
            headerMessage=self.api.header,
            productFilter=filters,
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_model_list(self, category=None):
        """
        Model categories allocated to the seller.

        :param category: category code to filter results
        :type category: str

        Examples::

            response = api.products.get_model_list()

            response = api.products.get_model_list("13380D0501")

        :return: models and mandatory model properties
        :rtype: dict
        """
        response = self.api.client.service.GetModelList(
            headerMessage=self.api.header,
            modelFilter=category
        )
        return serialize_object(response, dict)

    # TODO find a way to call it.
    @auto_refresh_token
    def get_all_model_list(self):
        """
        .. warning::
            Doesn't work at the moment.

        Model categories opened on marketplace.
        Example::

            response = api.products.get_all_model_list()

        :return: models and mandatory model properties
        :rtype: dict
        """
        # api_all = Connection('AllData', 'pa$$word')
        # response = api_all.client.service.GetAllModelList(
        #     headerMessage=api_all.header,
        # )
        # return serialize_object(response, dict)
        pass

    @auto_refresh_token
    def get_brand_list(self):
        """
        Complete list of the brands

        Example::

            response = api.products.get_brand_list()

        :return: all brands
        :rtype: dict
        """
        response = self.api.client.service.GetBrandList(
            headerMessage=self.api.header,
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def submit_product_package(self, products_dict, url):
        """
        To ask for the creation of products.

        :param products_dict: products as you can see on tests/samples/products/products_to_submit.json
        :type products_dict: dict

        :param url: url to upload offers package
        :type url: str


        Example::

            response = api.products.submit_product_package(
                products_dict={"Product":
                  [
                    {
                      "-BrandName": "Deeluxe",
                      "-SellerProductFamily": "SOJ50874",
                      "-SellerProductColorName": "Bleu Délavé",
                      "-Size": "38/36",
                      "-Description": "Marque Deeluxe, Modèle Tanner Snow Bleu, Jeans Coupe Droite Homme, Couleur Bleu Délavé, 100% Coton , Taille 38",
                      "-LongLabel": "Nudie Average Joe organic vacation worn Jeans",
                      "-Model": "SOUMISSION CREATION PRODUITS_MK",
                      "-ProductKind": "Variant",
                      "-CategoryCode": "0R050A01",
                      "-SellerProductId": "120905783",
                      "-ShortLabel": "Jeans Deeluxe Tanner Snow Bleu",
                      "-EncodedMarketingDescription": "RGVzY3JpcHRpb24gcXVpIGNvbnRpZW50IGR1IDxzdHJvbmc+SFRNTDwvc3Ryb25nPg==",
                      "Product.EanList": {
                        "ProductEan": { "-Ean": "3606918243767" }
                      },
                      "Product.ModelProperties": {
                        "x:String": [
                          {
                            "-x:Key": "Genre",
                            "#text": "Homme - Garçon"
                          },
                          {
                            "-x:Key": "Type de public",
                            "#text": "Adulte"
                          }
                        ]
                      },
                      "Product.Pictures": {
                        "ProductImage": [
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-1.jpg" },
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-2.jpg" },
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-3.jpg" },
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-4.jpg" }
                        ]
                      }
                    },
                    {
                      "-BrandName": "Deeluxe",
                      "-SellerProductFamily": "SOJ50874",
                      "-SellerProductColorName": "Bleu Délavé",
                      "-Size": "36/34",
                      "-Description": "Nudie Average Joe organic vacation worn Jeans Droite Homme 100% Organic",
                      "-LongLabel": "Jeans Deeluxe Tanner Snow Bleu",
                      "-Model": "SOUMISSION CREATION PRODUITS_MK",
                      "-ProductKind": "Variant",
                      "-CategoryCode": "0R050A01",
                      "-SellerProductId": "120905784",
                      "-ShortLabel": "Jeans Deeluxe Tanner Snow Bleu",
                      "-EncodedMarketingDescription": "RGVzY3JpcHRpb24gcXVpIGNvbnRpZW50IGR1IDxzdHJvbmc+SFRNTDwvc3Ryb25nPg==",
                      "Product.EanList": {
                        "ProductEan": { "-Ean": "3606918243774" }
                      },
                      "Product.ModelProperties": {
                        "x:String": [
                          {
                            "-x:Key": "Genre",
                            "#text": "Homme - Garçon"
                          },
                          {
                            "-x:Key": "Type de public",
                            "#text": "Adulte"
                          }
                        ]
                      },
                      "Product.Pictures": {
                        "ProductImage": [
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-1.jpg" },
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-2.jpg" },
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-3.jpg" },
                          { "-Uri": "http://cdn.sojeans.com/products/406x538/2710-jeans-deeluxe-tanner-4.jpg" }
                        ]
                      }
                    }
                  ]
                },
                url="path_to_upload.com"
            )

        :return: the id of package or -1
        :rtype: int
        """
        # get url.
        package_url = generate_package_url(products_dict, url)

        # Create request attribute.
        product_package = {'ZipFileFullPath': package_url}

        # Send request.
        response = self.api.client.service.SubmitProductPackage(
            headerMessage=self.api.header,
            productPackageRequest=product_package
        )
        return serialize_object(response, dict)

    # TODO find why it doesn't work.
    @auto_refresh_token
    def get_product_package_submission_result(self, filters={}):
        """
        Progress status of a product import.

        :param filters: (ex: package id)
        :type filters: dict
        :return: partial or complete report of package integration
        :rtype: dict
        """
        response = self.api.client.service.GetProductPackageSubmissionResult(
            headerMessage=self.api.header,
            productPackageFilter=filters
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_package_product_matching_file_data(self, package_id):
        """
        Information of the created products.

        :param package_id: package id to filter results
        :type package_id: str
        :return: information of the created products
        :rtype: dict
        """
        if package_id:
            response = self.api.client.service.GetProductPackageProductMatchingFileData(
                headerMessage=self.api.header,
                productPackageFilter={'PackageID': package_id}
            )
            return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_list_by_identifier(self, ean_list=[]):
        """
        Obtain details for a list of products

        :param ean_list: list of EAN to filter
        :type ean_list: list
        :return: complete list of products
        :rtype: dict
        """
        request = {'IdentifierType': 'EAN', 'ValueList': ean_list}
        response = self.api.client.service.GetProductListByIdentifier(
            headerMessage=self.api.header,
            identifierRequest=request
        )
        return serialize_object(response, dict)



