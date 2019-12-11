# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

# Python imports
from shutil import make_archive
from tempfile import gettempdir
import zipfile
from pathlib import Path

# Third-party imports
import pytest

# Project imports
from . import (
    SAMPLES_DIR,
    assert_response_succeeded,
    assert_xml_files_equal,
    discount_component,
    offer_publication_list,
)
from cdiscountapi.sections.offers import Offers


# HELPERS
def assert_offer_package_is_valid(filename):
    z = zipfile.ZipFile(filename, "r")
    files = set(z.namelist())
    expected_files = {"Content/Offers.xml", "_rels/.rels", "[Content_Types].xml"}
    assert files == expected_files


@pytest.mark.skip(reason="timeout error unresolve by cdiscount")
@pytest.mark.vcr()
def test_get_offer_list(api):
    response = api.offers.get_offer_list()
    assert_response_succeeded(response)
    assert "OfferList" in response.keys()


@pytest.mark.vcr()
def test_get_offer_list_paginated(api):
    response = api.offers.get_offer_list_paginated(PageNumber=2)
    assert_response_succeeded(response)
    assert "OfferList" in response.keys()


@pytest.mark.vcr()
def test_generate_offer_package(valid_offer_package):
    # ---- BEFORE ----
    package_path = Path(gettempdir()) / "uploading_package"
    zip_file = package_path.with_suffix(".zip")
    # Check uploading_package.zip doesn't exist yet.
    assert not package_path.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    # valid_offer_package contains 2 valid offers for the offer package
    Offers.generate_offer_package("A good package", package_path, valid_offer_package)

    # ---- AFTER ----
    # Check uploading_package.zip exists now.
    assert not package_path.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open(SAMPLES_DIR.joinpath("offers", "Offers.xml"), "r") as f:
        expected = f.read()

    with zipfile.ZipFile(zip_file) as zf:
        created = zf.read("Content/Offers.xml").decode()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, "Offer")


@pytest.mark.vcr()
def test_generate_offer_package_with_nonexistent_directory(valid_offer_package):
    """
    When the parent of the package_path does not exist a FileNotFoundError
    Offers.generate_offer_package should raise a FileNotFoundError
    """
    package_path = Path("/nonexistent/dir/uploading_package")
    pytest.raises(
        FileNotFoundError,
        Offers.generate_offer_package,
        "A good package",
        package_path,
        valid_offer_package
    )


@pytest.mark.vcr()
def test_generate_offer_package_with_existing_package_name_and_overwrite_false(valid_offer_package):
    """
    When the package_path already exists and overwrite=False, Offers.generate_offer_package should
    raise a FileExistsError
    """
    package_path = Path(gettempdir()) / "uploading_package"
    package_path.mkdir()
    make_archive(str(package_path), "zip", package_path, base_dir=".")
    pytest.raises(
        FileExistsError,
        Offers.generate_offer_package,
        "A good package",
        package_path,
        valid_offer_package,
        overwrite=False
    )


@pytest.mark.vcr()
def test_generate_offer_package_with_existing_package_name_and_overwrite_true(valid_offer_package):
    """
    When the package_path already exists and overwrite=True, Offers.generate_offer_package should
    overwrite the package
    """
    package_path = Path(gettempdir()) / "uploading_package"
    package_path.mkdir()
    make_archive(str(package_path), "zip", package_path, base_dir=".")
    Offers.generate_offer_package(
        "A good package", package_path, valid_offer_package,
        overwrite=True
    )


@pytest.mark.vcr()
def test_generate_offer_package_with_discount(valid_offer_package):
    """
    When the key 'DiscountList' is in the offer for the package,
    Offers.generate_offer_package should generate the offer package with the
    node DiscountList in Offers.xml
    """
    # ---- BEFORE ----
    package_path = Path(gettempdir()) / "uploading_package"
    zip_file = package_path.with_suffix(".zip")
    # Check uploading_package doesn't exists yet.
    assert not package_path.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    # We add the DiscountList in the first offer
    valid_offer_package[0]["DiscountList"] = {
        "DiscountComponent": [discount_component()]
    }
    Offers.generate_offer_package("A good package", package_path, valid_offer_package)

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert not package_path.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open(SAMPLES_DIR.joinpath("offers", "Offers_with_discount.xml"), "r") as f:
        expected = f.read()

    with zipfile.ZipFile(zip_file) as zf:
        created = zf.read("Content/Offers.xml").decode()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, "Offer")


@pytest.mark.vcr()
def test_generate_offer_package_with_offer_publication_list(valid_offer_package):
    """
    When the argument 'offer_publication_list' is specified,
    Offers.generate_offer_package should generate the offer package with the
    node OfferPublicationList in Offers.xml
    """
    # ---- BEFORE ----
    package_path = Path(gettempdir()) / "uploading_package"
    zip_file = package_path.with_suffix(".zip")
    # Check uploading_package doesn't exists yet.
    assert not package_path.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    Offers.generate_offer_package(
        "A good package",
        package_path,
        valid_offer_package,
        offer_publication_list=offer_publication_list(),
    )

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert not package_path.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open(
        SAMPLES_DIR.joinpath("offers", "Offers_with_offer_publication_list.xml"),
        "r"
    ) as f:
        expected = f.read()

    with zipfile.ZipFile(zip_file) as zf:
        created = zf.read("Content/Offers.xml").decode()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, "Offer")


@pytest.mark.vcr()
def test_generate_offer_package_with_purge_and_replace(valid_offer_package):
    """
    When the argument 'purge_and_replace' is set to True,
    Offers.generate_offer_package should should set the attribute
    PurgeAndReplace in the node OfferPackage to True in Offers.xml
    """
    # ---- BEFORE ----
    package_path = Path(gettempdir()) / "uploading_package"
    zip_file = package_path.with_suffix(".zip")
    # Check uploading_package doesn't exists yet.
    assert not package_path.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    Offers.generate_offer_package(
        "A good package",
        package_path, valid_offer_package, purge_and_replace=True
    )

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert not package_path.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open(
        SAMPLES_DIR.joinpath("offers", "Offers_with_purge_and_replace.xml"),
        "r"
    ) as f:
        expected = f.read()

    with zipfile.ZipFile(zip_file) as zf:
        created = zf.read("Content/Offers.xml").decode()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, "Offer")


@pytest.mark.vcr()
def test_submit_offer_package(api):
    response = api.offers.submit_offer_package(
        url="https://www.myserver/uploading_package.zip"
    )
    assert_response_succeeded(response)
    assert "PackageId" in response.keys()


@pytest.mark.vcr()
def test_get_offer_package_submission_result(api):
    response = api.offers.get_offer_package_submission_result(541)
    assert_response_succeeded(response)
    assert "OfferLogList" in response.keys()
