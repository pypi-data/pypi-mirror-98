#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
from typing import Any
from typing import Optional

from ruamel.yaml import YAML

import cr_api_client.core_api_client as core_api_client


#
# generic method to launch API operation on a target simulation
#


def _simulation_execute_operation(
    operation: str,
    id_simulation: int,
    operation_status: str,
    optional_param: Optional[Any] = None,
) -> str:

    print(
        "[+] Going to execute operation '{}' on simulation ID '{}'".format(
            operation, id_simulation
        )
    )

    # Build URI
    core_api_client.execute_operation_simulation(
        id_simulation, operation, optional_param=optional_param
    )

    # Wait for the operation to be completed in backend
    current_status = ""
    result = ""
    while True:
        # Sleep before next iteration
        time.sleep(2)

        print(
            "    [+] Currently executing operation '{}' on "
            "simulation ID '{}'...".format(operation, id_simulation)
        )

        simulation_dict = core_api_client.fetch_simulation(id_simulation)

        current_status = simulation_dict["status"]

        if current_status == "ERROR":
            error_message = simulation_dict["error_msg"]
            raise Exception(
                "Error during simulation operation: '{}'".format(error_message)
            )
        elif current_status != operation_status:
            # Operation has ended
            break

    print(
        "[+] Operation '{}' on simulation ID '{}' was correctly executed".format(
            operation, id_simulation
        )
    )
    print("[+] Current simulation status: '{}'".format(current_status))

    return result


#
# simulation creation helper
#


def _simu_create_validate_yaml_file(yaml_configuration_file: str) -> None:
    if os.path.exists(yaml_configuration_file) is not True:
        raise Exception(
            "The provided YAML configuration path does not exist: '{}'".format(
                yaml_configuration_file
            )
        )

    if os.path.isfile(yaml_configuration_file) is not True:
        raise Exception(
            "The provided YAML configuration path is not a file: '{}'".format(
                yaml_configuration_file
            )
        )

    if os.access(yaml_configuration_file, os.R_OK) is not True:
        raise Exception(
            "The provided YAML configuration file is not readable: '{}'".format(
                yaml_configuration_file
            )
        )


def _simu_create_read_yaml_file(yaml_configuration_file: str) -> str:
    with open(yaml_configuration_file, "r") as fd:
        yaml_content = fd.read()
        return yaml_content


def simu_create(architecture_file: str) -> int:
    """Process YAML configuration file and request core API to create a
    new simulation.

    """

    # Validate YAML configuration file
    _simu_create_validate_yaml_file(architecture_file)

    # Open and read YAML configuration file
    yaml_content = _simu_create_read_yaml_file(architecture_file)

    # Parse YAML configuration
    # We use ruamel.yaml because it keeps anchors and
    # aliases in memory. It is very convenient when the simulation
    # is stored/fetched (references are kept!)
    loader = YAML(typ="rt")
    network_structure = loader.load(yaml_content)

    if "name" not in network_structure:
        raise Exception(
            "Their should be a 'name' element in the YAML configuration file"
        )
    name = network_structure["name"]

    if "nodes" not in network_structure:
        raise Exception(
            "Their should be a 'nodes' structure in the YAML configuration file"
        )

    if "links" not in network_structure:
        raise Exception(
            "Their should be a 'links' structure in the YAML configuration file"
        )

    simulation_dict = {"name": name, "network": network_structure}

    id_simulation = core_api_client.create_simulation(simulation_dict)

    # Prepare disk resources
    _simulation_execute_operation("prepare", id_simulation, "PREPARING")

    return id_simulation


#
# 'simu_run' simulation
#
def simu_run(id_simulation: int, use_install_time: bool = False) -> None:
    # Check that no other simulation is running
    simulation_list = core_api_client.fetch_simulations()
    for simulation in simulation_list:
        if simulation["status"] == "RUNNING":
            raise Exception(
                "Cannot run a new simulation, as the simulation '{}' is "
                "already running".format(simulation["id"])
            )

    # Initiate the simulation
    _simulation_execute_operation(
        "start", id_simulation, "STARTING", optional_param=use_install_time
    )


#
# 'simu_pause' simulation
#
def simu_pause(id_simulation: int) -> None:
    _simulation_execute_operation("pause", id_simulation, "PAUSING")


#
# 'simu_unpause' simulation
#
def simu_unpause(id_simulation: int) -> None:
    _simulation_execute_operation("unpause", id_simulation, "UNPAUSING")


#
# 'simu_halt' simulation
#
def simu_halt(id_simulation: int) -> None:
    _simulation_execute_operation("stop", id_simulation, "STOPPING")


#
# 'simu_destroy' simulation
#
def simu_destroy(id_simulation: int) -> None:
    _simulation_execute_operation("destroy", id_simulation, "STOPPING")


#
# 'simu_clone' simulation
#
def simu_clone(id_simulation: int) -> int:
    id_new_simulation = _simulation_execute_operation("clone", id_simulation, "CLONING")
    return id_new_simulation


#
# 'simu_tap' simulation
#
def simu_tap(id_simulation: int, iface: str) -> None:
    core_api_client.tap_simulation(id_simulation, iface)


#
# 'simu_untap' simulation
#
def simu_untap(id_simulation: int, iface: str) -> None:
    core_api_client.untap_simulation(id_simulation, iface)


#
# 'simu_delete' simulation
#
def simu_delete(id_simulation: int) -> None:
    simulation_dict = core_api_client.fetch_simulation(id_simulation)
    simulation_status = simulation_dict["status"]

    if simulation_status == "RUNNING":
        _simulation_execute_operation("destroy", id_simulation, "STOPPING")

    _simulation_execute_operation("delete_snapshots", id_simulation, "STOPPING")

    core_api_client.delete_simulation(id_simulation)


#
# 'simu_status' simulation
#
def simu_status(id_simulation: int) -> str:
    # Check that no other simulation is running
    return core_api_client.get_simulation_status(id_simulation)


#
# 'simu_snap' simulation
#
def simu_snap(id_simulation: int) -> str:
    yaml: str = core_api_client.snapshot_simulation(id_simulation)

    print(f"[+] Starting the snaphot of simulation {id_simulation}...")
    while simu_status(id_simulation) != "SNAPSHOT":
        time.sleep(1)
    print("[+] Snapshot process has started")

    while simu_status(id_simulation) != "RUNNING":
        print("  [+] Snapshot in progress...")
        time.sleep(1)
    return yaml
