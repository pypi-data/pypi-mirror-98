#!/usr/bin/env python3


"""
Meraki CLI Command-Line Tool

https://github.com/PackeTsar/meraki-cli

This program is a wrapper around the official Meraki dashboard-api-python
    library available at https://github.com/meraki/dashboard-api-python.

The tool builds its argument parser using the class and method structures
    of the Meraki library by inspecting each method's positional and named
    parameters and turning them into argparse-native arguments. It also uses
    available annotations in the function arguments to further specify CLI
    argument requirements as well as method docstrings for CLI help.

The user's Meraki API key must be provided to the tool one of two ways:
    1. (Recommended) Via an environment variable by storing it like:
        export MERAKI_DASHBOARD_API_KEY=12345abcdef
    2. Passing it as an argument like '-k 12345abcdef'

Debugging can be set to one of 4 levels like "-d", "-dd", etc:
    Level 0: Default. Does not output and logs except warnings or above.
    Level 1: Informational data from CLI program.
    Level 2: Informational data from CLI program and Meraki programs.
    Level 3: Debugging level data from CLI program and Meraki programs.

Data returned from the different library methods will be best-effort formatted
    into a table for easy reading, or will be output as JSON if table
    formatting is not possible. Data may hev to be discarded in the
    table-formatting process. Data can be forced to JSON with the"-j" switch.
    You can also filter and order table columns with the "-c" switch like:
        -c "id,name,subnet"

Items returned in the data can be filtered using instances the "-f" argument.
    Filter statements use the <key>:<regex> format. An example of a filter is:
        -f name:^Test.*
    Multiple filter statements can be provided and all will be processed. The
    default logic of the filters is an "OR" logic, but can be changed to an
    "AND" logic with the "-a" switch.
    Filtering can be useful for searching and tuning output in a table, or to
    refine data being piped into another instance of the program.

Command pipelining is supported in the program. Pipelining is facilitated by
    passing JSON formatted objects into STDIN and then picking them up as
    STDOUT data in a second instance of the program. When this is done, the
    second instance must be provided with a target method for execution
    (ie: "appliance createNetworkApplianceVlan") in the CLI. When this is done
    the second instance of the program will extract required paramters from
    the STDIN input and pass those parameters into the target method. If
    multiple objects are passed via STDIN, the target method will be executed
    once for each item in a loop.
At times it is necessary to translate between keys in the data when pipelining.
    An example of this is when you use "appliance getNetworkApplianceVlan",
    VLANID numbers are returned under the key name "id". If you pipe this
    output into "appliance deleteNetworkApplianceVlan" to delete all returned
    objects, you will need to use the translation argument below:
        -t "vlanId=id"
    in the second instance of the program. This translation is changing all
    STDIN object keys from "id" to "vlanId" so they can be used in the target
    method properly.
If allowing direct pipeline execution is too risky, you can use the "-o" switch
    in the second program instance. This will prevent execution and instead
    will print out commands which can be used manually to the same effect.

DISCLAIMER: Use this program at your own risk. Automation makes it incredibly
    easy to break an environment quickly. Make sure to you are careful when
    performing significant changes to your environment.
"""


# Built-in libraries
import os
import re
import sys
import json
import inspect
import logging
import argparse

# Installed libraries
import meraki
import argcomplete
from rich.console import Console
from rich.table import Table

# Local libraries
from . import __version__


class Args:
    """
    Namespace object for storage of a method's position, named, and kw
        parameters. Used to help build the argument parsing structure for the
        CLI.

    - func (method): Target method from the Meraki library
    """
    def __init__(self, func):
        self.function = self.method = func
        self.name = self.function.__name__
        # Positional parameter names required by the method
        self.positionals = []
        # Keyword parameter names and default values from the method
        self.keywords = []
        # Name of variable arguments parameter if there is one (ie: *args)
        self.varargs = None
        # Name of variable keywords parameter if there is one (ie: **kwargs)
        self.varkw = None
        # Top statement of the method as it appears in the code (ie: def ...)
        self.signature = inspect.signature(func)
        for value in self.signature.parameters.values():
            # If it appears to be a variable keywords parameter (**kwargs)
            if value.kind == value.VAR_KEYWORD:
                self.varkw = value
            # If it appears to be a variable positional parameter (*args)
            elif value.kind == value.VAR_POSITIONAL:
                self.varargs = value
            # If it has no default value, it is a positional
            elif value.default == inspect._empty:
                self.positionals.append(value)
            else:  # Otherwise it is a keyword parameter
                self.keywords.append(value)


class Parser(argparse.ArgumentParser):
    """
    Customised argparse class with custom error messaging
    """
    def error(self, message: str) -> None:
        """
        Override the error method to output help instead of usage
        """
        self.print_help()  # Display the help info instead of usage
        log.critical(f'\nERROR: {message}')  # Add the error at the bottom
        sys.exit(2)  # Exit with an error code


# Map to enhance CLI argument parser by providing additional parsing
#     context extracted from parameter annotation data types.
ANNOTATION_MAP = {
    inspect._empty: {
        'metavar': 'STRING',
        },
    type(None): {
        'metavar': 'STRING',
        },
    str: {
        'metavar': 'STRING',
        },
    list: {
        'action': 'append',
        'metavar': 'ITEM',
        },
    dict: {
        'metavar': 'JSON_STRING',
        },
    bool: {
        'action': 'store_true',
        },
    int: {
        'type': int,
        'metavar': 'INT',
        },
}


