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


class ModelEndpointSchema(object):
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
        'auth_method': 'str',
        'created_at': 'datetime',
        'created_by': 'str',
        'environment_id': 'str',
        'expose_method': 'str',
        'fqdn': 'str',
        'hostname': 'str',
        'id': 'str',
        'ingress_protocol': 'str',
        'object': 'str',
        'project_id': 'str',
        'service_weights': 'dict(str, int)',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'auth_method': 'auth_method',
        'created_at': 'created_at',
        'created_by': 'created_by',
        'environment_id': 'environment_id',
        'expose_method': 'expose_method',
        'fqdn': 'fqdn',
        'hostname': 'hostname',
        'id': 'id',
        'ingress_protocol': 'ingress_protocol',
        'object': 'object',
        'project_id': 'project_id',
        'service_weights': 'service_weights',
        'updated_at': 'updated_at'
    }

    readonly_attributes = {
        'created_at',
        'created_by',
        'fqdn',
        'id',
        'object',
        'project_id',
        'updated_at'
    }

    def __init__(self, auth_method=None, created_at=None, created_by=None, environment_id=None, expose_method='PRIVATE', fqdn=None, hostname=None, id=None, ingress_protocol=None, object='endpoint', project_id=None, service_weights=None, updated_at=None, **kwargs):  # noqa: E501
        """ModelEndpointSchema - a model defined in OpenAPI"""  # noqa: E501

        self._auth_method = None
        self._created_at = None
        self._created_by = None
        self._environment_id = None
        self._expose_method = None
        self._fqdn = None
        self._hostname = None
        self._id = None
        self._ingress_protocol = None
        self._object = None
        self._project_id = None
        self._service_weights = None
        self._updated_at = None
        self.discriminator = None

        if auth_method is not None:
            self.auth_method = auth_method
        self.environment_id = environment_id
        if expose_method is not None:
            self.expose_method = expose_method
        if hostname is not None:
            self.hostname = hostname
        self.ingress_protocol = ingress_protocol
        if service_weights is not None:
            self.service_weights = service_weights

    @classmethod
    def from_response(cls, auth_method=None, created_at=None, created_by=None, environment_id=None, expose_method='PRIVATE', fqdn=None, hostname=None, id=None, ingress_protocol=None, object='endpoint', project_id=None, service_weights=None, updated_at=None, **kwargs):  # noqa: E501
        """Instantiate ModelEndpointSchema from response"""  # noqa: E501
        self = cls.__new__(cls)

        self._auth_method = None
        self._created_at = None
        self._created_by = None
        self._environment_id = None
        self._expose_method = None
        self._fqdn = None
        self._hostname = None
        self._id = None
        self._ingress_protocol = None
        self._object = None
        self._project_id = None
        self._service_weights = None
        self._updated_at = None
        self.discriminator = None

        if auth_method is not None:
            self.auth_method = auth_method
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        self.environment_id = environment_id
        if expose_method is not None:
            self.expose_method = expose_method
        if fqdn is not None:
            self.fqdn = fqdn
        if hostname is not None:
            self.hostname = hostname
        if id is not None:
            self.id = id
        self.ingress_protocol = ingress_protocol
        if object is not None:
            self.object = object
        if project_id is not None:
            self.project_id = project_id
        if service_weights is not None:
            self.service_weights = service_weights
        if updated_at is not None:
            self.updated_at = updated_at
        return self

    @property
    def auth_method(self):
        """Gets the auth_method of this ModelEndpointSchema.  # noqa: E501


        :return: The auth_method of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._auth_method

    @auth_method.setter
    def auth_method(self, auth_method):
        """Sets the auth_method of this ModelEndpointSchema.


        :param auth_method: The auth_method of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """
        allowed_values = ["NONE", "TOKEN", "SSO"]  # noqa: E501
        if auth_method not in allowed_values:
            raise ValueError(
                "Invalid value for `auth_method` ({0}), must be one of {1}"  # noqa: E501
                .format(auth_method, allowed_values)
            )

        self._auth_method = auth_method

    @property
    def created_at(self):
        """Gets the created_at of this ModelEndpointSchema.  # noqa: E501


        :return: The created_at of this ModelEndpointSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelEndpointSchema.


        :param created_at: The created_at of this ModelEndpointSchema.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this ModelEndpointSchema.  # noqa: E501


        :return: The created_by of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelEndpointSchema.


        :param created_by: The created_by of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def environment_id(self):
        """Gets the environment_id of this ModelEndpointSchema.  # noqa: E501


        :return: The environment_id of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._environment_id

    @environment_id.setter
    def environment_id(self, environment_id):
        """Sets the environment_id of this ModelEndpointSchema.


        :param environment_id: The environment_id of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """
        if environment_id is None:
            raise ValueError("Invalid value for `environment_id`, must not be `None`")  # noqa: E501
        if environment_id is not None and not re.search(r'^([a-zA-Z0-9\-]+)$', environment_id):  # noqa: E501
            raise ValueError(r"Invalid value for `environment_id`, must be a follow pattern or equal to `/^([a-zA-Z0-9\-]+)$/`")  # noqa: E501

        self._environment_id = environment_id

    @property
    def expose_method(self):
        """Gets the expose_method of this ModelEndpointSchema.  # noqa: E501


        :return: The expose_method of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._expose_method

    @expose_method.setter
    def expose_method(self, expose_method):
        """Sets the expose_method of this ModelEndpointSchema.


        :param expose_method: The expose_method of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """
        allowed_values = ["PRIVATE", "PUBLIC"]  # noqa: E501
        if expose_method not in allowed_values:
            raise ValueError(
                "Invalid value for `expose_method` ({0}), must be one of {1}"  # noqa: E501
                .format(expose_method, allowed_values)
            )

        self._expose_method = expose_method

    @property
    def fqdn(self):
        """Gets the fqdn of this ModelEndpointSchema.  # noqa: E501

        Fully-qualified domain name  # noqa: E501

        :return: The fqdn of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._fqdn

    @fqdn.setter
    def fqdn(self, fqdn):
        """Sets the fqdn of this ModelEndpointSchema.

        Fully-qualified domain name  # noqa: E501

        :param fqdn: The fqdn of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """

        self._fqdn = fqdn

    @property
    def hostname(self):
        """Gets the hostname of this ModelEndpointSchema.  # noqa: E501

        Endpoint hostname. Must be valid DNS name and not match reserved keywords (auth, broker, consul, prom, pub, traefik).  # noqa: E501

        :return: The hostname of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """Sets the hostname of this ModelEndpointSchema.

        Endpoint hostname. Must be valid DNS name and not match reserved keywords (auth, broker, consul, prom, pub, traefik).  # noqa: E501

        :param hostname: The hostname of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """
        if hostname is not None and len(hostname) > 53:
            raise ValueError("Invalid value for `hostname`, length must be less than or equal to `53`")  # noqa: E501
        if hostname is not None and len(hostname) < 5:
            raise ValueError("Invalid value for `hostname`, length must be greater than or equal to `5`")  # noqa: E501
        if hostname is not None and not re.search(r'^(?!bdrk-)[a-z]([-a-z0-9]{3,61}[a-z0-9])(?<!-nb)$', hostname):  # noqa: E501
            raise ValueError(r"Invalid value for `hostname`, must be a follow pattern or equal to `/^(?!bdrk-)[a-z]([-a-z0-9]{3,61}[a-z0-9])(?<!-nb)$/`")  # noqa: E501

        self._hostname = hostname

    @property
    def id(self):
        """Gets the id of this ModelEndpointSchema.  # noqa: E501


        :return: The id of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelEndpointSchema.


        :param id: The id of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def ingress_protocol(self):
        """Gets the ingress_protocol of this ModelEndpointSchema.  # noqa: E501


        :return: The ingress_protocol of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._ingress_protocol

    @ingress_protocol.setter
    def ingress_protocol(self, ingress_protocol):
        """Sets the ingress_protocol of this ModelEndpointSchema.


        :param ingress_protocol: The ingress_protocol of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """
        if ingress_protocol is None:
            raise ValueError("Invalid value for `ingress_protocol`, must not be `None`")  # noqa: E501
        allowed_values = ["HTTP", "H2C"]  # noqa: E501
        if ingress_protocol not in allowed_values:
            raise ValueError(
                "Invalid value for `ingress_protocol` ({0}), must be one of {1}"  # noqa: E501
                .format(ingress_protocol, allowed_values)
            )

        self._ingress_protocol = ingress_protocol

    @property
    def object(self):
        """Gets the object of this ModelEndpointSchema.  # noqa: E501


        :return: The object of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this ModelEndpointSchema.


        :param object: The object of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """

        self._object = object

    @property
    def project_id(self):
        """Gets the project_id of this ModelEndpointSchema.  # noqa: E501


        :return: The project_id of this ModelEndpointSchema.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ModelEndpointSchema.


        :param project_id: The project_id of this ModelEndpointSchema.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def service_weights(self):
        """Gets the service_weights of this ModelEndpointSchema.  # noqa: E501


        :return: The service_weights of this ModelEndpointSchema.  # noqa: E501
        :rtype: dict(str, int)
        """
        return self._service_weights

    @service_weights.setter
    def service_weights(self, service_weights):
        """Sets the service_weights of this ModelEndpointSchema.


        :param service_weights: The service_weights of this ModelEndpointSchema.  # noqa: E501
        :type: dict(str, int)
        """

        self._service_weights = service_weights

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelEndpointSchema.  # noqa: E501


        :return: The updated_at of this ModelEndpointSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelEndpointSchema.


        :param updated_at: The updated_at of this ModelEndpointSchema.  # noqa: E501
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
        if not isinstance(other, ModelEndpointSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
