# Project imports
from cdiscountapi.exceptions import ValidationError


class BaseValidator(object):
    required = set()
    optional = set()

    @classmethod
    def package_type(cls):
        return cls.__name__.split("Validator")[0]

    @classmethod
    def validate(cls, data):
        """
        Return the data if the keys are valid attributes
        """
        provided = set(data.keys())
        missing_required = cls.required - provided
        if len(missing_required) > 0:
            raise ValidationError(
                "Missing required attributes for {}: {}".format(
                    cls.package_type(), missing_required
                )
            )

        invalid_attributes = provided - cls.required - cls.optional
        if len(invalid_attributes) > 0:
            raise ValidationError(
                "These attributes are not valid: {}."
                " Please use only the following ones if necessary: {}".format(
                    invalid_attributes, cls.optional
                )
            )
        return data


class OfferValidator(BaseValidator):
    # Parameters common to PackageType "Full" and "StockAndPrice"
    required = {
        "ProductEan",
        "SellerProductId",
    }

    optional = {
        "Comment",
        "StrikedPrice",
        "PriceMustBeAligned",
        "MinimumPriceForPriceAlignment",
        "ProductPackagingUnit",
        "ProductPackagingValue",
        "BluffDeliveryMax",
        "DiscountList",
        "ShippingInformationList",
        # These parameters are only required when PackageType is "Full"
        "ProductCondition",
        "Price",
        "EcoPart",
        "Vat",
        "DeaTax",
        "Stock",
        "PreparationTime",
    }


class ProductValidator(BaseValidator):
    required = {
        "ShortLabel",
        "SellerProductId",
        "CategoryCode",
        "ProductKind",
        "Model",
        "LongLabel",
        "Description",
        "BrandName",
        "EanList",
        "Pictures",
    }

    optional = {
        "Width",
        "Weight",
        "Size",
        "SellerProductFamily",
        "SellerProductColorName",
        "ManufacturerPartNumber",
        "Length",
        "ISBN",
        "Height",
        "EncodedMarketingDescription",
        "ModelProperties",
        "Navigation",
    }


class DiscountComponentValidator(BaseValidator):
    required = {"DiscountValue", "Type", "StartDate", "EndDate"}


class ShippingInformationValidator(BaseValidator):
    required = {"ShippingCharges", "AdditionalShippingCharges", "DeliveryMode"}


class ProductEanValidator(BaseValidator):
    required = {"Ean"}


class ProductImageValidator(BaseValidator):
    required = {"Uri"}