# False if pipe exists behind and we are consuming STDIN
NO_STDIN = os.isatty(0)
# False if pipe exists ahead and we are feeding STDOUT
NO_STDOUT = sys.stdout.isatty()


# Instantiate logger facilities for unit testing
log = logging.getLogger('testing')
log.setLevel(logging.CRITICAL)


def _reconcile_args(parsed_args: argparse.Namespace, filePath: str) -> None:
    """
    Process arguments from a static config file against arguments provided
        at the CLI. Prefer CLI-provided arguments over file-based ones. Also
        prefer the MERAKI_DASHBOARD_API_KEY environment variable over one
        provided by a config file.

    - parsed_args: Parsed arguments namespace object from argparse.
    - filePath: String file path for an existing config file
    """
    if parsed_args.debug:
        log.warning(f'INFO: Loading config file: {filePath}')
    try:  # Catch a JSON parsing failure
        # Open file and load contents with JSON
        fileData = json.loads(open(filePath).read())
    except json.decoder.JSONDecodeError as e:
        # If there is bad JSON data, throw error and exit
        log.critical(f'ERROR: Config file {filePath} contains malformatted'
                     ' JSON data')
        log.critical(e)
        sys.exit(1)
    # Throw error and exit if the type of config file data is incorrect
    if type(fileData) is not dict:
        log.critical('ERROR: Config file data is not dict (object). Data '
                     'must be formatted like: {"argname": "value"}')
        sys.exit(1)
    # Iterate the key, value items in the config file
    for arg, value in fileData.items():
        if arg == "command":  # If we are setting the command we are running
            # Just set it now as it will not exist in the argparse namespace
            #     if the type was not set at all
            parsed_args.command = value
        # If the argument is not an argument in the parser
        if arg not in parsed_args.__dict__:
            log.critical(f'ERROR: Argument from file ({arg}) is not a '
                         'recognized argument for this program')
            sys.exit(1)
        # If the value was not set in the CLI
        if not getattr(parsed_args, arg):
            # If the argument is the API key and there is an environment var
            if arg == 'apiKey' and os.environ.get('MERAKI_DASHBOARD_API_KEY'):
                continue  # Don't set the value, prefer the env variable
            # Set the attribute
            setattr(parsed_args, arg, value)


def _args_from_file(parsed_args: argparse.Namespace) -> None:
    """
    Check some pre-set and CLI-provided locations for a config file and load
        config parameters from that file.

    - parsed_args: Parsed arguments namespace object from argparse.
    """
    # Static file paths to check
    filePaths = [
        'meraki-cli.conf',  # Current working directory
        os.path.join(  # Hidden dot (.) folder in user's directory
            os.path.expanduser("~"),
            '.meraki-cli',
            'meraki-cli.conf'
            ),
        os.path.join(  # Standard MacOS app config directory
            os.path.expanduser("~"),
            'Library',
            'Application Support',
            'meraki-cli',
            'meraki-cli.conf'
            ),
        '/etc/meraki-cli/meraki-cli.conf',  # Standard Linux config directory
    ]
    # Environment variable directories to check
    envPaths = [
        'APPDATA',  # Windows roamed user settings directory
        'LOCALAPPDATA',  # Windows machine-specific user settings directory
    ]
    # If a config file path was provided from the CLI
    if parsed_args.configFile:
        # If that file doesn't exist, throw error and exit
        if not os.path.isfile(parsed_args.configFile):
            log.critical(f'Defined config file ({parsed_args.configFile})'
                         ' does not exist')
            sys.exit(1)
        # If it does exist, process it
        _reconcile_args(parsed_args, parsed_args.configFile)
    else:  # If a path wasn't provided from the CLI
        # Loop through environment variable paths
        for envPath in envPaths:
            # Grab the value (None if non-existant)
            value = os.environ.get(envPath)
            if value:  # If there was an env variable
                # Use ./meraki/meraki.conf as the path
                filePath = os.path.join(value, 'meraki-cli', 'meraki-cli.conf')
                # If the file exists in that path
                if os.path.isfile(filePath):
                    # Process it
                    _reconcile_args(parsed_args, filePath)
                    return None
        # Loop through the static file paths
        for filePath in filePaths:
            if os.path.isfile(filePath):  # If this file exists
                _reconcile_args(parsed_args, filePath)  # Process it
                return None  # And quit the function


def _configure_logging(parsed_args: argparse.Namespace) -> ():
    """
    Prepare and return two logging objects: one for the general program, and
        another for the Meraki library. Uses arguments from the CLI to set
        debugging levels and lof file options.

    - parsed_args: Parsed arguments namespace object from argparse.
    """
    log = logging.getLogger('default')  # General program logging object
    meraki_log = logging.getLogger('meraki')  # Meraki logging object
    # Add in a timestamp and logging level to each message
    format = logging.Formatter(
        "%(asctime)s [%(levelname)-5.5s]  %(message)s"
        )
    # STDERR default handler for terminal output
    handler = logging.StreamHandler()
    handler.setFormatter(format)
    # Apply handler to logging objects
    log.addHandler(handler)
    meraki_log.addHandler(handler)
    # Set debug level based on CLI arguments
    if parsed_args.debug == 1:
        log.setLevel(logging.INFO)
    elif parsed_args.debug == 2:
        log.setLevel(logging.INFO)
        meraki_log.setLevel(logging.DEBUG)
    elif parsed_args.debug > 2:
        log.setLevel(logging.DEBUG)
        meraki_log.setLevel(logging.DEBUG)
    # If a logfile location was defined
    if parsed_args.logfile:
        # Create a handler to write the file
        fileHandler = logging.FileHandler(parsed_args.logfile)
        # Add the formatter
        fileHandler.setFormatter(format)
        # And apply the handler to both logging objects
        log.addHandler(fileHandler)
        meraki_log.addHandler(fileHandler)
    return log, meraki_log


