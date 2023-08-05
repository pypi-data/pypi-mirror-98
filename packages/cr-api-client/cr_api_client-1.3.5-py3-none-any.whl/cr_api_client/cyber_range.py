#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import configparser
import sys
import time
from typing import Any

import requests

import cr_api_client.core_api_client as core_api_client
import cr_api_client.core_helper as core_helper
import cr_api_client.provisioning_helper as provisioning_helper
import cr_api_client.redteam_helper as redteam_helper
import cr_api_client.scenario_helper as scenario_helper


#
# 'status' related functions
#
def status_handler(args: Any) -> None:
    """Get platform status."""

    print("[+] Platform status")

    # Testing Core API
    print("  [+] Core API")
    print("    [+] address: {}".format(core_api_client.CORE_API_URL))
    try:
        core_api_client.fetch_simulations()
    except requests.exceptions.ConnectionError:
        print("    [+] status: not running !")
        return
    else:
        print("    [+] status: OK")

    # Testing Virtclient API
    print("  [+] Virtclient API")
    try:
        status = core_api_client.virtclient_status()
    except Exception:
        print("    [+] status: not running !")
    else:
        print("    [+] status: OK")
        print("    [+] available slots: {}".format(status["nb_slots"]))

    # # Testing frontend
    # print("  [+] Frontend")
    # print(
    #     "    [+] Address: {}:{}".format(
    #         cyber_range_conf.frontend["listen_host"],
    #         cyber_range_conf.frontend["listen_port"],
    #     )
    # )
    # try:
    #     result = requests.get(
    #         "http://{}:{}".format(
    #             cyber_range_conf.frontend["listen_host"],
    #             cyber_range_conf.frontend["listen_port"],
    #         )
    #     )
    #     if result.status_code != 200:
    #         raise Exception("Error detected in frontend response")
    # except requests.exceptions.ConnectionError:
    #     print("    [+] Status: not running !")
    # except Exception:
    #     print("    [+] Status: not working properly !")
    #     return
    # else:
    #     print("    [+] Status: OK")


#
# 'init' related functions
#
def init_handler(args: Any) -> None:
    """Process initialization of mysql db and snapshots path."""

    print(
        "[+] Reset virtclient (stop VMs, stop Docker containers, delete snaphots, ...)"
    )
    core_api_client.virtclient_reset()

    print("[+] Initialize database")
    core_api_client.reset_database()


#
# 'basebox_list' related functions
#
def basebox_list_handler(args: Any) -> None:
    """List available baseboxes, for use in simulations."""
    print("[+] List of available baseboxes")
    baseboxes = core_api_client.fetch_baseboxes()

    for basebox in baseboxes:

        # Check if basebox is in local catalog
        if basebox["available"]:
            local_basebox = "yes: {}".format(basebox["path"])
        else:
            local_basebox = "no"

        print(
            "  [+] {}: {} (role: {}, {}, {}) - available? {}".format(
                basebox["id"],
                basebox["description"],
                basebox["role"],
                basebox["language"],
                basebox["operating_system"],
                local_basebox,
            )
        )


#
# 'simu_create' simulation related functions
#
def simu_create_handler(args: Any) -> None:
    """Process YAML configuration file and request core API to create a
    new simulation.

    """

    # Parameters
    architecture_file = args.architecture_file

    # Compute elpased time
    t1 = time.time()

    try:
        id_simulation = core_helper.simu_create(architecture_file)
        print("Created simulation ID: '{}'".format(id_simulation))
    except Exception as e:
        print(f"Error when creating new simulation: '{e}'")
        sys.exit(1)
    finally:
        t2 = time.time()
        time_elapsed = t2 - t1
        print("[+] Time elapsed: {0:.2f} seconds".format(time_elapsed))


