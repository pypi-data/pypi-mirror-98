import uuid
from unittest import TestCase

import pytest

from cloudshell.shell.standards.autoload_generic_models import (
    GenericChassis,
    GenericModule,
    GenericPort,
    GenericResourceModel,
    GenericSubModule,
)


class TestNetworkingResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ["CS_Switch"]

    @property
    def entities(self):
        class _NetworkingEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = GenericPort

        return _NetworkingEntities


def _create_resource():
    """Creates a resource.

    Resource structure:
    Chassis1 Module1  Sub Module1-1  Port1-1-1
                      Sub Module1-2  Port1-2-1
                                     Port1-2-2
                      Port 1-3
             Module2  Sub Module2-1
                      Sub Module2-2
                      Port 2-3
             Module3  Sub Module3-1
             Module4
    """
    port_1_1_1 = GenericPort("1-1-1")
    port_1_2_1 = GenericPort("1-2-1")
    port_1_2_1.model_name = "port-1-2-1"
    port_1_2_2 = GenericPort("1-2-2")
    port_1_2_2.model_name = "port-1-2-2"
    port_1_3 = GenericPort("1-3")
    port_1_3.model_name = "port-1-3"
    port_2_3 = GenericPort("2-3")
    port_2_3.model_name = "port-2-3"

    sub_module1_1 = GenericSubModule("1")
    sub_module1_1.model = "submodule1-1 model"
    sub_module1_1.connect_port(port_1_1_1)

    sub_module1_2 = GenericSubModule("2")
    sub_module1_2.model = "submodule1-2 model"
    sub_module1_2.connect_port(port_1_2_1)
    sub_module1_2.connect_port(port_1_2_2)

    sub_module2_1 = GenericSubModule("1")
    sub_module2_1.model = "submodule2-1 model"

    sub_module2_2 = GenericSubModule("2")
    sub_module2_2.model = "submodule2-2 model"

    sub_module3_1 = GenericSubModule("1")
    sub_module3_1.model = "submodule3-1 model"

    module1 = GenericModule("1")
    module1.model = "module1 model"
    module1.connect_sub_module(sub_module1_1)
    module1.connect_sub_module(sub_module1_2)
    module1.connect_port(port_1_3)

    module2 = GenericModule("2")
    module2.model = "module2 model"
    module2.connect_sub_module(sub_module2_1)
    module2.connect_sub_module(sub_module2_2)
    module2.connect_port(port_2_3)

    module3 = GenericModule("3")
    module3.model = "module3 model"
    module3.connect_sub_module(sub_module3_1)

    module4 = GenericModule("4")
    module4.model = "module4 model"

    chassis = GenericChassis("1")
    chassis.connect_module(module1)
    chassis.connect_module(module2)
    chassis.connect_module(module3)
    chassis.connect_module(module4)

    resource = TestNetworkingResourceModel("resource name", "shell name", "CS_Switch")
    resource.connect_chassis(chassis)
    return resource


@pytest.fixture()
def resource():
    return _create_resource()


class TestAutoloadDetailsBuilderFiltering(TestCase):
    def setUp(self):
        self._resource = _create_resource()

    def test_filtering_empty_modules(self):
        expected_resource_names = {
            "Chassis 1",
            "Module 1",
            "SubModule 1",
            "Port 1-1-1",
            "SubModule 2",
            "Port 1-2-1",
            "Port 1-2-2",
            "Port 1-3",
            "Module 2",
            "Port 2-3",
        }

        details = self._resource.build(filter_empty_modules=True)
        resource_names = {resource.name for resource in details.resources}
        self.assertEqual(resource_names, expected_resource_names)

    def test_by_default_not_filter_modules(self):
        expected_resource_names = {
            "Module 4",
            "Port 1-1-1",
            "SubModule 1",
            "Module 3",
            "Module 2",
            "Port 1-2-2",
            "Port 1-2-1",
            "Port 1-3",
            "SubModule 2",
            "SubModule 1",
            "Module 1",
            "SubModule 1",
            "Chassis 1",
            "SubModule 2",
            "Port 2-3",
        }
        details = self._resource.build()
        resource_names = {resource.name for resource in details.resources}
        self.assertEqual(resource_names, expected_resource_names)


def test_autoload_details_builder_with_cs_id(resource):
    cs_resource_id = uuid.uuid4()
    resource.cs_resource_id = cs_resource_id
    structure = resource.build(use_new_unique_id=True)

    unique_ids = [resource.unique_identifier for resource in structure.resources]
    assert len(set(unique_ids)) == len(unique_ids), "Not all unique ids are unique"
