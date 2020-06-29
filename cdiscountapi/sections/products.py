# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.products
    ------------------------------

    Handles the products.

    :copyright: © 2019 Alexandria
"""

from tempfile import gettempdir

from zeep.helpers import serialize_object

from cdiscountapi.helpers import generate_package
from .base import BaseSection
from ..helpers import auto_refresh_token


class Products(BaseSection):
    """
    Allows to get information about products and submit new products on Cdiscount.

    Methods::

        get_all_allowed_category_tree()
        get_allowed_category_tree()
        get_product_list(category_code)
        get_model_list(category=category)
        get_all_model_list()
        get_brand_list()
        generate_product_package(package_name, products_list)
        submit_product_package(url)
        get_product_package_submission_result(package_ids=package_ids)
        get_product_package_product_matching_file_data(package_id)
        get_product_list_by_identifier(ean_list=ean_list)

    Operations are included in the Products API section.
    (https://dev.cdiscount.com/marketplace/?page_id=220)

    """

    @auto_refresh_token
    def get_allowed_category_tree(self):
        """
        Categories which are accessible to the seller.

        Usage::

            response = api.products.get_allowed_category_tree()

        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        """
        response = self.api.client.service.GetAllowedCategoryTree(
            headerMessage=self.api.header
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_all_allowed_category_tree(self):
        """
        All categories.

        Usage::

            response = api.products.get_all_allowed_category_tree()

        :return:  tree of the categories leaves of which are authorized for the integration of products and/or offers
        """
        from ..cdiscountapi import Connection

        api_all = Connection("AllData", "pa$$word", header_message=self.header)
        response = api_all.client.service.GetAllAllowedCategoryTree(
            headerMessage=api_all.header
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_list(self, category_code):
        """
        Search products in the reference frame.

        :param str category_code: code to filter products by category

        Usage::

            response = api.products.get_product_list("13380D0501")

        :return: products corresponding to research
        """
        filters = self.api.factory.ProductFilter(category_code)

        response = self.api.client.service.GetProductList(
            headerMessage=self.api.header, productFilter=filters
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_model_list(self, category=None):
        """
        Model categories allocated to the seller.

        :param str category: category code to filter results

        Usages::

            response = api.products.get_model_list()

            response = api.products.get_model_list("13380D0501")

        :return: models and mandatory model properties
        """
        categories = category if isinstance(category, (list, tuple)) else [category]
        model_filter = self.api.factory.ModelFilter(
            self.array_of('string', categories)
        )

        response = self.api.client.service.GetModelList(
            headerMessage=self.api.header, modelFilter=model_filter
        )
        return serialize_object(response, dict)

    # TODO find a way to call it.
    @auto_refresh_token
    def get_all_model_list(self):
        """
        .. warning::
            Doesn't work at the moment.

        Model categories opened on marketplace.

        Usage::

            response = api.products.get_all_model_list()

        :return: models and mandatory model properties
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

        Usage::

            response = api.products.get_brand_list()

        :return: all brands
        """
        response = self.api.client.service.GetBrandList(headerMessage=self.api.header)
        return serialize_object(response, dict)

    @staticmethod
    def generate_product_package(
            package_name, package_path, products_list, overwrite=True
    ):
        """
        Generate a zip product package as cdiscount wanted.

        :param str package_name: [mandatory] the full path to the offer package (without .zip)
        :param bool overwrite: [optional] Determine if an existing package is
        overwritten when a new one with the same name is created (default: True)
        :param list products_list:

            - Mandatory attributes:
                - BrandName *(str)*
                - Description *(str)*
                - LongLabel *(str)*
                - Model *(str)*
                - Navigation *(str)*
                - ProductKind *(str)*
                    - 'Variant'
                    - 'Standart'
                - SellerProductId *(str)*
                - ShortLabel *(str)*
            - Optional attributes:
                - Width *(int)*
                - Weight *(int)*
                - Length *(int)*
                - Height *(int)*
                - Size *(str)*
                - SellerProductFamily *(str)*
                - SellerProductColorName *(str)*
                - ManufacturerPartNumber *(str)*
                - ISBN *(str)*
                - EncodedMarketingDescription *(str)*

        Example::

            response = api.products.generate_product_package(products_list)

        """
        return generate_package(
            "product",
            package_path,
            {
                "Products": products_list,
                "Name": package_name,
            },
            overwrite=overwrite
        )

    @auto_refresh_token
    def submit_product_package(self, url):
        """
        To ask for the creation of products.
        It could included between 10K and 20K products by package.

        There is 2 ways to use it.

        1. You can generate a zip package with:
            api.products.generate_product_package(products_dict)

        2. You can generate the package yourself before uploading.

        Then you'll have to get an url to download zip package
        Finally, you can use submit_product_package(url)


        Examples::

            api.products.submit_product_package(url)

        :return: the id of package or -1

        """
        product_package = self.api.factory.ProductPackageRequest(url)

        # Send request.
        response = self.api.client.service.SubmitProductPackage(
            headerMessage=self.api.header, productPackageRequest=product_package
        )
        return serialize_object(response, dict)

    # TODO find why it doesn't work.
    @auto_refresh_token
    def get_product_package_submission_result(self, package_ids=None):
        """
        Progress status of a product import.

        :param long package_ids: PackageID

        Usage::

            response = api.products.get_product_package_submission_result(2154894)

        :return: partial or complete report of package integration
        """
        filters = self.api.factory.PackageFilter(package_ids)
        response = self.api.client.service.GetProductPackageSubmissionResult(
            headerMessage=self.api.header, productPackageFilter=filters
        )
        return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_package_product_matching_file_data(self, package_id):
        """
        Information of the created products.

        :param long package_id: package id to filter results

        Usage::

            response = api.products.get_product_package_product_matching_file_data(21454894)

        :return: information of the created products
        """
        if package_id:
            response = self.api.client.service.GetProductPackageProductMatchingFileData(
                headerMessage=self.api.header,
                productPackageFilter={"PackageID": package_id},
            )
            return serialize_object(response, dict)

    @auto_refresh_token
    def get_product_list_by_identifier(self, ean_list=[]):
        """
        Obtain details for a list of products

        :param list ean_list: list of EAN to filter

        Usage::

            response = api.products.get_product_list_by_identifier('2009863600561')

        :return: complete list of products
        """
        request = {"IdentifierType": "EAN", "ValueList": ean_list}
        response = self.api.client.service.GetProductListByIdentifier(
            headerMessage=self.api.header, identifierRequest=request
        )
        return serialize_object(response, dict)
