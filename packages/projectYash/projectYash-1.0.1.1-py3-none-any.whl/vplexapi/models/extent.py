# coding: utf-8

"""
    VPlex REST API

    A definition for the next-gen VPlex API  # noqa: E501

    OpenAPI spec version: 0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Extent(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'application_consistent': 'str',
        'block_count': 'float',
        'block_size': 'float',
        'block_offset': 'float',
        'capacity': 'float',
        'health_indications': 'list[str]',
        'health_state': 'str',
        'io_status': 'str',
        'locality': 'str',
        'itls': 'list[str]',
        'operational_status': 'str',
        'storage_array_family': 'str',
        'storage_volume': 'str',
        'storage_volumetype': 'str',
        'system_id': 'str',
        'thin_capable': 'bool',
        'underlying_storage_block_size': 'float',
        'use': 'str',
        'used_by': 'list[str]',
        'vendor_specific_name': 'str'
    }

    attribute_map = {
        'name': 'name',
        'application_consistent': 'application_consistent',
        'block_count': 'block_count',
        'block_size': 'block_size',
        'block_offset': 'block_offset',
        'capacity': 'capacity',
        'health_indications': 'health_indications',
        'health_state': 'health_state',
        'io_status': 'io_status',
        'locality': 'locality',
        'itls': 'itls',
        'operational_status': 'operational_status',
        'storage_array_family': 'storage_array_family',
        'storage_volume': 'storage_volume',
        'storage_volumetype': 'storage_volumetype',
        'system_id': 'system_id',
        'thin_capable': 'thin-capable',
        'underlying_storage_block_size': 'underlying_storage_block_size',
        'use': 'use',
        'used_by': 'used_by',
        'vendor_specific_name': 'vendor_specific_name'
    }

    def __init__(self, name=None, application_consistent=None, block_count=None, block_size=None, block_offset=None, capacity=None, health_indications=None, health_state=None, io_status=None, locality=None, itls=None, operational_status=None, storage_array_family=None, storage_volume=None, storage_volumetype=None, system_id=None, thin_capable=None, underlying_storage_block_size=None, use=None, used_by=None, vendor_specific_name=None):  # noqa: E501
        """Extent - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._application_consistent = None
        self._block_count = None
        self._block_size = None
        self._block_offset = None
        self._capacity = None
        self._health_indications = None
        self._health_state = None
        self._io_status = None
        self._locality = None
        self._itls = None
        self._operational_status = None
        self._storage_array_family = None
        self._storage_volume = None
        self._storage_volumetype = None
        self._system_id = None
        self._thin_capable = None
        self._underlying_storage_block_size = None
        self._use = None
        self._used_by = None
        self._vendor_specific_name = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if application_consistent is not None:
            self.application_consistent = application_consistent
        if block_count is not None:
            self.block_count = block_count
        if block_size is not None:
            self.block_size = block_size
        if block_offset is not None:
            self.block_offset = block_offset
        if capacity is not None:
            self.capacity = capacity
        if health_indications is not None:
            self.health_indications = health_indications
        if health_state is not None:
            self.health_state = health_state
        if io_status is not None:
            self.io_status = io_status
        if locality is not None:
            self.locality = locality
        if itls is not None:
            self.itls = itls
        if operational_status is not None:
            self.operational_status = operational_status
        if storage_array_family is not None:
            self.storage_array_family = storage_array_family
        if storage_volume is not None:
            self.storage_volume = storage_volume
        if storage_volumetype is not None:
            self.storage_volumetype = storage_volumetype
        if system_id is not None:
            self.system_id = system_id
        if thin_capable is not None:
            self.thin_capable = thin_capable
        if underlying_storage_block_size is not None:
            self.underlying_storage_block_size = underlying_storage_block_size
        if use is not None:
            self.use = use
        if used_by is not None:
            self.used_by = used_by
        if vendor_specific_name is not None:
            self.vendor_specific_name = vendor_specific_name

    @property
    def name(self):
        """Gets the name of this Extent.  # noqa: E501


        :return: The name of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Extent.


        :param name: The name of this Extent.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def application_consistent(self):
        """Gets the application_consistent of this Extent.  # noqa: E501


        :return: The application_consistent of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._application_consistent

    @application_consistent.setter
    def application_consistent(self, application_consistent):
        """Sets the application_consistent of this Extent.


        :param application_consistent: The application_consistent of this Extent.  # noqa: E501
        :type: str
        """

        self._application_consistent = application_consistent

    @property
    def block_count(self):
        """Gets the block_count of this Extent.  # noqa: E501


        :return: The block_count of this Extent.  # noqa: E501
        :rtype: float
        """
        return self._block_count

    @block_count.setter
    def block_count(self, block_count):
        """Sets the block_count of this Extent.


        :param block_count: The block_count of this Extent.  # noqa: E501
        :type: float
        """

        self._block_count = block_count

    @property
    def block_size(self):
        """Gets the block_size of this Extent.  # noqa: E501


        :return: The block_size of this Extent.  # noqa: E501
        :rtype: float
        """
        return self._block_size

    @block_size.setter
    def block_size(self, block_size):
        """Sets the block_size of this Extent.


        :param block_size: The block_size of this Extent.  # noqa: E501
        :type: float
        """

        self._block_size = block_size

    @property
    def block_offset(self):
        """Gets the block_offset of this Extent.  # noqa: E501


        :return: The block_offset of this Extent.  # noqa: E501
        :rtype: float
        """
        return self._block_offset

    @block_offset.setter
    def block_offset(self, block_offset):
        """Sets the block_offset of this Extent.


        :param block_offset: The block_offset of this Extent.  # noqa: E501
        :type: float
        """

        self._block_offset = block_offset

    @property
    def capacity(self):
        """Gets the capacity of this Extent.  # noqa: E501


        :return: The capacity of this Extent.  # noqa: E501
        :rtype: float
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this Extent.


        :param capacity: The capacity of this Extent.  # noqa: E501
        :type: float
        """

        self._capacity = capacity

    @property
    def health_indications(self):
        """Gets the health_indications of this Extent.  # noqa: E501


        :return: The health_indications of this Extent.  # noqa: E501
        :rtype: list[str]
        """
        return self._health_indications

    @health_indications.setter
    def health_indications(self, health_indications):
        """Sets the health_indications of this Extent.


        :param health_indications: The health_indications of this Extent.  # noqa: E501
        :type: list[str]
        """

        self._health_indications = health_indications

    @property
    def health_state(self):
        """Gets the health_state of this Extent.  # noqa: E501


        :return: The health_state of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._health_state

    @health_state.setter
    def health_state(self, health_state):
        """Sets the health_state of this Extent.


        :param health_state: The health_state of this Extent.  # noqa: E501
        :type: str
        """

        self._health_state = health_state

    @property
    def io_status(self):
        """Gets the io_status of this Extent.  # noqa: E501


        :return: The io_status of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._io_status

    @io_status.setter
    def io_status(self, io_status):
        """Sets the io_status of this Extent.


        :param io_status: The io_status of this Extent.  # noqa: E501
        :type: str
        """

        self._io_status = io_status

    @property
    def locality(self):
        """Gets the locality of this Extent.  # noqa: E501


        :return: The locality of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._locality

    @locality.setter
    def locality(self, locality):
        """Sets the locality of this Extent.


        :param locality: The locality of this Extent.  # noqa: E501
        :type: str
        """

        self._locality = locality

    @property
    def itls(self):
        """Gets the itls of this Extent.  # noqa: E501


        :return: The itls of this Extent.  # noqa: E501
        :rtype: list[str]
        """
        return self._itls

    @itls.setter
    def itls(self, itls):
        """Sets the itls of this Extent.


        :param itls: The itls of this Extent.  # noqa: E501
        :type: list[str]
        """

        self._itls = itls

    @property
    def operational_status(self):
        """Gets the operational_status of this Extent.  # noqa: E501


        :return: The operational_status of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._operational_status

    @operational_status.setter
    def operational_status(self, operational_status):
        """Sets the operational_status of this Extent.


        :param operational_status: The operational_status of this Extent.  # noqa: E501
        :type: str
        """

        self._operational_status = operational_status

    @property
    def storage_array_family(self):
        """Gets the storage_array_family of this Extent.  # noqa: E501


        :return: The storage_array_family of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._storage_array_family

    @storage_array_family.setter
    def storage_array_family(self, storage_array_family):
        """Sets the storage_array_family of this Extent.


        :param storage_array_family: The storage_array_family of this Extent.  # noqa: E501
        :type: str
        """

        self._storage_array_family = storage_array_family

    @property
    def storage_volume(self):
        """Gets the storage_volume of this Extent.  # noqa: E501


        :return: The storage_volume of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._storage_volume

    @storage_volume.setter
    def storage_volume(self, storage_volume):
        """Sets the storage_volume of this Extent.


        :param storage_volume: The storage_volume of this Extent.  # noqa: E501
        :type: str
        """

        self._storage_volume = storage_volume

    @property
    def storage_volumetype(self):
        """Gets the storage_volumetype of this Extent.  # noqa: E501


        :return: The storage_volumetype of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._storage_volumetype

    @storage_volumetype.setter
    def storage_volumetype(self, storage_volumetype):
        """Sets the storage_volumetype of this Extent.


        :param storage_volumetype: The storage_volumetype of this Extent.  # noqa: E501
        :type: str
        """

        self._storage_volumetype = storage_volumetype

    @property
    def system_id(self):
        """Gets the system_id of this Extent.  # noqa: E501


        :return: The system_id of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """Sets the system_id of this Extent.


        :param system_id: The system_id of this Extent.  # noqa: E501
        :type: str
        """

        self._system_id = system_id

    @property
    def thin_capable(self):
        """Gets the thin_capable of this Extent.  # noqa: E501


        :return: The thin_capable of this Extent.  # noqa: E501
        :rtype: bool
        """
        return self._thin_capable

    @thin_capable.setter
    def thin_capable(self, thin_capable):
        """Sets the thin_capable of this Extent.


        :param thin_capable: The thin_capable of this Extent.  # noqa: E501
        :type: bool
        """

        self._thin_capable = thin_capable

    @property
    def underlying_storage_block_size(self):
        """Gets the underlying_storage_block_size of this Extent.  # noqa: E501


        :return: The underlying_storage_block_size of this Extent.  # noqa: E501
        :rtype: float
        """
        return self._underlying_storage_block_size

    @underlying_storage_block_size.setter
    def underlying_storage_block_size(self, underlying_storage_block_size):
        """Sets the underlying_storage_block_size of this Extent.


        :param underlying_storage_block_size: The underlying_storage_block_size of this Extent.  # noqa: E501
        :type: float
        """

        self._underlying_storage_block_size = underlying_storage_block_size

    @property
    def use(self):
        """Gets the use of this Extent.  # noqa: E501


        :return: The use of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._use

    @use.setter
    def use(self, use):
        """Sets the use of this Extent.


        :param use: The use of this Extent.  # noqa: E501
        :type: str
        """

        self._use = use

    @property
    def used_by(self):
        """Gets the used_by of this Extent.  # noqa: E501


        :return: The used_by of this Extent.  # noqa: E501
        :rtype: list[str]
        """
        return self._used_by

    @used_by.setter
    def used_by(self, used_by):
        """Sets the used_by of this Extent.


        :param used_by: The used_by of this Extent.  # noqa: E501
        :type: list[str]
        """

        self._used_by = used_by

    @property
    def vendor_specific_name(self):
        """Gets the vendor_specific_name of this Extent.  # noqa: E501


        :return: The vendor_specific_name of this Extent.  # noqa: E501
        :rtype: str
        """
        return self._vendor_specific_name

    @vendor_specific_name.setter
    def vendor_specific_name(self, vendor_specific_name):
        """Sets the vendor_specific_name of this Extent.


        :param vendor_specific_name: The vendor_specific_name of this Extent.  # noqa: E501
        :type: str
        """

        self._vendor_specific_name = vendor_specific_name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Extent, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Extent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