#
# 'provisioning_execute' related functions
#
def provisioning_execute_handler(args: Any) -> None:
    """Process YAML configuration file and execute a new provisioning
    chronology (generate + play)).

    """

    # Parameters
    id_simulation = args.id_simulation
    provisioning_configuration_file = args.provisioning_configuration_file
    debug = args.debug_mode

    try:
        provisioning_helper.provisioning_execute(
            id_simulation, provisioning_configuration_file, debug=debug
        )
    except Exception as e:
        print(f"Error during provisioning: '{e}'")
        sys.exit(1)


#
# 'provisioning_ansible' related functions
#
def provisioning_ansible_handler(args: Any) -> None:
    """Apply ansible playbook on targets."""

    # Parameters
    id_simulation = args.id_simulation
    provisioning_playbook_path = args.provisioning_playbook_path
    provisioning_target_role = args.provisioning_target_role
    provisioning_target_system_type = args.provisioning_target_system_type
    provisioning_target_operating_system = args.provisioning_target_operating_system
    provisioning_target_name = args.provisioning_target_name
    debug = args.debug_mode

    # TODO: check that only one target type is defined

    # TODO: support other target types
    if provisioning_target_operating_system is not None:
        raise NotImplementedError("target_operating_system not yet supported")
    if provisioning_target_system_type is not None:
        raise NotImplementedError("target_system_type not yet supported")
    if provisioning_target_role is not None:
        raise NotImplementedError("target_role not yet supported")

    if provisioning_target_name is None:
        raise NotImplementedError("target_name (-n option) should be defined")

    try:
        provisioning_helper.provisioning_ansible(
            id_simulation,
            provisioning_playbook_path,
            target_role=provisioning_target_role,
            target_system_type=provisioning_target_system_type,
            target_operating_system=provisioning_target_operating_system,
            target_name=provisioning_target_name,
            debug=debug,
        )
    except Exception as e:
        print(f"Error during provisioning: '{e}'")
        sys.exit(1)


#
# 'scenario_play' simulation
#
def scenario_play_handler(args: Any) -> None:
    """Play scenario on targeted simulation."""
    # Parameters
    id_simulation = args.id_simulation
    scenario_path = args.scenario_path
    file_results = args.scenario_file_results
    debug_mode = args.scenario_debug_mode
    speed = args.scenario_speed

    print(
        "[+] Playing scenario '{}' on simulation id '{}'".format(
            scenario_path, id_simulation
        )
    )

    try:
        scenario_helper.scenario_play(
            id_simulation, scenario_path, debug_mode, speed, file_results
        )
    except Exception as e:
        print(f"Error when playing scenario: '{e}'")
        sys.exit(1)


#
# 'scenario_status' simulation
#
def scenario_status_handler(args: Any) -> None:
    """Get scenario status on targeted simulation."""
    # Parameters
    id_simulation = args.id_simulation

    print("[+] Get scenario status on simulation id '{}'".format(id_simulation))
    status = scenario_helper.scenario_status(id_simulation)
    print("  [+] Current status: {}".format(status["status"]))


#
# 'simu_run' simulation
#
def simu_run_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation
    use_install_time = args.use_install_time

    # Compute elpased time
    t1 = time.time()

    try:
        core_helper.simu_run(id_simulation, use_install_time)
    except Exception as e:
        print(f"Error when starting simulation: '{e}'")
        sys.exit(1)
    else:
        print("[+] Simulation is running...")
    finally:
        t2 = time.time()
        time_elapsed = t2 - t1
        print("[+] Time elapsed: {0:.2f} seconds".format(time_elapsed))


