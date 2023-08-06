import re

## List of netbox slugs that map to 'switch or router' roles
# that the ETL copied from equipdb
EQUIPDB_SWITCH_OR_ROUTER = [
    'switch-or-router-access-layer',
    'switch-or-router-bin',
    'switch-or-router-core',
    'switch-or-router-data-center',
    'switch-or-router-distribution-layer',
    'switch-or-router-distribution-access-layer',
    'switch-or-router-other',
    'switch-or-router-out-of-band',
    'switch-or-router-terminal-server',
    'switch-or-router-umd',
    'switch-or-router-voice',
]


### List of UM subnets ####
IPV4_UMNETS = [
    '10.0.0.0/9',
    '10.160.0.0/11',
    '10.196.0.0/14',
    '10.194.0.0/16',
    '10.211.0.0/16',
    '10.212.0.0/16',
    '10.213.0.0/16',
    '10.224.0.0/11',
    '35.0.0.0/17',
    '35.0.192.0/18', # Ignoring NCRC Guest
    '35.1.0.0/16',
    '35.2.0.0/16',
    '35.3.0.0/16',
    '35.5.0.0/16',
    '35.7.0.0/16',
    '67.194.0.0/16',
    '141.211.0.0/16',
    '141.212.0.0/16',
    '141.213.0.0/16',
    '172.21.0.0/16',
    '172.23.0.0/16',
    '172.28.0.0/16',
    '192.168.0.0/16',
    '198.108.8.0/21',
    '198.111.224.0/22',
    '207.75.144.0/20',
    '192.231.253.0/24',
]

## Maps interface prefix abbreviations
# for easy expansion (or un-expansion) lookups
I_ABBR = {
    'Gi': 'GigabitEthernet',
    'Te': 'TenGigabitEthernet',
    'Fa': 'FastEthernet',
}

#### NSO constants #########

# Namespace, useful for xpath queries of lxml elements
NSO_NAMESPACE = "http://tail-f.com/ns/ncs"

## Maps NSO NEDs and types to netbox platforms
NETBOX_NSO_NEDS = {
    'JUNOS_EX': {
        'device-type':'netconf',
        'ned-id':'juniper-junos-nc-3.0',
        },
    'JUNOS_EX_ELS': {
        'device-type':'netconf',
        'ned-id':'juniper-junos-nc-3.0',
        },
    'JUNOS_MX': {
        'device-type':'netconf',
        'ned-id':'juniper-junos-nc-3.0',
        },
    'JUNOS_QFX': {
        'device-type':'netconf',
        'ned-id':'juniper-junos-nc-3.0',
        },        
    'CISCO_IOS': {
        'device-type':'cli',
        'ned-id':'cisco-ios-cli-3.8',
        },        
}


##########################
#### Regex constants #####

# Mac address
_MAC_A = '[a-f0-9]{4}\.[a-f0-9]{4}\.[a-f0-9]{4}'
_MAC_B = '[a-f0-9]{2}[:-][a-f0-9]{2}[:-][a-f0-9]{2}[:-][a-f0-9]{2}[:-][a-f0-9]{2}[:-][a-f0-9]{2}'
MAC_RE = re.compile('^(' + _MAC_A + '|' + _MAC_B + ')$', flags=re.IGNORECASE)

# Lazy regexes for ipv4 and ipv6
IPV4_ADDR_RE = re.compile('^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$')
IPV6_ADDR_RE = re.compile('[a-f0-9:]+$')
IPV4_NET_RE = re.compile('^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2}$')
IPV6_NET_RE = re.compile('[a-f0-9:]+/\d{1,3}$')

UMICH_FQDN_RE = re.compile('^[\w.-]+.umich.edu')
NETNAME_RE = re.compile('^(D|V|L3|O|CFW|DFW|NGFW|VFW|IPS)[\-\w]+$')


