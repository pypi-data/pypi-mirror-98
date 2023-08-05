#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import requests


# Configuration access to Cyber Range endpoint
CORE_API_URL = "http://127.0.0.1:5000"
# Expect a path to CA certs (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CA_CERT_PATH = None
# Expect a path to client cert (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None
# Expect a path to client private key (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None


# Simulation status mapping
map_status = {
    "CREATED": 1,
    "PREPARING": 2,
    "READY": 3,
    "STARTING": 4,
    "PROVISIONING": 5,
    "RUNNING": 6,
    "SCENARIO_PLAYING": 7,
    "STOPPING": 8,
    "DESTROYED": 9,
    "CLONING": 10,
    "PAUSING": 11,
    "UNPAUSING": 12,
    "PAUSED": 13,
    "ERROR": 14,
}


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def __get(route: str, **kwargs: Any) -> requests.Response:
    return requests.get(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __post(route: str, **kwargs: Any) -> requests.Response:
    return requests.post(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __put(route: str, **kwargs: Any) -> requests.Response:
    return requests.put(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __delete(route: str, **kwargs: Any) -> requests.Response:
    return requests.delete(
        f"{CORE_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


# -------------------------------------------------------------------------- #


def reset_database() -> Any:
    """Reset the database (clean tables) and
    re-populate it with static info (baseboxes, roles...)
    """
    result = __delete("/database/")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation info from core API. "
            f"Status code: '{result.status_code}'"
        )

    return result.json()


def create_simulation(simulation_dict: dict) -> int:
    """Create simulation and return a simulation ID."""

    # hack (turns the python object representation of the network topology
    # into raw bytes)
    simulation_dict["network"] = pickle.dumps(simulation_dict["network"]).hex()
    data = json.dumps(simulation_dict)

    result = __post(
        "/simulation/",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:

        if result.headers.get("content-type") == "application/json":
            error_msg = result.json()["message"]
        else:
            error_msg = result.text

        raise Exception(
            f"Cannot post simulation information to core API. "
            f"Status code: '{result.status_code}'. "
            f"Error message: '{error_msg}'"
        )

    id_simulation = result.json()["id"]
    return id_simulation


def get_simulation_status(id_simulation: int) -> str:
    """Return only the status of the simulation"""
    result = __get(f"/simulation/{id_simulation}/status")
    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation info from core API. "
            f"Status code '{result.status_code}'"
        )
    return result.json()


def fetch_simulation(id_simulation: int) -> dict:
    """Return a simulation dict given a simulation id."""
    result = __get(f"/simulation/{id_simulation}")

    if result.status_code != 200:
        if result.headers.get("content-type") == "application/json":
            error_msg = result.json()["message"]
        else:
            error_msg = result.text

        raise Exception(
            f"Cannot retrieve simulation info from core API. "
            f"Status code: '{result.status_code}'. "
            f"Error message: '{error_msg}'"
        )

    simulation_dict = result.json()

    # hack (turns the raw bytes representation of the network topology
    # into a real python object)
    b = bytes.fromhex(simulation_dict["network"])
    simulation_dict["network"] = pickle.loads(b)
    return simulation_dict


def fetch_simulations() -> List[Any]:
    """Return all simulations."""
    result = __get("/simulation/")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation info from core API. "
            f"Status code: '{result.status_code}'"
        )

    simulation_list = result.json()
    return simulation_list


def execute_operation_simulation(
    id_simulation: int, operation: str, optional_param: Optional[str] = None
) -> int:
    """Execute operation on targeted simulation."""

    uri = f"/simulation/{id_simulation}/{operation}"

    # Handle optional URI parameter
    if optional_param is not None:
        uri = f"{uri}/{str(optional_param)}"

    # Request URI
    result = __get(uri)

    if result.status_code != 200:
        error_message = result.json()
        raise Exception(
            f"Cannot execute operation '{operation}' "
            f"on simulation '{id_simulation}'. "
            f"Status code: '{result.status_code}' - '{error_message}'"
        )

    # Handle cloning case where a new id_simulation is returned
    if operation == "clone":
        id_simulation = result.json()["id"]

    return id_simulation


def delete_simulation(id_simulation: int) -> Any:
    """Delete a simulation from database."""

    # Delete simulation machines
    delete_machines(id_simulation)

    # Delete simulation
    result = __delete(f"/simulation/{id_simulation}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot delete simulation from core API. "
            f"Status code: '{result.status_code}'"
        )

    return result.json()


def update_simulation(id_simulation: int, simulation_dict: dict) -> Any:
    """Update simulation information information given a simulation id
    and a dict containing simulation info.
    """
    data = json.dumps(simulation_dict)
    result = __put(
        f"/simulation/{id_simulation}",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        raise Exception(
            f"Cannot update simulation information"
            f"with core API. Status code: '{result.status_code}'"
        )

    return result.json()


def fetch_simulation_architecture(id_simulation: int) -> Any:
    """Return the architecture of a simulation."""
    result = __get(f"/simulation/{id_simulation}/architecture")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation architecture info "
            f"from core API. Status code: '{result.status_code}'"
        )

    return result.json()


def fetch_assets(simulation_id: int) -> Any:
    """Return the list of the assets
    of a given simulation. It corresponds to
    the list of the nodes with some additional
    information.
    """
    result = __get(f"/simulation/{simulation_id}/assets")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve assets from core API. "
            f"Status code: '{result.status_code}' ({result.json()})"
        )

    return result.json()


def fetch_machine(machine_id: int) -> List[Any]:
    """Return a machine given its id"""
    result = __get(f"/machine/{machine_id}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve machine from core API. "
            f"Status code: '{result.status_code}' ({result.json()})"
        )

    return result.json()


def delete_machine(id_machine: int) -> Any:
    """Delete simulation machine given a virtual machine id."""
    # Fetch virtual machine network interfaces
    network_interfaces = fetch_network_interfaces(id_machine)

    # Delete each network interfaces
    for network_interface in network_interfaces:
        delete_network_interface(network_interface["id"])

    # Delete virtual machine
    result = __delete(f"/machine/{id_machine}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot delete virtual machine "
            f"from core API. Status code: '{result.status_code}'"
        )

    return result.json()


def fetch_machines(id_simulation: int) -> Any:
    """Return simulation virtual machines dict given
    a simulation id, where keys are virtual machine names.
    """
    result = __get(f"/simulation/{id_simulation}/machine")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation virtual machines from core API. "
            f"Status code: '{result.status_code}'"
        )

    return result.json()


