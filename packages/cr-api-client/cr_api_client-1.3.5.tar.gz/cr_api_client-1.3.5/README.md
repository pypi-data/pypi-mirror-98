# AMOSSYS Cyber Range client API

## Installation

Note: it is recommanded to install the package in a virtualenv in order to avoid conflicts with version dependencies of other packages.

```sh
python3 setup.py install
```

## Configuration

Access to the Cyber Range is possible with either of the following configuration methods.

### Configuration through configuration file (CLI only)

It is possible to configure access to the Cyber Range through a configuration file, specified with the `--config` command line parameter:

```sh
$ cyber_range --help
(...)
--config CONFIG       Configuration file
(...)
```

Configuration file content should be of the form `--key = value` (without quotes in values), as in the following exemple:

```
[DEFAULT]
--core-url = https://[CORE-URL-API]
--scenario-url = https://[SCENARIO-URL-API]
--provisioning-url = https://[PROVISIONING-URL-API]
--redteam-url = https://[REDTEAM-URL-API]
--cacert = <PATH TO CA CERT>
--cert = <PATH TO CLIENT CERT>
--key = <PATH TO CLIENT PRIVATE KEY>
```

### Configuration through command line arguments (CLI only)

It is possible to configure access to the Cyber Range through command line arguments. See `cyber_range --help` command line output for available parameters:

```sh
$ cyber_range --help
(...)
  --core-url CORE_API_URL
                        Set core API URL (default: 'http://127.0.0.1:5000')
  --scenario-url SCENARIO_API_URL
                        Set scenario API URL (default: 'http://127.0.0.1:5002')
  --provisioning-url PROVISIONING_API_URL
                        Set provisioning API URL (default: 'http://127.0.0.1:5003')
  --redteam-url REDTEAM_API_URL
                        Set redteam API URL (default: 'http://127.0.0.1:5004')
  --cacert CACERT       Set path to CA certs
  --cert CERT           Set path to client cert
  --key KEY             Set path to client key
```

### Configuration through programmatic means

It is possible to configure access to the Cyber Range programmatically in Python:

```python
import cr_api_client.core_api_client as core_api_client
import cr_api_client.core_helper as core_helper
import cr_api_client.scenario_helper as scenario_helper
import cr_api_client.provisioning_helper as provisioning_helper
import cr_api_client.redteam_helper as redteam_helper

# Set URL API
core_api_client.CORE_API_URL = "https://[CORE-URL-API]"
scenario_helper.SCENARIO_API_URL = "https://[SCENARIO-URL-API]"
provisioning_helper.PROVISIONING_API_URL = "https://[PROVISIONING-URL-API]"
redteam_helper.REDTEAM_API_URL = "https://[REDTEAM-URL-API]"

# Set server and client certificates for Core API
core_api_client.CA_CERT_PATH = <PATH TO CA CERT>
core_api_client.CLIENT_CERT_PATH = <PATH TO CLIENT CERT>
core_api_client.CLIENT_KEY_PATH = <PATH TO CLIENT PRIVATE KEY>

# Apply same server and client certificates to other API
redteam_helper.CA_CERT_PATH = provisioning_helper.CA_CERT_PATH = scenario_helper.CA_CERT_PATH = core_api_client.CA_CERT_PATH
redteam_helper.CLIENT_CERT_PATH = provisioning_helper.CLIENT_CERT_PATH = scenario_helper.CLIENT_CERT_PATH = core_api_client.CLIENT_CERT_PATH
redteam_helper.CLIENT_KEY_PATH = provisioning_helper.CLIENT_KEY_PATH = scenario_helper.CLIENT_KEY_PATH = core_api_client.CLIENT_KEY_PATH
```

## CLI usage

See `cyber_range --help` command line output for available parameters:

```sh
$ cyber_range --help
(...)
```

## Programmatic usage

### Platform initialization API

Before starting a new simulation, the platform has to be initialized:

