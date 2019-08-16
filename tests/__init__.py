import os
from lxml import etree
from pathlib import Path


# CONSTANTS
CDISCOUNT_WITHOUT_DATA = True if os.getenv("CDISCOUNT_WITHOUT_DATA") == "1" else False
SAMPLES_DIR = Path().joinpath("tests", "samples")


# HELPER FUNCTIONS
def xpath(xml, tag, namespace):
    return xml.xpath(".//ns:{}".format(tag), namespaces={"ns": namespace})


# ASSERT FUNCTIONS
def assert_response_succeeded(response):
    assert response["ErrorList"] is None, "ErrorList should be None but is {}".format(
        response["ErrorList"]
    )
    assert (
        response["ErrorMessage"] is None
    ), "ErrorMessage should be None but is {}".format(response["ErrorMessage"])
    assert (
        response["OperationSuccess"] is True
    ), "OperationSuccess should be True but is {}".format(response["OperationSuccess"])


def assert_response_failed(response):
    assert (
        response["ErrorMessage"] is not None
    ), "ErrorMessage should not be None but is {}".format(response["ErrorMessage"])
    assert (
        response["OperationSuccess"] is False
    ), "OperationSuccess should be False but is {}".format(response["OperationSuccess"])


def assert_dict_equal(d1, d2):
    # First we check the keys
    not_in_d1 = [k for k in d2.keys() if k not in d1.keys()]
    not_in_d2 = [k for k in d1.keys() if k not in d2.keys()]

    error_msg = ""
    if len(not_in_d2) > 0:
        error_msg += "In dict1 but not in dict2: "
        error_msg += ", ".join(not_in_d2)
    if len(not_in_d1) > 0:
        error_msg += "\nIn dict2 but not in dict1: "
        error_msg += ", ".join(not_in_d1)

    if len(error_msg):
        raise AssertionError(error_msg)

    # We now know all the keys are the same. We can check the values
    different_values = []
    for k in d1.keys():
        if d1[k] != d2[k]:
            different_values.append((k, d1[k], d2[k]))

    if len(different_values) > 0:
        msg = "Values are different:\n"
        raise AssertionError(
            msg + "\n".join("- {0}: '{1}' != '{2}'".format(*x) for x in different_values)
        )



def assert_xml_equal(result, expected, msg=""):
    result_dict = dict(result.items())
    expected_dict = dict(expected.items())
    assert set(result_dict.keys()) == set(expected_dict.keys())

    for k in result_dict:
        error_msg = msg + "The key {} is not correct.".format(k)
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
            "Offer": (
                "clr-namespace:Cdiscount.Service.OfferIntegration.Pivot;"
                "assembly=Cdiscount.Service.OfferIntegration"
            ),
            "Product": (
                "clr-namespace:Cdiscount.Service.ProductIntegration.Pivot;"
                "assembly=Cdiscount.Service.ProductIntegration"
            ),
        }
        return xpath(xml, tag, namespace[pkg_type])

    tags = {
        "Offer": (
            "Offer.ShippingInformationList",
            "Offer.PriceAndDiscountList",
            "Offer.PublicationList",
        ),
        "Product": ("Product.EanList", "Product.ModelProperties", "Product.Pictures"),
    }

    result_xml = etree.XML(result_content)
    expected_xml = etree.XML(expected_content)

    # Check the attributes "Capacity"
    if pkg_type == "Product":
        product_collection = pkg_type_xpath(
            result_xml,
            "ProductCollection"
        )[0]
        expected_product_collection = pkg_type_xpath(
            expected_xml,
            "ProductCollection"
        )[0]

        product_collection.get('Capacity') == expected_product_collection.get('Capacity')

    # Attributes of the node OfferPackage
    # assert dict(result_xml.items()) == dict(expected_xml.items())
    assert_dict_equal(dict(result_xml.items()), dict(expected_xml.items()))

    # Content of the offer
    pkg_type_nodes = pkg_type_xpath(result_xml, pkg_type)
    expected_pkg_type_nodes = pkg_type_xpath(expected_xml, pkg_type)
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
        "DiscountValue": 5,
        "Type": 1,
        "StartDate": "2019-04-15T00:00",
        "EndDate": "2019-05-15T00:00",
    }


def offer_publication_list():
    """
    A simple exemple of ids used in OfferPublicationList in Offers.xml
    """
    return [1, 16]