def fetch_virtual_machines(id_simulation: int) -> List[dict]:
    """Return simulation virtual machines dict given a simulation id,
    where keys are virtual machine names.
    """
    results = fetch_machines(id_simulation)

    vm_only = filter(lambda m: m["type"] == "virtual_machine", results)
    return list(vm_only)


def fetch_machine_from_name(id_simulation: int, machine_name: str) -> dict:
    """Return simulation machines dict given
    a simulation id, and the name of a machine
    """
    result = __get(f"/simulation/{id_simulation}/machine/{machine_name}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation virtual machines from core API. "
            f"Status code: '{result.status_code}'"
        )

    return result.json()


def delete_machines(id_simulation: int) -> str:
    """Delete simulation machines given a simulation id."""

    # Fetch simulation machines
    result = __get(f"/simulation/{id_simulation}/machine")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve simulation virtual machines "
            f"from core API. Status code: '{result.status_code}'"
        )
    machines_list = result.json()

    # Delete each virtual machine
    for machine in machines_list:
        delete_machine(machine["id"])

    result_json = "{}"
    return result_json


def update_machine(machine_id: int, machine_dict: dict) -> Any:
    """Update  machine information given a  machine id and a dict containing
    machine data.
    """
    data = json.dumps(machine_dict)
    result = __put(
        f"/machine/{machine_id}",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        raise Exception(
            f"Cannot update machine information with core API. "
            f"Status code: '{result.status_code}', ({result.json()})"
        )
    return result.json()


def fetch_network_interfaces(id_virtual_machine: int) -> Any:
    """Return network interfaces list given a virtual machine id."""
    result = __get(f"/machine/{id_virtual_machine}/network_interface")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve virtual machine network "
            f"interfaces from core API. "
            f"Status code: '{result.status_code}'"
        )

    return result.json()


def delete_network_interface(id_network_interface: int) -> Any:
    """Delete network interface given an id."""
    result = __delete(f"/network_interface/{id_network_interface}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve machine network interfaces from core API. "
            f"Status code: '{result.status_code}'"
        )

    return result.json()


def fetch_baseboxes() -> Any:
    """Return baseboxes list."""
    result = __get("/basebox")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve baseboxes list from core API. "
            f"Status code: '{result.status_code}'"
        )

    baseboxes = result.json()
    return baseboxes


def fetch_basebox(id_basebox: int) -> Any:
    """Return basebox given a basebox id."""
    result = __get(f"/basebox/{id_basebox}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve basebox info from core API. "
            f"Status code: '{result.status_code}'"
        )

    basebox = result.json()
    return basebox


def fetch_user_actions() -> Any:
    """Return user actions list."""
    result = __get("/user_action")

    if result.status_code != 200:
        raise Exception(
            f"Cannot retrieve user actions list from core API. "
            f"Status code: '{result.status_code}'"
        )

    user_actions = result.json()
    return user_actions


def virtclient_status() -> Any:
    """Get virtclient service status."""
    result = __get("/simulation/virtclient_status")

    if result.status_code != 200:
        raise Exception(
            f"Cannot get virtclient service status. "
            f"Status code: '{result.status_code}'"
        )

    simulation_dict = result.json()
    return simulation_dict


def virtclient_reset() -> Any:
    """Ask to stop virtclient VMs."""
    result = __get("/simulation/virtclient_reset")

    if result.status_code != 200:
        raise Exception(f"Cannot reset virtclient. Status code: '{result.status_code}'")

    simulation_dict = result.json()
    return simulation_dict


def tap_simulation(id_simulation: int, iface: str) -> None:
    """Redirect network traffic to the tap interface."""
    result = __get(f"/simulation/{id_simulation}/tap/{iface}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot activate network traffic redirection from core API. "
            f"Status code: '{result.status_code}'"
        )


def untap_simulation(id_simulation: int, iface: str) -> None:
    """Stop redirection of network traffic to the tap interface."""
    result = __get(f"/simulation/{id_simulation}/untap/{iface}")

    if result.status_code != 200:
        raise Exception(
            f"Cannot stop network traffic redirection from core API. "
            f"Status code: '{result.status_code}'"
        )


def fetch_domains() -> Dict[str, str]:
    """Returns the mapping domain->IP"""
    result = __get("/network_interface/domains")

    if result.status_code != 200:
        raise Exception(
            f"Error while fetching domains. " f"Result: '{result.status_code}'"
        )

    return result.json()


def snapshot_simulation(simulation_id: int) -> Any:
    """Create a snapshot of a simulation
    All the files will be stored to
    /cyber-range-catalog/simulations/<hash campaign>/<timestamp>/

    Parameters
    ----------
    simulation_id: int
        Simulation to snapshot
    """
    # this API call returns the path where the
    # architecture file will be stored
    result = __post(f"/simulation/{simulation_id}/snapshot")
    if result.status_code != 200:
        print(result.content.decode())
        raise Exception(
            f"Error while creating snapshot. " f"Result: '{result.status_code}'"
        )

    return result.json()