```python
core_api_client.virtclient_reset()
core_api_client.reset_database()
redteam_helper.reset_redteam()
```

### Simulation API

```python
core_helper.simu_create(architecture_file: str)  # Process YAML configuration file and request core API to create a new simulation

core_helper.simu_run(id_simulation: int, use_vm_time: bool)  # Start the simulation, with current time (by default) or time where the VM was created (use_vm_time=True)

core_helper.simu_pause(id_simulation: int)  # Pause a simulation (calls libvirt suspend API)

core_helper.simu_unpause(id_simulation: int)  # Pause a simulation (calls libvirt suspend API)

core_helper.simu_halt(id_simulation: int)  # Properly stop a simulation, by sending a shutdown signal to the operating systems

core_helper.simu_destroy(id_simulation: int)  # Stop a simulation through a hard reset

core_helper.simu_clone(id_simulation: int) -> int  # Clone a simulation and create a new simulation, and return the new ID

core_helper.simu_tap(id_simulation: int, iface: str)  # Mirror all network traffic through a local network interface

core_helper.simu_untap(id_simulation: int, iface: str)  # Stop mirroring all network traffic

core_helper.simu_delete(id_simulation: int)  # Delete a simulation in database
```

### Provisioning API

```python
provisioning_helper.provisioning_execute(id_simulation: int, provisioning_configuration_file: str)  # Apply provisioning configuration defined in YAML file on simulation defined in argument ID
```

### Scenario API

```python
scenario_helper.scenario_play(id_simulation: int, scenario_path: str,
                              debug_mode: str = 'off', speed: str = 'normal',
                              scenario_file_results: str = None)
```

This method makes it possible to play  scenario defined in ``scenario path`` on simulation defined in ``id_simulation``.
These parameters are **mandatory**.

The following parameters are optional:

* ``debug_mode``: This parameter has to be used for **debug** only. It corresponds to the level of verbosity of the debug traces generated during the execution of user actions:
  * ``'off'``: no debug traces,
  * ``'on'``:  with debug traces,
  * ``'full'``: with maximum debug traces.

  The default is ``'off'``. Debug traces are generated **on the server side only**.

* ``speed``: This parameter affects the speed of typing keys on the keyboard and the speed of mouse movement:
  * ``'slow'``: slow speed,
  * ``'normal'``:  normal speed,
  * ``'fast'``: fast speed.

  The default is ``'normal'``.

* ``scenario_file_results``: This parameter makes it possible to get the scenario results (of user actions) in a file.
  Results are stored using a json format. The file name should be absolute (``'/tmp/results.json'`` for example).

  Here an example:

  ```json
  {
    "success": true,
    "scenario_results": [
        {
            "name": "scenario.py",
            "success": true,
            "target": {
                "name": "CLIENT1",
                "role": "client",
                "basebox_id": 70,
                "ip_address": "localhost",
                "vnc_port": 5901
            },
            "action_packs": {
                "operating_system": "operating_system/windows7"
            },
            "action_list": [
                {
                    "name": "open_session",
                    "parameters": {
                        "password": "7h7JMc67",
                        "password_error": "false",
                        "login": "John"
                    },
                    "start_time": "2021-03-01 12:39:25.119",
                    "end_time": "2021-03-01 12:39:57.325",
                    "success": true,
                    "implemented": true
                },
                {
                    "name": "close_session",
                    "parameters": {},
                    "start_time": "2021-03-01 12:40:02.330",
                    "end_time": "2021-03-01 12:40:09.303",
                    "success": true,
                    "implemented": true
                }
            ]
        }
    ]
  }
  ```

Here are some examples of calling this method:

```python
scenario_helper.scenario_play(1, './scenarios/my_scenario') # this is the common way

scenario_helper.scenario_play(1, './scenarios/my_scenario', scenario_file_results='/tmp/results.json')

scenario_helper.scenario_play(1, './scenarios/my_scenario', debug_mode='full', speed='fast')
```

### Redteam API

*In progress*
