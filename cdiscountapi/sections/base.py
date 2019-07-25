# -*- coding: utf-8 -*-
"""
    cdiscountapi.sections.base
    --------------------------

    Base class for the different section classes

    :copyright: © 2019 Alexandria
"""


from zeep.helpers import serialize_object


class BaseSection(object):
    def __init__(self, api):
        self.api = api
        self.arrays_factory = self.api.client.type_factory(
            "http://schemas.microsoft.com/2003/10/Serialization/Arrays"
        )

    def array_of(self, type_name, sequence):
        """
        Cast the sequence into an array of the given type.

        The arrays are defined in the XSD file
        (cf http://schemas.microsoft.com/2003/10/Serialization/Arrays)
        (cf https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-ipamm/38d7c101-385d-4180-bb95-983955f41e19) ?
        """
        valid_type_names = (
            "int",
            "string",
            "long",
            "KeyValueOfstringArrayOfstringty7Ep6D1",
            "KeyValueOfintstring",
        )

        if type_name not in valid_type_names:
            raise TypeError(
                "Invalid type_name. "
                "Please choose between {}".format(valid_type_names)
            )

        array = getattr(self.arrays_factory, "ArrayOf{}".format(type_name))(sequence)
        return serialize_object(array, dict)

    def update_with_valid_array_type(self, record, keys_to_cast):
        """
        Update the dictionary with the array having the valid type

        :param dict record: The dictionary to update
        :param dict keys_to_cast: The dictionary specifying what keys to convert and what types

        Example::

            section = BaseSection(api)
            new_record = section.update_with_valid_array_type(
                {'DepositIdList': [1, 2, 3], 'PageSize': 10},
                {'DepositIdList': 'int'}
            )

        :returns: The updated dictionary with the valid array type

        """
        new_record = record.copy()
        for key, type_name in keys_to_cast.items():
            if key in new_record:
                new_record[key] = self.array_of(type_name, new_record[key])
        return new_record
