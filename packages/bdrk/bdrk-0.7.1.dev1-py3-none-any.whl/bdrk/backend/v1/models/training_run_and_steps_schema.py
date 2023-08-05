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


class TrainingRunAndStepsSchema(object):
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
        'object': 'str',
        'run': 'TrainingPipelineRunSchema',
        'steps': 'list[TrainingRunStepSchema]'
    }

    attribute_map = {
        'object': 'object',
        'run': 'run',
        'steps': 'steps'
    }

    readonly_attributes = {
        'object',
        'run',
        'steps'
    }

    def __init__(self, object='trainingRunAndSteps', run=None, steps=None, **kwargs):  # noqa: E501
        """TrainingRunAndStepsSchema - a model defined in OpenAPI"""  # noqa: E501

        self._object = None
        self._run = None
        self._steps = None
        self.discriminator = None


    @classmethod
    def from_response(cls, object='trainingRunAndSteps', run=None, steps=None, **kwargs):  # noqa: E501
        """Instantiate TrainingRunAndStepsSchema from response"""  # noqa: E501
        self = cls.__new__(cls)

        self._object = None
        self._run = None
        self._steps = None
        self.discriminator = None

        if object is not None:
            self.object = object
        if run is not None:
            self.run = run
        if steps is not None:
            self.steps = steps
        return self

    @property
    def object(self):
        """Gets the object of this TrainingRunAndStepsSchema.  # noqa: E501


        :return: The object of this TrainingRunAndStepsSchema.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this TrainingRunAndStepsSchema.


        :param object: The object of this TrainingRunAndStepsSchema.  # noqa: E501
        :type: str
        """

        self._object = object

    @property
    def run(self):
        """Gets the run of this TrainingRunAndStepsSchema.  # noqa: E501


        :return: The run of this TrainingRunAndStepsSchema.  # noqa: E501
        :rtype: TrainingPipelineRunSchema
        """
        return self._run

    @run.setter
    def run(self, run):
        """Sets the run of this TrainingRunAndStepsSchema.


        :param run: The run of this TrainingRunAndStepsSchema.  # noqa: E501
        :type: TrainingPipelineRunSchema
        """

        self._run = run

    @property
    def steps(self):
        """Gets the steps of this TrainingRunAndStepsSchema.  # noqa: E501


        :return: The steps of this TrainingRunAndStepsSchema.  # noqa: E501
        :rtype: list[TrainingRunStepSchema]
        """
        return self._steps

    @steps.setter
    def steps(self, steps):
        """Sets the steps of this TrainingRunAndStepsSchema.


        :param steps: The steps of this TrainingRunAndStepsSchema.  # noqa: E501
        :type: list[TrainingRunStepSchema]
        """

        self._steps = steps

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
        if not isinstance(other, TrainingRunAndStepsSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