def _log_exception(exception, exit=False) -> None:
    """
    Check the current debug level and log a thrown exception if we are
        debugging. Then exit the program if switch was thrown.

    - exception: Exception object which was caught in caller
    - exit: Boolean of whether or not to exit the program
    """
    if log.level >= logging.INFO:  # If we are debugging at all
        log.warning('An exception was thrown and is logged below')
        log.exception(exception)
    if exit:
        sys.exit()


def _cmd_title(mtdstr: str) -> str:
    """
    Generate command/method title, based on its name, which is
        displayed in the list of commands under a type (class).

    - mtdstr: String name of the method (ie: 'getOrganizations')
    """
    # Split into a list of words based on capital characters
    wordlist = re.sub(r"([A-Z])", r" \1", mtdstr).split()
    wordlist[0] = wordlist[0].capitalize()  # Capitalize the first word
    return ' '.join(wordlist).title()  # Camel case all words and join them


def _cmd_help(arg_obj: Args) -> str:
    """
    Generate the description/instructions section in a command/method's help
        text. Use the docstring of the method and add the method's signature
        (top line from the code) at the bottom.

    - mtdstr: String name of the method (ie: 'getOrganizations')
    """
    result = arg_obj.method.__doc__  # Start with the doc string
    # Set the docstring header (wrapped in asterisks) to uppercase
    result = re.sub(r'\*\*(.*)\*\*', lambda ele: ele.group(0).upper(), result)
    # Remove leading tabs from header and add en extra line break
    result = re.sub(r'\t\t\*\*(.*)\*\*', r'\1\n', result)
    # Remove leading tabs from link
    result = re.sub(r'\t\t(https://.*)\n', r'\1', result)
    if arg_obj.positionals:  # If there are positional (required) arguments
        # Add an "All Arguments" line below http for the argument entries
        result = re.sub(r'(https://.*)\n', r'\1\n\nAll Arguments:\n', result)
    # Remove leading tabs from argument entries and append double-hypen
    result = re.sub(r'\t\t- ([a-zA-Z0-9_]+) ', r'  --\1 ', result)
    # Add the signature at the bottom of the help.
    result += '\nFunction Signature:\n\t'\
              f'>>> def {arg_obj.name}{arg_obj.signature}:'
    return result


def _clean_args(parsed_args: argparse.Namespace):
    """
    Remove static arguments from the parsed namespace to obtain a dict of
        only the provided parameters to be used on the target function.

    - parsed_args: Parsed arguments namespace object from argparse.
    """
    # Start with a copy of the namespace dict so it can be modified.
    arg_dict = dict(parsed_args.__dict__)
    # Iterate a list of known static arguments
    for key in ['apiKey', 'debug', 'logfile', 'jsonOutput', 'configFile',
                'type', 'filters', 'and_logic', 'command', 'kwargs',
                'columns', 'translations', 'output_commands']:
        try:
            del arg_dict[key]  # Remove each from the dict
        except KeyError:
            pass
    return arg_dict


def _get_method_params(parsed_args: argparse.Namespace,
                       arg_dict: dict, arg_obj: Args) -> ():
    """
    Transform provided CLI arguments into positional and keyword parameters
        based on the needs of the target method.

    - parsed_args: Parsed arguments namespace object from argparse.
    - arg_dict: Cleaned dict of arguments from CLI. Example:
        {'vlanId': "100"}
    - arg_obj: Instance of the Args() class which holds parameter info for the
        target method.
    """
    positionals = []  # Start with an empty list of positional parameter values
    for param in arg_obj.positionals:
        try:
            positionals.append(arg_dict[param.name])  # Add each needed value
        except KeyError:  # If we are missing one
            log.critical(f'ERROR. Cannot find "{param.name}". May need to be '
                         'translated from an input key with the "-t" argument')
            sys.exit()
        # Remove from the arg_dict so it does not get passed in as keyword
        del arg_dict[param.name]
    # If variable keywords (**kwargs) are allowed by the method and we are
    #     not consuming piped data from STDIN
    if arg_obj.varkw and NO_STDIN:
        # Get the value of the varkw argument from the CLI
        kwargs_value = getattr(parsed_args, arg_obj.varkw.name)
        if kwargs_value:  # If a value was provided at the CLI
            try:
                kwargs = json.loads(kwargs_value)  # Interpret the JSON
                log.debug(f'Loaded kwargs:\n{json.dumps(kwargs, indent=4)}')
                arg_dict.update(kwargs)  # Add the data to the keyword values
            except json.decoder.JSONDecodeError as e:
                log.critical('Error loading JSON kwargs. Check syntax.')
                log.exception(e)
                sys.exit()
    return (positionals, arg_dict)


