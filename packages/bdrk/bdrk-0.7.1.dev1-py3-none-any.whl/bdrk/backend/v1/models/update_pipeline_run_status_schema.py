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


class UpdatePipelineRunStatusSchema(object):
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
        'status': 'str',
        'timestamp': 'datetime'
    }

    attribute_map = {
        'status': 'status',
        'timestamp': 'timestamp'
    }

    readonly_attributes = {
    }

    def __init__(self, status=None, timestamp=None, **kwargs):  # noqa: E501
        """UpdatePipelineRunStatusSchema - a model defined in OpenAPI"""  # noqa: E501

        self._status = None
        self._timestamp = None
        self.discriminator = None

        self.status = status
        if timestamp is not None:
            self.timestamp = timestamp

    @classmethod
    def from_response(cls, status=None, timestamp=None, **kwargs):  # noqa: E501
        """Instantiate UpdatePipelineRunStatusSchema from response"""  # noqa: E501
        self = cls.__new__(cls)

        self._status = None
        self._timestamp = None
        self.discriminator = None

        return self

    @property
    def status(self):
        """Gets the status of this UpdatePipelineRunStatusSchema.  # noqa: E501


        :return: The status of this UpdatePipelineRunStatusSchema.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this UpdatePipelineRunStatusSchema.


        :param status: The status of this UpdatePipelineRunStatusSchema.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["Accepted", "Rejected", "Queued", "Running", "Failed", "Succeeded", "Unknown", "Stopping", "Stopped"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def timestamp(self):
        """Gets the timestamp of this UpdatePipelineRunStatusSchema.  # noqa: E501


        :return: The timestamp of this UpdatePipelineRunStatusSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this UpdatePipelineRunStatusSchema.


        :param timestamp: The timestamp of this UpdatePipelineRunStatusSchema.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

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
        if not isinstance(other, UpdatePipelineRunStatusSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
