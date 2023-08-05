#!/usr/bin/python
# -*- coding: utf-8 -*-
import warnings

from cloudshell.shell.core.driver_context import (
    AutoLoadAttribute,
    AutoLoadDetails,
    AutoLoadResource,
)


class AutoloadDetailsBuilder(object):
    def __init__(
        self, resource_model, filter_empty_modules=False, use_new_unique_id=False
    ):
        """Autoload Details Builder.

        :param cloudshell.shell.standards.autoload_generic_models.GenericResourceModel resource_model:  # noqa: E501
        :param bool filter_empty_modules:
        :param bool use_new_unique_id: use CS resource Id for creating unique id
        """
        if not filter_empty_modules:
            # todo v2.0 - set filter_empty_modules=True by default
            warnings.warn(
                "Empty modules would be filtered by default in next major version",
                PendingDeprecationWarning,
            )
        if not use_new_unique_id:
            # todo v2.0 - always use CS Id for generating unique id
            warnings.warn(
                "CS resource Id would be used by default in next major version",
                PendingDeprecationWarning,
            )
        self.resource_model = resource_model
        self._filter_empty_modules = filter_empty_modules
        self._cs_resource_id = (
            resource_model.cs_resource_id if use_new_unique_id else None
        )

    def _build_branch(self, resource):
        """Build a branch.

        :param cloudshell.shell.standards.core.autoload.resource_model.AbstractResource resource: # noqa: E501
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        resource.shell_name = resource.shell_name or self.resource_model.shell_name
        relative_address = str(resource.relative_address)
        unique_identifier = get_unique_id(self._cs_resource_id, resource)

        autoload_details = AutoLoadDetails([], [])

        if relative_address:
            autoload_details.resources = [
                AutoLoadResource(
                    model=resource.cloudshell_model_name,
                    name=resource.name,
                    relative_address=relative_address,
                    unique_identifier=unique_identifier,
                )
            ]

        autoload_details.attributes = [
            AutoLoadAttribute(
                relative_address=relative_address,
                attribute_name=str(name),
                attribute_value=str(value),
            )
            for name, value in resource.attributes.items()
            if value is not None
        ]
        for child_resource in resource.extract_sub_resources():
            # skip modules and sub modules without children
            if self._filter_empty_modules and is_module_without_children(
                child_resource
            ):
                continue
            child_details = self._build_branch(child_resource)
            autoload_details.resources.extend(child_details.resources)
            autoload_details.attributes.extend(child_details.attributes)
        return autoload_details

    def build_details(self):
        """Build resource details.

        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self._build_branch(self.resource_model)


def get_unique_id(cs_resource_id, resource):
    """Get unique ID for the resource.

    If we have cs_resource_id use it for creating unique id.
    :type cs_resource_id: str
    :param cloudshell.shell.standards.core.autoload.resource_model.AbstractResource resource:  # noqa: E501
    :rtype: str
    """
    if cs_resource_id:
        unique_id = "{}+{}".format(cs_resource_id, resource.unique_identifier)
        unique_id = str(hash(unique_id))
    else:
        unique_id = str(resource.unique_identifier)
    return unique_id


def is_module_without_children(resource):
    from cloudshell.shell.standards.autoload_generic_models import (
        GenericModule,
        GenericSubModule,
    )

    children = resource.extract_sub_resources()
    if isinstance(resource, GenericSubModule):
        return not children
    elif isinstance(resource, GenericModule):
        return all(map(is_module_without_children, children))
    else:
        return False