def _translate_input(arg_dicts: list, translation_strs: list) -> []:
    """
    Flip the key values of objects provided by STDIN so they match the
        required paramter names of the target method.

    - arg_dicts: List of dict arguments interpreted from STDIN. Example:
        [{'vlanId': "100"}, {'vlanId': "200"}]

    - translation_strs: List of string translation statements. Example:
        ["id=vlanId", "name=description"]
    """
    translations = {}  # Start with no translations
    try:  # Catch exceptions with poorly formatted translations
        for translation_str in translation_strs:
            # Output key, and Input Key
            okey, ikey = translation_str.split('=')
            translations[ikey] = okey  # Add to dict for lookups
    except Exception as e:
        log.critical(f'Could not interpret translation: "{translation_str}"')
        # Log the exception and exit
        _log_exception(e, exit=True)
    log.debug(f'Built translations:\n{json.dumps(translations, indent=4)}')
    result = []  # Start with no result objects (dicts)
    for arg_dict in arg_dicts:
        new_dict = {}
        for key, value in arg_dict.items():
            if key in translations:  # If a translation key exists
                # Add to the new dict under the replacement key name
                new_dict[translations[key]] = value
            else:
                new_dict[key] = value  # Use the original key name
        result.append(new_dict)
    return result


def _json_to_args(json_string: str, parsed_args: argparse.Namespace,
                  arg_obj: Args) -> []:
    """
    Parse a raw JSON string into method-ready arguments. Parse JSON into
        objects, run them through a translator if the user provided key
        translations, reconcile them with CLI inputs from the user (preferring
        arguments from the user) and conform the arguments to the parameters
        required by the target method.

    - json_string: String of valid JSON objects. Example:
        '[{"vlanId": "100"}]'
    - parsed_args: Parsed arguments namespace object from argparse.
    - arg_obj: Instance of the Args() class which holds parameter info for the
        target method.
    """
    result = []
    stdin_arg_dicts = json.loads(json_string)  # Interpret as JSON
    log.debug(f'Loaded STDIN data: {stdin_arg_dicts}')
    if type(stdin_arg_dicts) is not list:  # Make a list if not a list
        stdin_arg_dicts = [stdin_arg_dicts]
    if parsed_args.translations:  # If translations were provided from the CLI
        # Run the arguments through the translator
        stdin_arg_dicts = _translate_input(stdin_arg_dicts,
                                           parsed_args.translations)
        log.debug(f'Translated STDIN data: {stdin_arg_dicts}')
    # Clean static args from CLI arguments
    cli_arg_dict = _clean_args(parsed_args)
    log.debug(f'Cleaned CLI Arguments: {cli_arg_dict}. '
              'Reconciling CLI and STDIN...')
    # Override STNIN values with CLI-provided args if any were provided. This
    #     allows the user to adjust one or more parameters of the input as it
    #     is piped from the output of one instance to the input of another.
    for key, value in cli_arg_dict.items():  # Iterate CLI arguments
        if value:  # If the argument was provided
            log.debug(f'Overriding arg "{key}" in STDIN args with CLI value.')
            # Iterate all the items from STDIN
            for stdin_arg_dict in stdin_arg_dicts:
                # And replace their values
                stdin_arg_dict[key] = value
    # Iterate the final argument values and conform them to the target method
    for arg_dict in stdin_arg_dicts:
        # Pull the positional and keyword args in a tuple
        arg_tup = _get_method_params(parsed_args, arg_dict, arg_obj)
        result.append(arg_tup)
    return result


def _get_stdin_args(parsed_args: argparse.Namespace, arg_obj: Args) -> []:
    """
    Get input objects from a pipeline (STDIN), run them through a translator
        if the user provided key translations, reconcile them with CLI inputs
        from the user (preferring arguments from the user) and conform the
        arguments to the parameters required by the target method.

    - parsed_args: Parsed arguments namespace object from argparse.
    - arg_obj: Instance of the Args() class which holds parameter info for the
        target method.
    """
    stdin = sys.stdin.read()  # Get the raw STDIN data
    log.debug(f'Raw STDIN data:\n{stdin}')
    if not stdin:  # If the STDIN data is empty
        log.critical('STDIN is empty. Source instance returned no data. '
                     'Exiting program.')
        sys.exit()
    return _json_to_args(stdin, parsed_args, arg_obj)


class ExtrasParser(argparse.ArgumentParser):
    """
    Customised argparse class for minimal errors on parsing extra args for
        use in kwargs
    """
    def error(self, message: str) -> None:
        """
        Override the error method to output minimal info
        """
        log.critical(message)  # Output using our logging
        sys.exit(2)  # Exit with an error code


