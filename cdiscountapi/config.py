# As zeep 3.3.1 doesn't support validation of the values accepted by an XSD
# type, we manually add it.

REFUND_INFORMATION = {
    'MotiveId': {
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
}


class Values(object):
    def __init__(self, *values):
        self.values = values


class Description(object):
    pass


class SellerRefundRequestDescription(Description):
    Mode = Values('Claim', 'Retraction')
    Motive = Values('VendorRejection',
                    'ClientCancellation',
                    'VendorRejectionAndClientCancellation',
                    'ClientClaim',
                    'VendorInitiatedRefund',
                    'ClientRetraction',
                    'NoClientWithDrawal'
                    'ProductStockUnavailable')

