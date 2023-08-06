import os
from netaddr import *
from .constants import I_ABBR
import re

def get_env_vars(vars_list):
    '''
    Pull list of variables from the environment,
    store in dict
    '''
    results = {}
    for var in vars_list:
        val = os.getenv(var)
        if val:
            results[var] = val
        else:
            print(f"ERROR: Please set {var} environment variable")
            quit()

    return results

def is_ip_network(input_str, version=None):
 
    # First check that this is a valid IP or network
    try:
        net = IPNetwork(input_str)
    except:
        return False

    # Now verify it's a network and not an IP by
    # converting back to string and checking it's the same
    if(str(net) != input_str):
        return False

    if version and version != net.version:
        return False
    
    return True

def is_ip_address(input_str, version=None):
    try:
        ip = IPAddress(input_str)
    except:
        return False

    if version and version != ip.version:
        return False

    return True

def is_mac_address(input_str):
    try:
        EUI(input_str)
    except:
        return False

    return True

def expand_interface(input_str):
    '''
    Expands a cisco interface to its full name.
    If no match is found, the string is returned
    unchanged
    '''
    for short, long in I_ABBR.items():
        if re.search(f'{short}\d',input_str):
            return input_str.replace(short, long)
    return input_str

