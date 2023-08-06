from certora_cli.certoraUtils import safe_create_dir  # type: ignore
from certora_cli.certoraUtils import Mode
import argparse
import json
from datetime import datetime
import re
from copy import deepcopy

"""
This file is responsible for reading and writing configuration files.
"""


def current_conf_to_file(parsed_options: argparse.Namespace) -> None:
    """
    Saves current command line options to a configuration file
    @param parsed_options: command line options after argparse parsing
    """
    json_rep = deepcopy(parsed_options.__dict__)

    """
    We are not saving options if they were not provided (and have a simple default that cannot change between runs).
    Why?
    1. The .conf file is shorter
    2. The .conf file is much easier to read, easy to find relevant arguments when debugging
    3. Reading the .conf file is quicker
    4. Parsing the .conf file is simpler, as we can ignore the null case
    """
    keys_to_delete = ['mode']  # Unnecessary at this point - we were in CONFIG mode
    for (option, value) in json_rep.items():
        if value is None or value is False:
            keys_to_delete.append(option)
    for key in keys_to_delete:
        del json_rep[key]

    safe_create_dir(".last_confs", debug=parsed_options.debug)
    out_file_name = f".last_confs/last_conf_{datetime.now().strftime('%d_%m_%Y__%H_%M_%S')}.conf"
    # debug_print(f"Saving config file to {out_file_name}")
    with open(out_file_name, 'w+') as out_file:
        json.dump(json_rep, out_file, indent=4, sort_keys=True)


# features: read from conf. write last to last_conf and to conf_date..
def read_from_conf(args: argparse.Namespace) -> None:
    """
    Reads data from conf file and adds it to the args namespace, if it is undefined.
    Note: a command line definition trumps the definition in the file.
    If in the .conf file solc is 4.25 and in the command line --solc solc6.10 was given, sol6.10 will be used
    @param args: A namespace containing options from the command line, if any
    """
    assert args.mode == Mode.CONF, "read_from_conf() should only be invoked in CONF mode"

    conf_file_name = args.files[0]
    assert re.search(r'\.conf$', conf_file_name), "file must be of type .conf"

    with open(conf_file_name, "r") as conf_file:
        configuration = json.load(conf_file)

    for option in configuration:
        if hasattr(args, option):
            val = getattr(args, option)
            if val is None or val is False:
                setattr(args, option, configuration[option])

    assert 'files' in configuration, "configuration file corrupted: key 'files' must exist at configuration"
    args.files = configuration['files']  # Override the current .conf file
