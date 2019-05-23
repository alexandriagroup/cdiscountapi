import re
import os
import pytest

from ..sections.base import BaseSection


@pytest.mark.vcr()
def test_array_of(api):
    section = BaseSection(api)
    array_of_ints = section.array_of("int", [1, 2, 3])
    assert array_of_ints == {"int": [1, 2, 3]}


@pytest.mark.vcr()
def test_array_of_with_invalid_type(api):
    section = BaseSection(api)
    pytest.raises(TypeError, section.array_of, "invalid_type", [1, 2, 3])


@pytest.mark.vcr()
def test_update_with_valid_array_type(api):
    section = BaseSection(api)
    request = {"DepositIdList": [1, 2, 3], "PageSize": 10}

    new_request = section.update_with_valid_array_type(
        request, {"DepositIdList": "int"}
    )

    assert new_request == {"DepositIdList": {"int": [1, 2, 3]}, "PageSize": 10}
    assert request == {"DepositIdList": [1, 2, 3], "PageSize": 10}
