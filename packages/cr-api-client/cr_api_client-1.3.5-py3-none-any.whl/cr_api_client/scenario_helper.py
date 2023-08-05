#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
from tempfile import TemporaryDirectory
from typing import Any

import requests


# Configuration access to Cyber Range endpoint
SCENARIO_API_URL = "http://127.0.0.1:5002"
CA_CERT_PATH = None  # Expect a path to CA certs (see: https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None  # Expect a path to client cert (see: https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None  # Expect a path to client private key (see: https://requests.readthedocs.io/en/master/user/advanced/)


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def __get(route: str, **kwargs: str) -> Any:
    return requests.get(
        f"{SCENARIO_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __post(route: str, **kwargs: str) -> Any:
    return requests.post(
        f"{SCENARIO_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __put(route: str, **kwargs: str) -> Any:
    return requests.put(
        f"{SCENARIO_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __delete(route: str, **kwargs: str) -> Any:
    return requests.delete(
        f"{SCENARIO_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


# -------------------------------------------------------------------------- #


#
# 'scenario_play' helper
#
def _zip_scenario(scenario_path: str, temp_dir: str) -> str:
    """Private function to zip a scenario_path content"""
    zip_file_name = os.path.join(temp_dir, "scenario")

    shutil.make_archive(zip_file_name, "zip", scenario_path)

    return "{}.zip".format(zip_file_name)


def scenario_play(
    id_simulation: int,
    scenario_path: str,
    debug_mode: str = "off",
    speed: str = "normal",
    scenario_file_results: str = None,
) -> None:
    """Play scenario on targeted simulation."""

    if scenario_path is None:
        scenario_path = "test/scenarios/scenario0.yml"

    python_api = False

    if os.path.isdir(scenario_path):
        # scenarios written with Python syntax
        python_api = True
    else:
        # scenarios written with YAML syntax
        with open(scenario_path, "r") as fd:
            scenario_yaml = fd.read()

    # Play scenario

    scenario_success = False
    scenario_log_filename = None

    try:
        if python_api:
            data = {
                "idSimulation": id_simulation,
                "debug_mode": debug_mode,
                "speed": speed,
            }

            with TemporaryDirectory() as temp_dir:
                # Zipping scenario files
                zip_file_name = _zip_scenario(scenario_path, temp_dir)
                scenario_files = open(zip_file_name, "rb")
                files = {"scenario_files": scenario_files}
                try:
                    result = __post(
                        "/scenario/start_scenario_py", data=data, files=files
                    )
                finally:
                    scenario_files.close()

        else:
            data = json.dumps(
                {"idSimulation": id_simulation, "scenarioYAML": scenario_yaml}
            )

            result = __post(
                "/scenario/start_scenario",
                data=data,
                headers={"Content-Type": "application/json"},
            )

        if result.status_code != 200:
            raise Exception(
                "Cannot start scenario at scenario API. "
                "Status code: '{}'. Error message: '{}'".format(
                    result.status_code, result.json()["message"]
                )
            )

        # Wait for the operation to be completed in backend
        current_status = ""
        while True:
            # Sleep before next iteration
            time.sleep(2)

            print(
                f"    [+] Currently executing scenario for simulation ID '{id_simulation}'..."
            )

            result = __get("/scenario/status_scenario")

            result.raise_for_status()

            result = result.json()

            if "status" in result:
                current_status = result["status"]

                if current_status == "ERROR":
                    error_message = result["error_msg"]
                    raise Exception(
                        "Error during simulation operation: '{}'".format(error_message)
                    )
                elif current_status == "FINISHED":
                    # Operation has ended
                    break

        # Get Scenario Result
        request = __get("/scenario/result_scenario")
        request.raise_for_status()

        result = request.json()

        scenario_results = result["result"][0]
        scenario_success = scenario_results["success"]
        scenario_log_filename = result["result"][1]

        if scenario_success:
            print(
                f"[+] Scenario was correctly executed on simulation ID '{id_simulation}'"
            )
        else:
            print(
                f"[+] Scenario was executed with errors on simulation ID '{id_simulation}'"
            )
            if scenario_file_results is None:
                print(
                    "[+] In order to know about errors, replay the scenario using the '-o <output_json_filename>' option"
                )

        if scenario_file_results is not None:
            # create file for json results
            try:
                with open(scenario_file_results, "w") as fd:
                    json.dump(scenario_results, fd, indent=4)

                print(
                    f"[+] Scenario results are available here: {scenario_file_results}"
                )

            except Exception as e:
                print(f"[+] Error while writing scenario results: {e}")

        if not scenario_success:
            raise Exception(
                "Some action could not be played. See scenario result for more information."
            )

    except Exception as e:
        raise Exception("Issue when starting scenario execution: '{}'".format(e))

    return (scenario_success, scenario_log_filename)


def scenario_status(id_simulation: int) -> None:
    """Get scenario status on targeted simulation."""

    try:
        result = __get(
            "/scenario/status_scenario", headers={"Content-Type": "application/json"}
        )

        if result.status_code != 200:
            raise Exception(
                "Cannot get scenario status from scenario API. "
                "Status code: '{}'. Error message: '{}'".format(
                    result.status_code, result.json()["message"]
                )
            )

        return result.json()

    except Exception as e:
        raise Exception("Issue when getting scenario status: '{}'".format(e))


def scenario_result(id_simulation: int) -> str:
    """Get scenario result on targeted simulation."""

    try:
        result = __get(
            "/scenario/result_scenario",
            headers={"Content-Type": "application/json"},
            verify=CA_CERT_PATH,
            cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        )

        if result.status_code != 200:
            raise Exception(
                "Cannot get scenario result from scenario API. "
                "Status code: '{}'. Error message: '{}'".format(
                    result.status_code, result.json()["message"]
                )
            )

        return result.json()

    except Exception as e:
        raise Exception("Issue when getting scenario result: '{}'".format(e))