def _extra_args_to_kwargs(existing_kwarg_dict: dict, arglist: list) -> {}:
    """
    Interpret a list of 'extra' uninterpreted arguments from the CLI into a
        dict of arguments which are then combined with the existing kwargs
        dict. This resulting kwargs dict is then passed into the target method
        for keyword parameters as well as target_method(**kwargs) for POST
        bodies in the API.

    - existing_kwarg_dict: Dict of existing kwargs from the main interpreter
    - arglist: List of extra, unrecognized CLI arguments discarded by the
        primary parser.
    """
    if not arglist:  # If there were no extra arguments provided
        return existing_kwarg_dict  # Just return what we started with
    parser = ExtrasParser()  # Instantiate our custom parser class
    for arg in arglist:  # For each of the words in the unparsed arguments
        if arg[:2] == '--':  # If the args starts with two hyphens
            parser.add_argument(arg)  # Add it as an argument in the parser
    # Parse known args so we ignore any extra info in the CLI (like comments)
    #     and grab the first entry from the tuple (since it will pass thru
    #     any other extras)
    args = parser.parse_known_args(arglist)[0]
    extra_arg_dict = {}  # Start with an empty dict for the extra args
    # Iterate each key, value pair in the parsed args
    for key, value in args.__dict__.items():
        try:  # Allow JSON parsing to fail
            # Try to read as JSON data in case it is nested
            data = json.loads(value)
            # If the data is a list or a dict
            if type(data) is list or type(data) is dict:
                # Then add it as that native data type
                extra_arg_dict[key] = json.loads(value)
            else:  # If it is not a list or a dict
                extra_arg_dict[key] = value  # Add it as the standard string
        except Exception:  # If this was non-compliant JSON data
            extra_arg_dict[key] = value  # Add it as the stnadard string
    # Merge the extra_arg_dict into the existing kwargs
    existing_kwarg_dict.update(extra_arg_dict)
    return existing_kwarg_dict  # And return it for use in the target method


def _print_commands(parsed_args: argparse.Namespace,
                    argtups: tuple, arg_obj: Args) -> None:
    """
    Generate commands which can be used manually to execute the same changes
        as would be executed during the pipeline automatically. These are
        useful for testing changes before you push them automatically.

    - parsed_args: Parsed arguments namespace object from argparse.
    - argtups: Tuple of positional and keyword arguments destined to be passed
        directly into the target method. Example:
        [(['positional1', 'positional2'], {'key1': 'value1'})]
    - arg_obj: Instance of the Args() class which holds parameter info for the
        target method.
    """
    # Start with the beginning of the command so we can add to it
    prepend = f'{sys.argv[0]} {parsed_args.type} {parsed_args.command}'
    print()
    for argtup in argtups:
        cmd = prepend  # Make a copy of the prepend string
        pos_args = argtup[0]  # Grab the positional arguments
        named_args = argtup[1]  # Grab the named/keyword arguments
        # Iterate the needed positional arguments and the positional
        #     argument values simultaneously
        for param, value in zip(arg_obj.positionals, pos_args):
            # Generate the CLI argument and add it to the command
            cmd += f" --{param.name} '{value}'"
        # If there are variable keyword arguments allowed by the method
        if arg_obj.varkw:
            # Generate a JSON dump of the keyword arguments
            json_data = json.dumps(named_args)
            # And add that JSON dump as a command argument
            cmd += f""" --{arg_obj.varkw.name} '{json_data}' """
        # Print the commands with spaces
        print(cmd)
        print()


def _object_filter(listofdicts: list, filter_strs: list,
                   and_logic=False) -> []:
    """
    Filter objects out of the result of a method call. Used by the "-f"
        filter to filter displayed or pipelined output.

    - listofdicts: List of dictionary objects where each dictionary is a series
        of attributes which can be matched against and filtered. Example:
        [{'id': '1', 'name': 'THING1'}, {'id': '2', 'name': 'THING2'}]
    - filter_strs: List of strings which are filter definitions. Example:
        ['name:^m...$', 'id:10...']
    - and_logic: Boolean of whether or not to use "AND" between filters or to
        use "OR" as is default.

    """
    log.debug(f'Starting item filter. Using "AND" logic: {and_logic}')
    # Return the data if it is not a list. We can't filter just one.
    if type(listofdicts) is not list:
        log.error(f'Cannot filter non-list. Returning data: {listofdicts}')
        return listofdicts
    filters = []  # Build list of dicts for filter definitions.
    for filter_str in filter_strs:  # Iterate user provided strings to parse
        # Extract the key name up to the colon
        key = re.search('^[a-zA-Z0-9].*?:', filter_str).group(0)
        # Grab the remaining string for the regex
        regex = filter_str[len(key):]
        key = key.replace(':', '')
        # If the provided filter key is not in the object attributes
        if key not in listofdicts[0]:
            raise KeyError(f'Filter key "{key}" does not exist in data')
        filters.append({'key': key, 'regex': regex})
    log.debug(f'Built regex filters:\n{json.dumps(filters, indent=4)}')
    result = []
    # Perform the actual filtering now. The 'fdict' variable will be a filter
    #     definition in dict form. Example:
    #     {'key': 'name', 'regex': '^Test Site.*$'}
    for item in listofdicts:
        # Use enumerate and an index so we can track how many of the filters
        #     have passed so far. This is used for the "AND" logic filtering
        for index, fdict in enumerate(filters):
            # If our regex generates a match with the value of the attribute
            if re.search(fdict['regex'], str(item[fdict['key']])):
                if and_logic:  # If we are using "AND" filter logic
                    # If this is the very last filter to be processed
                    if index+1 == len(fdict):
                        # The item passes in the "AND" logic. Add it to the
                        #      result and break the loop
                        result.append(item)
                        break
                else:  # If we are using "OR" logic
                    # Add the item since it passed this filter and break the
                    #     loop
                    result.append(item)
                    break
            else:  # If we didn't generate a match in this filter
                if and_logic:  # And we are using "AND" logic
                    break  # Break the loop to discard the item
    return result


