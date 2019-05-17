import os
from lxml import etree


# CONSTANTS
CDISCOUNT_WITHOUT_DATA = True if os.getenv('CDISCOUNT_WITHOUT_DATA') == '1' else False


# HELPER FUNCTIONS
def xpath(xml, tag, namespace):
    return xml.xpath('.//ns:{}'.format(tag),
                     namespaces={'ns': namespace})


# ASSERT FUNCTIONS
def assert_response_succeeded(response):
    assert response['ErrorList'] is None,\
        'ErrorList should be None but is {}'.format(response['ErrorList'])
    assert response['ErrorMessage'] is None,\
        'ErrorMessage should be None but is {}'.format(response['ErrorMessage'])
    assert response['OperationSuccess'] is True,\
        'OperationSuccess should be True but is {}'.format(response['OperationSuccess'])


def assert_response_failed(response):
    assert response['ErrorMessage'] is not None,\
        'ErrorMessage should not be None but is {}'.format(response['ErrorMessage'])
    assert response['OperationSuccess'] is False,\
        'OperationSuccess should be False but is {}'.format(response['OperationSuccess'])


def assert_xml_equal(result, expected, msg=''):
    result_dict = dict(result.items())
    expected_dict = dict(expected.items())
    assert set(result_dict.keys()) == set(expected_dict.keys())

    for k in result_dict:
        error_msg = msg + 'The key {} is not correct.'.format(k)
        assert result_dict[k] == expected_dict[k], error_msg


def assert_xml_files_equal(result_content, expected_content, pkg_type):
    """
    Raise an AssertionError if the content of the XML file doesn't match the expected content

    :param result_content: The content of the XML file
    :param expected_content: The content of the XML file that we expect
    :param pkg_type: 'Offer' or 'Product'
    :param tags: The tags to check in the file
    """
    def pkg_type_xpath(xml, tag):
        """
        Extract the selected nodes from the offer package or the product package XML.
        """
        namespace = {
            'Offer': ("clr-namespace:Cdiscount.Service.OfferIntegration.Pivot;"
                      "assembly=Cdiscount.Service.OfferIntegration"),
            'Product': ('clr-namespace:Cdiscount.Service.ProductIntegration.Pivot;'
                        'assembly=Cdiscount.Service.ProductIntegration')
        }
        return xpath(xml, tag, namespace[pkg_type])

    tags = {'Offer': ('Offer.ShippingInformationList',
                      'Offer.PriceAndDiscountList',
                      'Offer.PublicationList'),
            'Product': ('Product.EanList', 'Product.ModelProperties',
                        'Product.Pictures')}

    pkg_type_nodes = pkg_type_xpath(etree.XML(result_content), pkg_type)
    expected_pkg_type_nodes = pkg_type_xpath(etree.XML(expected_content), pkg_type)
    assert len(pkg_type_nodes) == len(expected_pkg_type_nodes)

    for i in range(len(pkg_type_nodes)):
        assert_xml_equal(pkg_type_nodes[i], expected_pkg_type_nodes[i])
        for tag in tags[pkg_type]:
            error_msg = "Error in {}. ".format(tag)
            result = pkg_type_xpath(pkg_type_nodes[i], tag)
            expected = pkg_type_xpath(expected_pkg_type_nodes[i], tag)
            assert len(result) == len(expected), error_msg
            for j in range(len(result)):
                assert_xml_equal(result[j], expected[j], msg=error_msg)


def discount_component():
    """
    A simple exemple of DiscountComponent used in Offers.xml
    """
    return {
        'DiscountValue': 5, 'Type': 1,
        'StartDate': '2019-04-15T00:00',
        'EndDate': '2019-05-15T00:00'
    }


def offer_publication_list():
    """
    A simple exemple of ids used in OfferPublicationList in Offers.xml
    """
    return [1, 16]