#
# 'simu_status' of simulation
#
def simu_status_handler(args: Any) -> None:
    # Parameters
    requested_simulation_id = args.id_simulation

    simulations = core_api_client.fetch_simulations()

    for simulation in simulations:
        if (
            requested_simulation_id is None
            or requested_simulation_id == simulation["id"]
        ):
            id_simulation = simulation["id"]

            print("[+] simulation id {}:".format(id_simulation))
            print("  [+] name: {}".format(simulation["name"]))
            print("  [+] status: {}".format(simulation["status"]))

            # Fetch associated machines
            machines = core_api_client.fetch_machines(id_simulation)

            print("  [+] machines:")
            for machine in machines:
                print("    [+] name: {} ({})".format(machine["name"], machine["type"]))
                print("      [+] status: {}".format(machine["status"]))
                print(
                    "      [+] machine stats: {} Mo, {} core(s)".format(
                        machine["memory_size"],
                        machine["nb_proc"],
                    )
                )

                if machine["type"] == "virtual_machine":
                    print(
                        "      [+] basebox: {}".format(
                            machine["basebox_id"],
                        )
                    )
                    print(
                        "      [+] current basebox path: {}".format(
                            machine["hard_drive"]
                        )
                    )
                    print("      [+] uuid: {}".format(machine["system_uid"]))
                    print("      [+] VNC port: {}".format(machine["vnc_port"]))
                    if machine["username"] is not None:
                        print(
                            "      [+] user account: {}:{}".format(
                                machine["username"], machine["password"]
                            )
                        )
                    else:
                        print("      [+] user account: None")
                    if machine["admin_username"] is not None:
                        print(
                            "      [+] admin account: {}:{}".format(
                                machine["admin_username"], machine["admin_password"]
                            )
                        )
                    else:
                        print("      [+] admin account: None")
                elif machine["type"] == "docker":
                    print(
                        "      [+] docker image: {}".format(
                            machine["base_image"],
                        )
                    )


#
# 'simu_pause' simulation
#
def simu_pause_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation

    try:
        core_helper.simu_pause(id_simulation)
    except Exception as e:
        print(f"Error when pausing simulation: '{e}'")
        sys.exit(1)
    else:
        print("Simulation paused")


#
# 'simu_unpause' simulation
#
def simu_unpause_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation

    try:
        core_helper.simu_unpause(id_simulation)
    except Exception as e:
        print(f"Error when unpausing simulation: '{e}'")
        sys.exit(1)
    else:
        print("Simulation unpaused")


#
# 'simu_halt' simulation
#
def simu_halt_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation

    try:
        core_helper.simu_halt(id_simulation)
    except Exception as e:
        print(f"Error when halting simulation: '{e}'")
        sys.exit(1)
    else:
        print("Simulation halted")


#
# 'simu_destroy' simulation
#
def simu_destroy_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation

    try:
        core_helper.simu_destroy(id_simulation)
    except Exception as e:
        print(f"Error when destroying simulation: '{e}'")
        sys.exit(1)
    else:
        print("Simulation destroyed")


#
# 'simu_clone' simulation
#
def simu_clone_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation

    try:
        id_new_simulation = core_helper.simu_clone(id_simulation)
    except Exception as e:
        print(f"Error when cloning simulation: '{e}'")
        sys.exit(1)
    else:
        print("Simulation cloned")
        print("Created simulation ID: '{}'".format(id_new_simulation))


#
# 'simu_tap' simulation
#
def simu_tap_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation
    iface = args.iface

    try:
        core_helper.simu_tap(id_simulation, iface)
    except Exception as e:
        print(f"Error when setting tap on simulation: '{e}'")
        sys.exit(1)
    else:
        print("Redirect network traffic to the tap interface")


#
# 'simu_untap' simulation
#
def simu_untap_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation
    iface = args.iface

    try:
        core_helper.simu_untap(id_simulation, iface)
    except Exception as e:
        print(f"Error when unsetting tap on simulation: '{e}'")
        sys.exit(1)
    else:
        print("Stop redirection of network traffic to the tap interface")


#
# 'simu_delete' simulation
#
def simu_delete_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation

    try:
        core_helper.simu_delete(id_simulation)
    except Exception as e:
        print(f"Error when deleting simulation: '{e}'")
        sys.exit(1)
    else:
        print("[+] VMs destroyed")
        print("[+] VMs snapshots deleted")
        print("[+] Simulation deleted from database")


