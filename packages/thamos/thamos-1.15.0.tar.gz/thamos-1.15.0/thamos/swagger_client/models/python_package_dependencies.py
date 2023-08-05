# coding: utf-8

"""
    Thoth User API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.6.0-dev

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class PythonPackageDependencies(object):
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
        "parameters": "object",
        "dependencies": "list[PythonPackageDependenciesDependencies]",
    }

    attribute_map = {"parameters": "parameters", "dependencies": "dependencies"}

    def __init__(self, parameters=None, dependencies=None):  # noqa: E501
        """PythonPackageDependencies - a model defined in Swagger"""  # noqa: E501
        self._parameters = None
        self._dependencies = None
        self.discriminator = None
        self.parameters = parameters
        self.dependencies = dependencies

    @property
    def parameters(self):
        """Gets the parameters of this PythonPackageDependencies.  # noqa: E501


        :return: The parameters of this PythonPackageDependencies.  # noqa: E501
        :rtype: object
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this PythonPackageDependencies.


        :param parameters: The parameters of this PythonPackageDependencies.  # noqa: E501
        :type: object
        """
        if parameters is None:
            raise ValueError(
                "Invalid value for `parameters`, must not be `None`"
            )  # noqa: E501

        self._parameters = parameters

    @property
    def dependencies(self):
        """Gets the dependencies of this PythonPackageDependencies.  # noqa: E501


        :return: The dependencies of this PythonPackageDependencies.  # noqa: E501
        :rtype: list[PythonPackageDependenciesDependencies]
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        """Sets the dependencies of this PythonPackageDependencies.


        :param dependencies: The dependencies of this PythonPackageDependencies.  # noqa: E501
        :type: list[PythonPackageDependenciesDependencies]
        """
        if dependencies is None:
            raise ValueError(
                "Invalid value for `dependencies`, must not be `None`"
            )  # noqa: E501

        self._dependencies = dependencies

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(PythonPackageDependencies, dict):
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
        if not isinstance(other, PythonPackageDependencies):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
