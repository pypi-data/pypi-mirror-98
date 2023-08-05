#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
from tempfile import TemporaryDirectory
from typing import Any

import requests

import cr_api_client.core_api_client as core_api_client


# Configuration access to Cyber Range endpoint
PROVISIONING_API_URL = "http://127.0.0.1:5003"
CA_CERT_PATH = None  # Expect a path to CA certs (see: https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None  # Expect a path to client cert (see: https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None  # Expect a path to client private key (see: https://requests.readthedocs.io/en/master/user/advanced/)


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def __get(route: str, **kwargs: str) -> Any:
    return requests.get(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __post(route: str, **kwargs: str) -> Any:
    return requests.post(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __put(route: str, **kwargs: str) -> Any:
    return requests.put(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __delete(route: str, **kwargs: str) -> Any:
    return requests.delete(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


# -------------------------------------------------------------------------- #


#
# 'provisioning' related functions
#
def _provisioning_generate_validate_input_file(input_file: str) -> None:
    if os.path.exists(input_file) is not True:
        raise Exception("The provided path does not exist: '{}'".format(input_file))

    if os.path.isfile(input_file) is not True:
        raise Exception("The provided path is not a file: '{}'".format(input_file))

    if os.access(input_file, os.R_OK) is not True:
        raise Exception("The provided file is not readable: '{}'".format(input_file))


def _provisioning_generate_read_yaml_file(yaml_configuration_file: str) -> str:
    with open(yaml_configuration_file, "r") as fd:
        yaml_content = fd.read()
        return yaml_content


def _zip_resources(resources_path: str, temp_dir: str) -> str:
    """Private function to zip resources path content"""
    zip_file_name = os.path.join(temp_dir, "resources")

    shutil.make_archive(zip_file_name, "zip", resources_path)

    return "{}.zip".format(zip_file_name)


def provisioning_execute(
    id_simulation: int, provisioning_configuration_file: str, debug: bool = False
) -> None:
    """Process YAML configuration file and generate a new provisioning
    chronology.

    """

    print(f"[+] Starting provisioning of simulation ID {id_simulation}")

    # Check simulation is running
    simulation_dict = core_api_client.fetch_simulation(id_simulation)
    simulation_status = simulation_dict["status"]
    if simulation_status != "RUNNING":
        raise Exception(
            "The simulation {id_simulation} should have is status RUNNING "
            "(current status is {current_status}) in order to generate provisioning "
            "chronology. Try the command 'cyber_range simu_run {id_simulation}' "
            "to start the simulation.".format(
                id_simulation=id_simulation, current_status=simulation_status
            )
        )

    # Validate input file
    _provisioning_generate_validate_input_file(provisioning_configuration_file)

    # Open and read YAML input files
    yaml_provisioning_config = _provisioning_generate_read_yaml_file(
        provisioning_configuration_file
    )

    data = json.dumps(
        {
            "idSimulation": id_simulation,
            "provisioningYAML": yaml_provisioning_config,
            "debug": debug,
        }
    )

    result = __post(
        "/provisioning/start_provisioning",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        if result.headers.get("content-type") == "application/json":
            error_msg = result.json()["message"]
        else:
            error_msg = result.text

        raise Exception(
            "Cannot apply provisioning. "
            "Status code: '{}'. Error message: '{}'".format(
                result.status_code, error_msg
            )
        )

    # Wait for the operation to be completed in backend
    current_status = ""
    while True:
        # Sleep before next iteration
        time.sleep(2)

        print(f"    [+] Currently provisioning simulation ID '{id_simulation}'...")

        result = __get("/provisioning/status_provisioning")

        result.raise_for_status()

        result = result.json()

        if "status" in result:
            current_status = result["status"]

            if current_status == "ERROR":
                error_message = result["error_msg"]
                raise Exception(
                    "Error durring provisioning operation: '{}'".format(error_message)
                )
            elif current_status == "FINISHED":
                # Operation has ended
                break

    # Get Provisioning Result
    request = __get("/provisioning/result_provisioning")
    request.raise_for_status()

    result = request.json()

    success = result["success"]

    if success:
        print(
            f"[+] Provisioning was correctly executed on simulation ID '{id_simulation}'"
        )
    else:
        print(
            f"[+] Provisioning was executed with errors on simulation ID '{id_simulation}'"
        )

    if not success:
        error_msg = "No error message returned"
        if "error_msg" in result:
            error_msg = result["error_msg"]
        raise Exception(error_msg)


def provisioning_ansible(
    id_simulation: int,
    playbook_path: str,
    target_role: str = None,
    target_system_type: str = None,
    target_operating_system: str = None,
    target_name: str = None,
    debug: bool = False,
) -> None:
    """Apply ansible playbook(s)s on targets."""

    print(
        f"[+] Starting provisioning ansible playbook(s) on simulation ID {id_simulation}"
    )

    # Check simulation is running
    simulation_dict = core_api_client.fetch_simulation(id_simulation)
    simulation_status = simulation_dict["status"]
    if simulation_status != "RUNNING":
        raise Exception(
            "The simulation {id_simulation} should have is status RUNNING "
            "(current status is {current_status}) in order to generate provisioning "
            "chronology. Try the command 'cyber_range simu_run {id_simulation}' "
            "to start the simulation.".format(
                id_simulation=id_simulation, current_status=simulation_status
            )
        )

    data = {
        "idSimulation": id_simulation,
        "target_role": target_role,
        "target_system_type": target_system_type,
        "target_operating_system": target_operating_system,
        "target_name": target_name,
        "debug": debug,
    }

    with TemporaryDirectory() as temp_dir:
        # Zipping resource files
        zip_file_name = _zip_resources(playbook_path, temp_dir)
        resources_file = open(zip_file_name, "rb")
        files = {"resources_file": resources_file}
        try:
            result = __post(
                "/provisioning/start_ansible",
                data=data,
                files=files,
            )
        finally:
            resources_file.close()

    if result.status_code != 200:

        if result.headers.get("content-type") == "application/json":
            error_msg = result.json()["message"]
        else:
            error_msg = result.text

        raise Exception(
            "Cannot apply provisioning. "
            "Status code: '{}'. Error message: '{}'".format(
                result.status_code, error_msg
            )
        )

    # Wait for the operation to be completed in backend
    current_status = ""
    while True:
        # Sleep before next iteration
        time.sleep(2)

        print(
            f"    [+] Currently provisioning ansible playbook(s) on simulation ID '{id_simulation}'..."
        )

        result = __get("/provisioning/status_provisioning")

        result.raise_for_status()

        result = result.json()

        if "status" in result:
            current_status = result["status"]

            if current_status == "ERROR":
                error_message = result["error_msg"]
                raise Exception(
                    "Error durring provisioning operation: '{}'".format(error_message)
                )
            elif current_status == "FINISHED":
                # Operation has ended
                break

    # Get Provisioning Result
    request = __get("/provisioning/result_provisioning")
    request.raise_for_status()

    result = request.json()

    success = result["success"]

    if success:
        print(
            f"[+] Provisioning was correctly executed on simulation ID '{id_simulation}'"
        )
    else:
        print(
            f"[+] Provisioning was executed with errors on simulation ID '{id_simulation}'"
        )

    if not success:
        error_msg = "No error message returned"
        if "error_msg" in result:
            error_msg = result["error_msg"]
        raise Exception(error_msg)


def provisioning_status(id_simulation: int) -> None:
    """Get provisioning status on targeted simulation."""

    try:
        result = __get(
            "/provisioning/status_provisioning",
            headers={"Content-Type": "application/json"},
        )

        if result.status_code != 200:
            if result.headers.get("content-type") == "application/json":
                error_msg = result.json()["message"]
            else:
                error_msg = result.text

            raise Exception(
                "Cannot get provisioning status. "
                "Status code: '{}'. Error message: '{}'".format(
                    result.status_code, error_msg
                )
            )

        return result.json()

    except Exception as e:
        raise Exception("Issue when getting provisioning status: '{}'".format(e))


def provisioning_result(id_simulation: int) -> str:
    """Get provisioning result on targeted simulation."""

    try:
        result = __get(
            "/provisioning/result_provisioning",
            headers={"Content-Type": "application/json"},
            verify=CA_CERT_PATH,
            cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        )

        if result.status_code != 200:
            if result.headers.get("content-type") == "application/json":
                error_msg = result.json()["message"]
            else:
                error_msg = result.text

            raise Exception(
                "Cannot get provisioning result. "
                "Status code: '{}'. Error message: '{}'".format(
                    result.status_code, error_msg
                )
            )

        return result.json()

    except Exception as e:
        raise Exception("Issue when getting provisioning result: '{}'".format(e))