def _table_ready_dicts(listofdicts: list) -> []:
    """
    Prepare a list of dict objects for printing to a table. Each dict is a
        set of object atributes where the key will be the table column name.
        The dicts are prepared by discarding any values which cannot be easily
        printed into a table cell (like lists, dicts, etc).
    The input should be a list of dictionaries, but might be something else.
        If it is something else, then we need to modify it to be ready for
        tabluation.

    - listofdicts: List of dictionary objects where each dictionary is a series
        of attributes which can be matched against and filtered. Example:
        [{'id': '1', 'name': 'THING1'}, {'id': '2', 'name': 'THING2'}]
    """
    result = []
    #################################################
    # Check For Nested Data
    if type(listofdicts) is dict:  # If we were given a dict instead of a list
        if (
                len(listofdicts) == 1  # If the dict has one kv pair
                and
                # The value of that kv pair is a list
                type(list(listofdicts.values())[0]) is list
                and
                # The entries in that list are dicts
                type(list(listofdicts.values())[0][0]) is dict
                ):
            # Use the lsit from the kv pair as the list of dicts
            listofdicts = list(listofdicts.values())[0]
        else:
            listofdicts = [listofdicts]
    #################################################
    # Strip Bad Types
    bad_types = [dict, list]  # Types of data we want to discard
    for d in listofdicts:
        newdict = {}  # Use a new dict instead of deleting kv pairs
        for k, v in d.items():
            if type(v) not in bad_types:
                newdict[k] = str(v)
            else:
                log.debug(f'Discarding data in table squash: {k}: {v}')
        result.append(newdict)
    #################################################
    return result


def _column_filter(listofdicts: list, columns_str: str) -> []:
    """
    Filter out and reorder key,value pairs in a list of dicts destined to be
        printed to a table.

    - listofdicts: List of dictionary objects where each dictionary is a series
        of attributes which can be matched against and filtered. Example:
        [{'id': '1', 'name': 'THING1'}, {'id': '2', 'name': 'THING2'}]

    - columns_str: String of comma-seperated column names. Will be split on
        the comma and used to filter and reorder the object attributes in the
        listofdicts. Example:
        'id,name,description'
    """
    columns = columns_str.replace(' ', '')  # Remove whitespace
    columns = columns_str.split(',')
    result = []
    for d in listofdicts:
        newdict = {}
        # Iterate column names to maintain preferred column order
        for column in columns:
            if column in d:  # If the column name can be found in the keys
                newdict[column] = d[column]
            else:
                log.warning(f'Column "{column}" not found in data. Skipping.')
        result.append(newdict)
    return result


def _nice_table(listofdicts: list) -> None:
    """
    Print out a nicely formatted table from a list of dicts.

    - listofdicts: List of dictionary objects where each dictionary is a series
        of attributes which can be matched against and filtered. Example:
        [{'id': '1', 'name': 'THING1'}, {'id': '2', 'name': 'THING2'}]
    """
    if not listofdicts:
        log.warning('Empty table data. Exiting.')
        sys.exit()
    console = Console()  # Instantiate the Rich console
    # Instantiate the table object with header settings
    table = Table(show_header=True, header_style="bold magenta")
    # For each header column name in the first dict in the list
    for head in listofdicts[0]:
        table.add_column(head)  # Add that header column name
    for d in listofdicts:
        # Add the dict values as args to table.add_row
        table.add_row(*list(d.values()))
    console.print(table)  # Print out the table


def _output(parsed_args: argparse.Namespace, result: list) -> None:
    """
    Output the results of a task in table or JSON format for the CLI.

    - parsed_args: Parsed arguments namespace object from argparse.
    - result: Preferrably a list but possibly a dictionary object
        attributes. List Example:
        [{'id': '1', 'name': 'THING1'}, {'id': '2', 'name': 'THING2'}]
    """
    if not result:  # If the result is empty
        log.info('Result data is empty. But command may have been successful.')
        return None
    # If user is requesting JSON output, or we detected that we are feeding
    #     the output into a pipeline. The "not NO_STDOUT" is indeed a double
    #     negative. It is confusing but unavoidable.
    if parsed_args.jsonOutput or not NO_STDOUT:
        log.debug(f'Outputting to JSON. '
                  f'Forward pipelining: {not NO_STDOUT}')
        print(json.dumps(result, indent=4))
    else:  # Otherwise let's try to output a nice table.
        # Prepare data to be formatted into a table by removing value
        #     types unfriendly to tabulation.
        tabledicts = _table_ready_dicts(result)
        # If the user has defined column filtering/ordering
        if parsed_args.columns:
            tabledicts = _column_filter(tabledicts, parsed_args.columns)
        _nice_table(tabledicts)  # Output our nice table to the CLI