#
# 'simu_snap' simulation
#
def simu_snap_handler(args: Any) -> None:
    # Parameters
    id_simulation = args.id_simulation
    # core generates an architecture file (yaml)
    # that will be located to /cyber_range_stuff...
    # This outfile is merely a copy of the generated
    # file
    output_file = args.output

    try:
        yaml = core_helper.simu_snap(id_simulation)
        with open(output_file, "w") as w:
            w.write(yaml)
        print(f"[+] Snapshot done. Architecture file stored at {output_file}")
    except Exception as e:
        print(f"Error when creating snapshot for simulation: '{e}'")
        sys.exit(1)


def set_core_api_url(core_api_url: str) -> str:
    print("  [+] Using core API URL: {}".format(core_api_url))
    core_api_client.CORE_API_URL = core_api_url
    return core_api_url


def set_scenario_api_url(scenario_api_url: str) -> str:
    print("  [+] Using scenario API URL: {}".format(scenario_api_url))
    scenario_helper.SCENARIO_API_URL = scenario_api_url
    return scenario_api_url


def set_provisioning_api_url(provisioning_api_url: str) -> str:
    print("  [+] Using provisioning API URL: {}".format(provisioning_api_url))
    provisioning_helper.PROVISIONING_API_URL = provisioning_api_url
    return provisioning_api_url


def set_redteam_api_url(redteam_api_url: str) -> str:
    print("  [+] Using redteam API URL: {}".format(redteam_api_url))
    redteam_helper.REDTEAM_API_URL = redteam_api_url
    return redteam_api_url


def set_cacert(cacert: str) -> str:
    print("  [+] Using CA certs path: {}".format(cacert))
    core_api_client.CA_CERT_PATH = cacert
    scenario_helper.CA_CERT_PATH = cacert
    provisioning_helper.CA_CERT_PATH = cacert
    redteam_helper.CA_CERT_PATH = cacert
    return cacert


def set_cert(cert: str) -> str:
    print("  [+] Using client cert path: {}".format(cert))
    core_api_client.CLIENT_CERT_PATH = cert
    scenario_helper.CLIENT_CERT_PATH = cert
    provisioning_helper.CLIENT_CERT_PATH = cert
    redteam_helper.CLIENT_CERT_PATH = cert
    return cert


def set_key(key: str) -> str:
    print("  [+] Using client key path: {}".format(key))
    core_api_client.CLIENT_KEY_PATH = key
    scenario_helper.CLIENT_KEY_PATH = key
    provisioning_helper.CLIENT_KEY_PATH = key
    redteam_helper.CLIENT_KEY_PATH = key
    return key


