# coding: utf-8

"""
    Bedrock

    API documentation for Bedrock platform  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ProjectSchema(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict):       The key is attribute name
                                  and the value is attribute type.
      attribute_map (dict):       The key is attribute name
                                  and the value is json key in definition.
      readonly_attributes (dict): Set of readonly attributes (will not be
                                  serialised in request body).
    """
    openapi_types = {
        'created_at': 'datetime',
        'created_by': 'UserSchema',
        'description': 'str',
        'public_id': 'str',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'created_at': 'created_at',
        'created_by': 'created_by',
        'description': 'description',
        'public_id': 'public_id',
        'updated_at': 'updated_at'
    }

    readonly_attributes = {
        'created_at',
        'created_by',
        'updated_at'
    }

    def __init__(self, created_at=None, created_by=None, description=None, public_id=None, updated_at=None, **kwargs):  # noqa: E501
        """ProjectSchema - a model defined in OpenAPI"""  # noqa: E501

        self._created_at = None
        self._created_by = None
        self._description = None
        self._public_id = None
        self._updated_at = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.public_id = public_id

    @classmethod
    def from_response(cls, created_at=None, created_by=None, description=None, public_id=None, updated_at=None, **kwargs):  # noqa: E501
        """Instantiate ProjectSchema from response"""  # noqa: E501
        self = cls.__new__(cls)

        self._created_at = None
        self._created_by = None
        self._description = None
        self._public_id = None
        self._updated_at = None
        self.discriminator = None

        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if description is not None:
            self.description = description
        self.public_id = public_id
        if updated_at is not None:
            self.updated_at = updated_at
        return self

    @property
    def created_at(self):
        """Gets the created_at of this ProjectSchema.  # noqa: E501


        :return: The created_at of this ProjectSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ProjectSchema.


        :param created_at: The created_at of this ProjectSchema.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this ProjectSchema.  # noqa: E501


        :return: The created_by of this ProjectSchema.  # noqa: E501
        :rtype: UserSchema
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ProjectSchema.


        :param created_by: The created_by of this ProjectSchema.  # noqa: E501
        :type: UserSchema
        """

        self._created_by = created_by

    @property
    def description(self):
        """Gets the description of this ProjectSchema.  # noqa: E501


        :return: The description of this ProjectSchema.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ProjectSchema.


        :param description: The description of this ProjectSchema.  # noqa: E501
        :type: str
        """
        if description is not None and len(description) > 150:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `150`")  # noqa: E501

        self._description = description

    @property
    def public_id(self):
        """Gets the public_id of this ProjectSchema.  # noqa: E501


        :return: The public_id of this ProjectSchema.  # noqa: E501
        :rtype: str
        """
        return self._public_id

    @public_id.setter
    def public_id(self, public_id):
        """Sets the public_id of this ProjectSchema.


        :param public_id: The public_id of this ProjectSchema.  # noqa: E501
        :type: str
        """
        if public_id is None:
            raise ValueError("Invalid value for `public_id`, must not be `None`")  # noqa: E501
        if public_id is not None and len(public_id) > 100:
            raise ValueError("Invalid value for `public_id`, length must be less than or equal to `100`")  # noqa: E501
        if public_id is not None and len(public_id) < 1:
            raise ValueError("Invalid value for `public_id`, length must be greater than or equal to `1`")  # noqa: E501
        if public_id is not None and not re.search(r'^[A-Za-z0-9_.-]{1,100}$', public_id):  # noqa: E501
            raise ValueError(r"Invalid value for `public_id`, must be a follow pattern or equal to `/^[A-Za-z0-9_.-]{1,100}$/`")  # noqa: E501

        self._public_id = public_id

    @property
    def updated_at(self):
        """Gets the updated_at of this ProjectSchema.  # noqa: E501


        :return: The updated_at of this ProjectSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ProjectSchema.


        :param updated_at: The updated_at of this ProjectSchema.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ProjectSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