def main(argstring=None) -> None:
    """
    Primary function called from native script. Allow an argument string to
        be passed in for testing purposes.
    """
    # Instantiate a fake instance of the API so we can parse it and build the
    #     argparse structure from it
    api = meraki.DashboardAPI('fake_key', suppress_logging=True)
    # Start our arg parser instance
    parser = Parser(add_help=False)
    argcomplete.autocomplete(parser)
    # Structure top level arguments into groups to make them easier to read.
    #     Any arguments added here need to also be listed in the _clean_args
    #     function so they can be stripped from parameters passed into target
    #     methods
    basic_group = parser.add_argument_group('Basic Arguments')
    basic_group.add_argument('-h', '--help',
                             help='Show help at any command level',
                             action='help')
    basic_group.add_argument('-v', '--version',
                             version=f'Meraki-CLI v{__version__} | '
                             f'Meraki API Library v{meraki.__version__}',
                             action="version")
    basic_group.add_argument('-k', '--apiKey',
                             help='Meraki API Access Key',
                             metavar='STRING',
                             dest='apiKey')
    basic_group.add_argument('-d', "--debug",
                             help='Set debug level 1-3 (ie: -d or -dd)',
                             dest="debug",
                             default=0,
                             action='count')
    basic_group.add_argument('-l', '--logfile',
                             help='Write logs to a logfile',
                             metavar='PATH',
                             dest='logfile')
    basic_group.add_argument('-c', '--configFile',
                             help='Use a config file for some arguments',
                             metavar='PATH',
                             dest='configFile')
    output_group = parser.add_argument_group('Output Formatting')
    output_group.add_argument('-j', '--jsonOutput',
                              help='Format output as JSON insted of default',
                              dest='jsonOutput',
                              action='store_true')
    output_group.add_argument('-s', '--columns',
                              help='Filter/Order Table Columns '
                              '(ie: id,networkId,etc)',
                              metavar='STRING',
                              dest='columns')
    filtering_group = parser.add_argument_group('Filtering')
    filtering_group.add_argument('-f', '--filter',
                                 help='Search filter for returned items '
                                 '(ie: "name:Headquarters")',
                                 metavar='STRING',
                                 dest='filters',
                                 action='append')
    filtering_group.add_argument('-a', '--and_logic',
                                 help='Use "AND" logic for multiple filters '
                                 'instead of default "OR"',
                                 dest='and_logic',
                                 action='store_true')
    pipe_group = parser.add_argument_group('Pipelining')
    pipe_group.add_argument('-t', '--translation',
                            help='Key translation for piped input '
                            '(ie: "id=vlanId")',
                            metavar='STRING',
                            dest='translations',
                            action='append')
    pipe_group.add_argument('-o', '--output_commands',
                            help='Output formatted commands instead of '
                            'executing actions.',
                            dest='output_commands',
                            action='store_true')
    # Start a dict map of the argument structure. We will use this once the
    #     CLI args have been parsed to look back and see what parameters are
    #     required by the target method. This is necessary because it doesn't
    #     seem possible to navigate the result argparse object to find this
    #     information.
    parser_map = {}
    # This will contain the command types like "networks" or "switch"
    subparser = parser.add_subparsers(dest='type', title='Command Types')
    # Iterate class strings and classes in the fake API instance
    for clsstr, cls in api.__dict__.items():
        if clsstr[0] == "_":  # If this is a private attribute
            continue  # Don't add it to the argument parser
        # Add the type command for this class
        tparser = subparser.add_parser(clsstr, help=f'{clsstr} commands')
        # Add a container for target method commands within this type
        tsub = tparser.add_subparsers(dest='command', title='Commands')
        # Add the type command to the map. Will use this later to print the
        #     help section of the command type
        parser_map[clsstr] = {'_parser': tparser}
        # For method string in the class
        for mtdstr in dir(cls):
            if mtdstr[0] == "_":  # Skip if private
                continue
            # Instantiate an Args object to parse the parameters required by
            #     the method and make them easy to access.
            arg_obj = Args(getattr(cls, mtdstr))
            # Add a command endpoint for this method to contain the argument
            #     options
            cmd = tsub.add_parser(
                mtdstr,  # Use the method name for the command endpoint
                add_help=False,  # Disable auto help since we add it manually
                help=_cmd_title(mtdstr),  # Grab the help section (title)
                description=_cmd_help(arg_obj),  # Grab the help section
                # Use a raw formatter to allow the help docstring to maintain
                #     it's multi-line format
                formatter_class=argparse.RawTextHelpFormatter)
            # A nice group for required (positional) arguments
            req_group = cmd.add_argument_group('Required Arguments')
            # A nice group for known optional (kwargs, help) arguments
            msc_group = cmd.add_argument_group('Misc Arguments')
            # Add help manually
            msc_group.add_argument('-h', '--help',
                                   help='Show help for this command',
                                   action='help')
            # Add the method parameter info into the map
            parser_map[clsstr][mtdstr] = arg_obj
            # Iterate the positionals and create argument options for each
            for arg in arg_obj.positionals:
                req_group.add_argument(f'--{arg.name}',
                                       dest=arg.name,
                                       help='(required)',
                                       # Don't require the arg if we are
                                       #     parsing the STDIN data
                                       required=NO_STDIN,
                                       # Use the annotation map to pass
                                       #     additional params to the
                                       #     argument option to make it
                                       #     easier to use and read
                                       **ANNOTATION_MAP[arg.annotation])
                # Add the parameter name to the positionals list in the map
            for arg in arg_obj.keywords:
                msc_group.add_argument(f'--{arg.name}',
                                       dest=arg.name,
                                       default=arg.default,
                                       # NOTE: These are never required.
                                       help=f'(default = {arg.default})',
                                       **ANNOTATION_MAP[type(arg.default)])
            if arg_obj.varkw:
                msc_group.add_argument(f'--{arg_obj.varkw.name}',
                                       dest=arg_obj.varkw.name,
                                       help='(Advanced Users) Optional '
                                            'arguments in JSON format ',
                                       metavar='JSON_STRING',)
    # If an argstring was passed in, we are probably being tested
    if argstring:
        # Split up the args and pass them in as a list to be parsed
        args, extraarglist = parser.parse_known_args(argstring.split(' '))
    else:
        # Parse the user provided CLI commands/args
        args, extraarglist = parser.parse_known_args()
    global log  # Make the "log" variable global to anybody can use it
    log.setLevel(logging.DEBUG)
    _args_from_file(args)  # Process any arguments from a file
    # Pull in the two logging systems
    log, meraki_log = _configure_logging(args)
    log.debug(f'Argument Settings: \n{json.dumps(args.__dict__, indent=4)}')
    if not args.type:  # If a type (networks, switch, etc) wasn't specified
        parser.print_help()  # Print help so the user can see options
        sys.exit()  # And exit the program
    if not args.command:  # If a command wasn't provided but a type was
        # Print the specific help for that command type
        parser_map[args.type]['_parser'].print_help()
        sys.exit()
    try:  # Catch an exception where the API key has not been provided at all
        if args.apiKey:
            log.debug('Instantiating Meraki API with defined API key')
            # Instantiate the real API object
            api = meraki.DashboardAPI(args.apiKey, suppress_logging=True)
        else:
            log.debug('Instantiating Meraki API with environment API key')
            api = meraki.DashboardAPI(suppress_logging=True)
    except meraki.exceptions.APIKeyError:  # If no API key was provided
        log.critical('Meraki API key not provided. Use the "-k" argument or '
                     'set an environment variable like: export '
                     'MERAKI_DASHBOARD_API_KEY=12345abcde')
        sys.exit()
    # Set all of the logger objects inside the API to the one we built
    api._logger = api._session.logger = api._session._logger = meraki_log
    # Grab the target method we intend to call
    target_method = getattr(getattr(api, args.type), args.command)
    log.info(f'Target method is {target_method}')
    if NO_STDIN:  # If not in front of a pipe (not being fed by STDIN)
        log.info('No STDIN detected. No pipe behind this instance.')
        # Remove the static args and get a clean dict back only containing
        #     argument meant to become parameters in the target method call
        arg_dict = _clean_args(args)
        log.debug(f'Cleaned Arguments: {arg_dict}')
        # Pull a list of tuples, each containing the parameters tailored for a
        #     call against the target method.
        # Tuple should have a list of positional arguments in [0] and a dict
        #     of dict of keyword args in [1]
        # _get_method_params returns a single tuple, but we loop through them
        #      below so we manually put that tuple in a list here.
        argtups = [_get_method_params(args, arg_dict,
                                      parser_map[args.type][args.command])]
    else:  # If we are being fed by STDIN through a pipeline
        log.info('STDIN detected. Pipe exists behind this instance.')
        # Pull a list of tuples, each containing the parameters tailored for a
        #     call against the target method.
        # Tuple should have a list of positional arguments in [0] and a dict
        #     of dict of keyword args in [1]
        argtups = _get_stdin_args(args, parser_map[args.type][args.command])
        log.debug(f'Arguments generated from STDIN: \n'
                  f'{json.dumps(argtups, indent=4)}')
    # If the user threw the switch to output commands instead of execute
    #     them
    if args.output_commands:
        log.debug('Outputting piped args as commands and cancelling '
                  'execution.')
        # Print the commands to STDOUT and exit the program
        _print_commands(args, argtups, parser_map[args.type][args.command])
        sys.exit()
    # Iterate through the argument tuples in this list. If the data came from
    #     STDIN, then we may have multiple argument sets to execute. If the
    #     data came from the CLI, then it is a list with one entry.
    for argtup in argtups:
        # Extract the positional and keyword args from the data
        positionals = argtup[0]
        if parser_map[args.type][args.command].varkw:
            arg_dict = argtup[1]
        else:
            arg_dict = {}
        if extraarglist:
            arg_dict = _extra_args_to_kwargs(arg_dict, extraarglist)
        log.info('Calling target method with:')
        log.info(f'    *Positionals: {positionals}')
        log.info(f'    **Named/Kwargs: {arg_dict}')
        try:  # Catch exceptions in method call
            # Call the target method to execute the command
            result = target_method(*positionals, **arg_dict)
        except Exception as e:
            if NO_STDIN:  # If not in front of a pipe (not being fed by STDIN)
                log.critical('An error occured in command execution, enable '
                             'debugging to see more detail')
                _log_exception(e, exit=True)
            else:  # If we are in front of a pipe
                # Log the exception but don't exit the program
                _log_exception(e)
        log.debug(f'Target method result: \n{json.dumps(result, indent=4)}')
        if args.filters:  # If we are supposed to filter result objects
            # Run the results through the filter
            result = _object_filter(result, args.filters,
                                    and_logic=args.and_logic)
            log.debug(f'Item list after filtering:'
                      f'\n{json.dumps(result, indent=4)}')
        # And output them for the user or pipeline
        _output(args, result)


if __name__ == "__main__":
    main()