def main() -> None:

    print("[+] Config")
    parser = argparse.ArgumentParser()

    # Manage options passed in config file
    parser.add_argument("--config", help="Configuration file")
    args, left_argv = parser.parse_known_args()
    if args.config:
        print(f"  [+] Using config file: {args.config}")
        config = configparser.SafeConfigParser()
        config.read(args.config)

    # Common debug argument
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug_mode",
        help="Activate debug mode (not set by default)",
    )

    # Common options to access remote API
    parser.add_argument(
        "--core-url",
        dest="core_api_url",
        type=set_core_api_url,
        help="Set core API URL (default: '{}')".format(core_api_client.CORE_API_URL),
    )
    parser.add_argument(
        "--scenario-url",
        dest="scenario_api_url",
        type=set_scenario_api_url,
        help="Set scenario API URL (default: '{}')".format(
            scenario_helper.SCENARIO_API_URL
        ),
    )
    parser.add_argument(
        "--provisioning-url",
        dest="provisioning_api_url",
        type=set_provisioning_api_url,
        help="Set provisioning API URL (default: '{}')".format(
            provisioning_helper.PROVISIONING_API_URL
        ),
    )
    parser.add_argument(
        "--redteam-url",
        dest="redteam_api_url",
        type=set_redteam_api_url,
        help="Set redteam API URL (default: '{}')".format(
            redteam_helper.REDTEAM_API_URL
        ),
    )
    parser.add_argument(
        "--cacert", dest="cacert", type=set_cacert, help="Set path to CA certs"
    )
    parser.add_argument(
        "--cert", dest="cert", type=set_cert, help="Set path to client cert"
    )
    parser.add_argument(
        "--key", dest="key", type=set_key, help="Set path to client key"
    )

    subparsers = parser.add_subparsers()

    # 'status' command
    parser_status = subparsers.add_parser("status", help="Get platform status")
    parser_status.set_defaults(func=status_handler)

    # 'init' command
    parser_init = subparsers.add_parser(
        "init",
        help="Initialize database (override previous simulations!)",
    )
    parser_init.set_defaults(func=init_handler)

    # 'basebox_list' command
    parser_bb_list = subparsers.add_parser(
        "basebox_list",
        help="List available baseboxes",
    )
    parser_bb_list.set_defaults(func=basebox_list_handler)

    # -----------------------
    # --- Core/simu options
    # -----------------------

    # 'simu_create' simulation command
    parser_simu_create = subparsers.add_parser(
        "simu_create",
        help="Create a new simulation",
    )
    parser_simu_create.set_defaults(func=simu_create_handler)
    parser_simu_create.add_argument(
        "-a",
        action="store",
        required=True,
        dest="architecture_file",
        help="Input path of simulation architecture",
    )

    # 'simu_run' simulation command
    parser_simu_run = subparsers.add_parser("simu_run", help="Run a simulation")
    parser_simu_run.set_defaults(func=simu_run_handler)
    parser_simu_run.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_run.add_argument(
        "--use_install_time",
        action="store_true",
        dest="use_install_time",
        help="Indicates that VM installation time will be used to set VMs boot time",
    )

    # 'simu_status' simulation command
    parser_simu_status = subparsers.add_parser(
        "simu_status", help="Get status of a simulation or all simulations"
    )
    parser_simu_status.set_defaults(func=simu_status_handler)
    parser_simu_status.add_argument(
        "id_simulation", type=int, nargs="?", help="The simulation id"
    )

    # 'simu_pause' simulation command
    parser_simu_pause = subparsers.add_parser(
        "simu_pause",
        help="Pause a simulation (suspend VMs)",
    )
    parser_simu_pause.set_defaults(func=simu_pause_handler)
    parser_simu_pause.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_unpause' simulation command
    parser_simu_unpause = subparsers.add_parser(
        "simu_unpause",
        help="Unpause a simulation (resume VMs)",
    )
    parser_simu_unpause.set_defaults(func=simu_unpause_handler)
    parser_simu_unpause.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )

    # 'simu_halt' simulation command
    parser_simu_halt = subparsers.add_parser(
        "simu_halt",
        help="Halt a simulation (stop VMs and save VMs state)",
    )
    parser_simu_halt.set_defaults(func=simu_halt_handler)
    parser_simu_halt.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_destroy' simulation command
    parser_simu_destroy = subparsers.add_parser(
        "simu_destroy",
        help="Destroy a simulation (stop VMs and delete VMs state)",
    )
    parser_simu_destroy.set_defaults(func=simu_destroy_handler)
    parser_simu_destroy.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )

    # 'simu_snap' simulation command
    parser_simu_snap = subparsers.add_parser(
        "simu_snap", help="Get status of a simulation or all simulations"
    )
    parser_simu_snap.set_defaults(func=simu_snap_handler)
    parser_simu_snap.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_snap.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        default=None,
        help="Path to the output yaml file",
    )

    # 'simu_clone' simulation command
    parser_simu_clone = subparsers.add_parser("simu_clone", help="Clone a simulation")
    parser_simu_clone.set_defaults(func=simu_clone_handler)
    parser_simu_clone.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_delete' simulation command
    parser_simu_delete = subparsers.add_parser(
        "simu_delete",
        help="Delete a simulation",
    )
    parser_simu_delete.set_defaults(func=simu_delete_handler)
    parser_simu_delete.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_tap' simulation command
    parser_simu_tap = subparsers.add_parser(
        "simu_tap",
        help="Redirect network traffic to the tap interface",
    )
    parser_simu_tap.set_defaults(func=simu_tap_handler)
    parser_simu_tap.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_tap.add_argument("iface", type=str, help="The tap network interface")

    # 'simu_untap' simulation command
    parser_simu_untap = subparsers.add_parser(
        "simu_untap",
        help="Stop redirection of network traffic",
    )
    parser_simu_untap.set_defaults(func=simu_untap_handler)
    parser_simu_untap.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_untap.add_argument("iface", type=str, help="The tap network interface")

    # -----------------------
    # --- Provisioning options
    # -----------------------

    # 'provisioning_execute' command
    parser_provisioning_execute = subparsers.add_parser(
        "provisioning_execute", help="Execute provisioning chronology for a simulation"
    )
    parser_provisioning_execute.set_defaults(func=provisioning_execute_handler)
    parser_provisioning_execute.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )
    parser_provisioning_execute.add_argument(
        "-c",
        action="store",
        required=True,
        dest="provisioning_configuration_file",
        help="Input path of provisioning configuration",
    )

    # 'provisioning_ansible' command
    parser_provisioning_ansible = subparsers.add_parser(
        "provisioning_ansible", help="Apply ansible playbook(s) on targets"
    )
    parser_provisioning_ansible.set_defaults(func=provisioning_ansible_handler)
    parser_provisioning_ansible.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )
    parser_provisioning_ansible.add_argument(
        "-c",
        action="store",
        required=True,
        dest="provisioning_playbook_path",
        help="Input directory containing ansible playbook(s)",
    )
    parser_provisioning_ansible.add_argument(
        "-r",
        action="store",
        dest="provisioning_target_role",
        help="Role used to filter targets ('client', 'activate_directory', 'file_server', 'admin', ...)",
    )
    parser_provisioning_ansible.add_argument(
        "-s",
        action="store",
        dest="provisioning_target_system_type",
        help="System type used to filter targets ('linux', 'windows')",
    )
    parser_provisioning_ansible.add_argument(
        "-o",
        action="store",
        dest="provisioning_target_operating_system",
        help="Operating system used to filter targets ('Windows 7', 'Windows 10', 'Debian', 'Ubuntu', ...)",
    )
    parser_provisioning_ansible.add_argument(
        "-n",
        action="store",
        dest="provisioning_target_name",
        help="Machine name used to filter targets",
    )

    # -----------------------
    # --- Scenario options
    # -----------------------

    # 'scenario_play' command
    parser_scenario_play = subparsers.add_parser(
        "scenario_play", help="Play scenario on a simulation"
    )
    parser_scenario_play.set_defaults(func=scenario_play_handler)
    parser_scenario_play.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )
    parser_scenario_play.add_argument(
        "-i",
        action="store",
        nargs="?",
        required=True,
        dest="scenario_path",
        help="Path of the scenario to play",
    )

    parser_scenario_play.add_argument(
        "-o",
        action="store",
        required=False,
        dest="scenario_file_results",
        help="Absolute name of scenario results (json format)",
    )

    parser_scenario_play.add_argument(
        "-d",
        action="store",
        required=False,
        dest="scenario_debug_mode",
        default="off",
        help="Debug mode ('off', 'on', 'full')",
    )
    parser_scenario_play.add_argument(
        "-t",
        action="store",
        required=False,
        dest="scenario_speed",
        default="normal",
        help="scenario speed ('slow', 'normal', 'fast')",
    )

    # 'scenario_status' command
    parser_scenario_status = subparsers.add_parser(
        "scenario_status", help="Get scenario status on a simulation"
    )
    parser_scenario_status.set_defaults(func=scenario_status_handler)
    parser_scenario_status.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    # Handle parameter written in config file
    if args.config:
        for k, v in config.items("DEFAULT"):
            parser.parse_args([str(k), str(v)], args)

    # Parse remaining args from command line (overriding potential config file
    # parameters)
    args = parser.parse_args(left_argv, args)

    args.func(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
