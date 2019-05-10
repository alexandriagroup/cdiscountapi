# Project imports
from cdiscountapi.exceptions import ValidationError


class BaseValidator(object):
    required = set()
    optional = set()

    @classmethod
    def validate(self, data):
        """
        Return the data if the keys are valid attributes
        """
        provided = set(data.keys())
        missing_required = self.required - provided
        if len(missing_required) > 0:
            raise ValidationError("Missing required attributes: {}".format(
                missing_required))

        invalid_attributes = provided - self.required - self.optional
        if len(invalid_attributes) > 0:
            raise ValidationError("These attributes are not valid: {}."
                                  " Please use only the following ones if necessary: {}".format(
                invalid_attributes, self.optional))
        return data


class OfferValidator(BaseValidator):
    required = {'ProductEan', 'SellerProductId', 'ProductCondition',
                'Price', 'EcoPart', 'Vat', 'DeaTax', 'Stock',
                'PreparationTime'}

    optional = {'Comment', 'StrikedPrice', 'PriceMustBeAligned',
                'MinimumPriceForPriceAlignment', 'ProductPackagingUnit',
                'ProductPackagingValue', 'BluffDeliveryMax', 'DiscountList',
                'ShippingInformationList'}


class ProductValidator(BaseValidator):
    required = {'ShortLabel', 'SellerProductId', 'CategoryCode', 'ProductKind',
                'Model', 'LongLabel', 'Description', 'BrandName',
                'Product.EanList', 'Product.Pictures'}

    optional = {'Width', 'Weight', 'Size', 'SellerProductFamily',
                'SellerProductColorName', 'ManufacturerPartNumber', 'Length',
                'ISBN', 'Height', 'EncodedMarketingDescription',
                'Product.ModelProperties', 'Navigation'}


class DiscountComponentValidator(BaseValidator):
    required = {'DiscountValue', 'Type', 'StartDate', 'EndDate'}


class ShippingInformationValidator(BaseValidator):
    required = {'ShippingCharges', 'AdditionalShippingCharges', 'DeliveryMode'}
