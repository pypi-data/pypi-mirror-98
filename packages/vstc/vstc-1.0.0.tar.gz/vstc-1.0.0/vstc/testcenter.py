'''
Virtual Spirent TestCenter
'''
from typing import NoReturn, Tuple, Union, Optional, List
import re
import os

from enum import Enum
from abc import ABC, abstractmethod

from spirentapi import SpirentAPI, STCObject
from spirentapi.tclwrapper import TCLWrapperError
from spirentapi.utils import dotdict, value
from wait import wait_for_true

from .util import len_of_mask


def chassis(ip:str) -> STCObject:
    """get chassis object with specified ip

    Args:
        ip (str): chassis ip

    Returns:
        STCObject: STCObject of PhysicalChassis type
    """
    manager = STCObject('system1.PhysicalChassisManager')

    if len(manager.children) == 0:
        SpirentAPI.instance.stc_connect(ip)

    for chassis in manager.children:
        if chassis['HostName'] == ip:
            return chassis
    
    return None

def slots(ip:str) -> list[STCObject]:
    """get slot objects of chassis with the ip

    Args:
        ip (str): chassis ip

    Returns:
        list[STCObject]: STCObject list with PhysicalTestModule type
    """
    return list(filter(lambda x : x.type == 'physicaltestmodule', chassis(ip).children))

def groups(ip:str) -> list[STCObject]:
    """get all port group of chassis

    Args:
        ip (str): chassis ip

    Returns:
        list[STCObject]: STCObject list with PhysicalPortGroup type
    """
    groups = [ ]
    for slot in slots(ip):
        groups.extend(list(filter(lambda x : x.type == 'physicalportgroup', slot.children)))

    return groups

def ports(ip:str) -> list[STCObject]:
    """get all port of chassis

    Args:
        ip (str): chassis ip

    Returns:
        list[STCObject]: STCObject list with PhysicalPort type
    """
    ports = [ ]
    for group in groups(ip):

        ports.extend(list(filter(lambda x : x.type == 'physicalport', group.children)))
    
    return ports

def locations(ip:str) -> list[str]:
    """all locations under chassis

    Args:
        ip (str): chassis ip

    Returns:
        list[str]: list of locations
    """
    return [ port['Location'] for port in ports(ip) ]

def break_location(location:str) -> Tuple[str, int, int]:
    """break location to ip, slot, port

    Args:
        location (str): port location, c/s/p

    Returns:
        Tuple[str, int, int]: tuple of ip, slot, port
    """
    return re.compile('//(.+)/(.+)/(.+)').fullmatch(location).groups()

def port(location:str) -> STCObject:
    """get STCObject of PhysicalPort type by location

    Args:
        location (str): port location

    Returns:
        STCObject: STCObject of PhysicalPort type
    """
    ip, _, _ = break_location(location)
    port = list(filter(lambda x : x['Location'] == location, ports(ip)))
    assert len(port) == 1, 'should only one match: %s' % port

    return port[0]

def ifstacks(host:STCObject) -> list[STCObject]:
    """get interface object stacks

    Args:
        object (STCObject): object which has interface object children

    Returns:
        list[STCObject]: list of interface object, from bottom to up
    """
    stacks = [ ]

    # init loop
    topif = STCObject(host['TopLevelIf'])
    stacks.insert(0, topif)

    # start loop
    while topif['StackedOn'] != None:
        topif = STCObject(topif['StackedOn'])
        stacks.insert(0, topif)
    
    return stacks

def pdus(streamblock:STCObject) -> list[STCObject]:
    """streamblock pdus

    Args:
        streamblock (STCObject): streamblock

    Returns:
        list[STCObject]: pdus STCObject list, from bottom to top
    """
    return list(filter(lambda x : x.type.find(':') != -1, streamblock.children))

def ethii_pdus(streamblockObject:STCObject) -> List[STCObject]:
    """find ethii pdus

    Args:
        streamblockObject (STCObject): STCObject to find

    Returns:
        List[STCObject]: find ethii pdus under STCObject
    """
    return list(filter(lambda x : x.type == 'ethernet:ethernetii', pdus(streamblockObject)))

def ipv4_pdus(streamblockObject:STCObject) -> List[STCObject]:
    """find ipv4 pdus

    Args:
        streamblockObject (STCObject): STCObject to find

    Returns:
        List[STCObject]: find ipv4 pdus under STCObject
    """
    return list(filter(lambda x : x.type == 'ipv4:ipv4', pdus(streamblockObject)))

def ethii_ifs(hostObject:STCObject) -> List[STCObject]:
    """find ethii ifs

    Args:
        streamblockObject (STCObject): STCObject to find

    Returns:
        List[STCObject]: find ethii ifs under STCObject
    """
    return list(filter(lambda x : x.type == 'ethiiif', ifstacks(hostObject)))

def ipv4_ifs(hostObject:STCObject) -> List[STCObject]:
    """find ipv4 ifs

    Args:
        streamblockObject (STCObject): STCObject to find

    Returns:
        List[STCObject]: find ipv4 ifs under STCObject
    """
    return list(filter(lambda x : x.type == 'ipv4if', ifstacks(hostObject)))

def insert_vlan(streamObject:STCObject, vid:int) -> NoReturn:
    """insert port vid into streamblock

    Args:
        handle (str): streamblock handle to insert vlan
        vid (int): vid to insert
    """
    # find lowest ethernet::ethernetii
    ethiiObject = ethii_pdus(streamObject)[0]

    # find vlans under ethernet::ethernetii
    vlansObjects = list(filter(lambda x : x.type == 'vlans', ethiiObject.children))
    if len(vlansObjects) == 0: # if not found, create one
        vlansObject = SpirentAPI.instance.stc_create('vlans', under=ethiiObject.handle)
    else:
        vlansObject = vlansObjects[0]

    # find vlan under vlans
    vlanObjects = list(filter(lambda x : x.type == 'vlan', vlansObject.children))

    # insert vlan
    vlanObject = SpirentAPI.instance.stc_create('vlan', under=vlansObject.handle, id=vid)
        
    # re-create vlan object
    for vlanObject in vlanObjects:
            
        # create new vlan object based on old vlan object
        SpirentAPI.instance.stc_create(
            'vlan',
            under=vlansObject.handle,
            Name=vlanObject['Name'],
            type=vlanObject['type'],
            pri=vlanObject['pri'],
            cfi=vlanObject['cfi'],
            id=vlanObject['id'],
            Active=vlanObject['Active']
        )

            # delete old vlan object
        SpirentAPI.instance.stc_delete(vlanObject.handle)

class FillType(Enum):
    """Stream Payload FillType
    """
    constant = 'CONSTANT'
    incr = 'INCR'
    decr = 'DECR'
    prbs = 'PRBS'
    incr_word = 'INCRWORD'
    decr_word = 'DECRWORD'
    custom = 'CUSTOM'

class LengthMode(Enum):
    """Stream Frame Size
    """
    fixed = 'FIXED'
    incr = 'INCR'
    decr = 'DECR'
    random = 'RANDOM'
    auto = 'AUTO'
    imix = 'IMIX'


class StreamState(Enum):
    """RunningState of stream block
    """
    stopped = 'STOPPED'
    running = 'RUNNING'
    pending_start = 'PENDING_START'
    pending_stop = 'PENDING_STOP'


class IPCPEncap(Enum):
    """IPCP Encapsulation in PPPoE Client
    """
    ipv4 = 'IPV4'
    ipv6 = 'IPV6'
    ipv4v6 = 'IPV4V6'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class PPPoXAuthMode(Enum):
    """PPPoE Authentication Mode
    """
    none = 'NONE'
    auto = 'AUTO'
    chap_md5 = 'CHAP_MD5'
    pap = 'PAP'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class PPPoXState(Enum):
    """PPPoX State
    """
    none = 'NONE'
    idle = 'IDLE'
    connecting = 'CONNECTING'
    connected = 'CONNECTED'
    disconnecting = 'DISCONNECTING'
    terminating = 'TERMINATING'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class FilterMode(Enum):
    """igmp / mld filter mode
    """
    include = 'INCLUDE'
    exclude = 'EXCLUDE'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class IGMPVersion(Enum):
    """IGMP Version
    """
    igmp_v1 = 'IGMP_V1'
    igmp_v2 = 'IGMP_V2'
    igmp_v3 = 'IGMP_V3'
    mld_v1 = 'MLD_V1'
    mld_v2 = 'MLD_V2'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class IGMPState(Enum):
    """IGMP state
    """
    undefined = 'UNDEFINED'
    non_member = 'NON_MEMBER'
    joining = 'JOINING'
    member = 'MEMBER'
    leaving = 'LEAVING'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class DHCPOption(Enum):
    """DHCP Option Request List
    """
    subnet_mask = '1'
    router = '3'
    domain_name_servers = '6'
    domain_name = '15'
    static_routes = '33'
    netbios_name_servers = '44'
    netbios_node_type = '46'
    netbios_scope = '47'
    ipaddress_lease_time = '51'
    server_identifier = '54'
    renewal_time = '58'
    rebinding_time = '59'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class DHCPState(Enum):
    """dhcp state
    """
    idle = 'IDLE'
    request = 'REQUEST'
    release = 'RELEASE'
    renew = 'RENEW'
    rebind = 'REBIND'
    autorenew = 'AUTORENEW'
    groupreq = 'GROUPREQ'
    reboot = 'REBOOT'
    roam = 'ROAM'
    dnarequest = 'DNAREQUEST'
    bound = 'BOUND'

    def __str__(self) -> str:
        """str

        Returns:
            str: str value
        """
        return self.value


class DHCPServerState(Enum):
    """DHCP Server State
    """
    down = 'NONE'
    up = 'UP'


class OwnershipState(Enum):
    """Port Ownership state
    """

    # Port group is available for reservation
    AVAILABLE = 'OWNERSHIP_STATE_AVAILABLE'
    
    # Port group is currently reserved
    RESERVED = 'OWNERSHIP_STATE_RESERVED'

    # Current owner has disconnected from the port group but still has it reserved
    DISCONNECTED = 'OWNERSHIP_STATE_DISCONNECTED'


class PortMode(Enum):
    """DataPathMode of Physical Interface of Port
    """

    # normal mode
    normal = 'NORMAL'

    # loopback mode
    local_loopback = 'LOCAL_LOOPBACK'


class DeviceType(Enum):
    """Device type to create
    """
    host = 0

    dhcpv4_client = 1
    dhcpv4_server = 2

    igmp = 3

    pppox_client = 4
    pppox_server = 5


class StreamType(Enum):
    """stream type

    """
    raw = 0
    bound = 1


class PDU(Enum):
    """Protocol Data Unit

    Protocol Data Unit is used by streamblock to setup protocol stack
    """
    EthII = 'ethernet:ethernetii'
    IPv4 = 'ipv4:ipv4'
    IPv6 = 'ipv6:ipv6'
    TCP = 'tcp:tcp'
    UDP = 'udp:udp'


class INTF(Enum):
    """Interface Object

    Interface Object is used by HOST, EmulationDevice to setup protocol stack
    """
    aal5 = 'aal5if'
    dlc = 'dlcif'
    ethii = 'ethiiif'
    fc = 'fcif'
    gre = 'greif'
    ipv4 = 'ipv4if'
    ipv6 = 'ipv6if'
    itag = 'itagif'
    l2tpv2 = 'l2tpv2if'
    mpls = 'mplsif'
    PPP = 'pppif'
    pppoe = 'pppoeif'
    vlan = 'vlanif'
    wimax = 'wimaxif'


class Device:
    """Device

    presents Device under Virutal Spirent TestCenter Port
    """

    def __init__(self, port, **kwargs) -> NoReturn:
        """init

        Args:
            port (Port): associated port object
        """
        # save port object
        self._port = port
        
        # create device
        self._object = self._create_device(**kwargs)

        # some sth:: can't set name correctly, to fix this, use stc::config to set name
        if 'name' in kwargs.keys():
            self._object['Name'] = kwargs['name']

        # insert vlan if there is
        self._insert_vlan()

    @property
    def port(self):
        """associated Port object

        Returns:
            Port: associated Port object
        """
        return self._port
    
    @property
    def handle(self) -> str:
        """ handle of Device
        
        Returns:
            str: device handle
        """
        return self.object.handle

    @property
    def proto_handle(self) -> Union[str, NoReturn]:
        """protocol handle of Device

        Returns:
            str: protocol handle of Device
        """
        # get top level if
        toplevelif = STCObject(self.object['toplevelif'])
        # get top level if's usesif source
        return  toplevelif['usesif-Sources']

    @property
    def object(self) -> STCObject:
        """STCObject of Device

        Returns:
            STCObject: device handle object
        """
        assert self._object != None, '_object attribute doesn\'t exist'

        return self._object
    
    @property
    def name(self) -> str:
        """device name

        Returns:
            str: device name
        """
        return self.object.name
    
    @name.setter
    def name(self, value:str) -> NoReturn:
        """set device name

        Args:
            value (str): device name to set
        """
        self.object['name'] = value

    def _create_device(self, **kwargs) -> STCObject:
        """create traffic device

        Returns:
            STCObject: STCObject wrapped device handle
        """
        # create device
        dev_ret = self._device_config(mode='create', port_handle=self.port.handle, **kwargs)

        # return
        return STCObject(dev_ret.handle)

    def _device_config(self, **kwargs) -> dotdict:
        """short for sth_emulation_device_config
        """
        return SpirentAPI.instance.sth_emulation_device_config(**kwargs)

    def _insert_vlan(self) -> NoReturn:
        """insert vlan into protocol stack of device
        
        after calling _create_device, call this method to insert vlanif in the protocol stack of device
        """
        # if vid is None, no need to insert vlan
        if self.port.vid == None:
            return
        
        # find bottom ethiiif
        ethiiif = None
        for intf in ifstacks(self.object):
            if intf.type == INTF.ethii.value:
                ethiiif = intf
                break
        
        assert ethiiif != None, 'can\'t find ethiiif'
        
        # find if which is stacked on ethiiif
        intfs = [ ]
        for intf in ifstacks(self.object):
            if intf['StackedOn'] == ethiiif.handle:
                intfs.append(intf)

        # create vlanif and stackedon ethiiif
        vlanif = STCObject(SpirentAPI.instance.stc_create(INTF.vlan.value, under=self.handle, StackedOn=ethiiif.handle))

        # config intf in intfs re-stack on vlanif
        for intf in intfs:
            SpirentAPI.instance.stc_config(intf.handle, StackedOn=vlanif.handle)

    @property
    def stats(self) -> dotdict:
        """device stats

        Returns:
            dotdict: device stats
        """
        return { }
    
    def clear_stats(self) -> NoReturn:
        """clear stats
        """
        return

    def delete(self) -> NoReturn:
        """delete device
        """
        if self.object != None:

            self.port.remove_device(self)

            SpirentAPI.instance.stc_delete(self.handle)
            
            self._object = None
    
    @property
    def gateway(self) -> str:
        """ip gateway

        Returns:
            str: ip gateway
        """
        return ipv4_ifs(self.object)[0]['Gateway']

    @gateway.setter
    def gateway(self, address:str) -> str:
        """ip gateway address

        Args:
            addr (str): ip gateway address to set
        """
        ipv4_ifs(self.object)[0]['Gateway'] = address

    @property
    def gwmac(self) -> str:
        """gateway mac address

        Returns:
            str: gateway mac address
        """
        return ipv4_ifs(self.object)[0]['GatewayMac']

    @gwmac.setter
    def gwmac(self, address:str) -> str:
        """gateway mac address

        Args:
            addr (str): ip gateway mac address to set
        """
        ipv4_ifs(self.object)[0]['GatewayMac'] = address

    @property
    def ip(self) -> str:
        """ip address

        Returns:
            str: ip address
        """
        return ipv4_ifs(self.object)[0]['Address']

    @ip.setter
    def ip(self, address:str) -> NoReturn:
        """set ip address

        Args:
            address (str): ip address to set
        """
        ipv4_ifs(self.object)[0]['Address'] = address

    @property
    def mask(self) -> int:
        """subnet mask in ip layer

        Returns:
            int: subnet mask in int type
        """
        return int(ipv4_ifs(self.object)[0]['PrefixLength'])

    @mask.setter
    def mask(self, mask:Union[str, int]) -> NoReturn:
        """set prefix length in int or str

        for example:
            mask = 24
            mask = '255.255.255.0'

        Args:
            mask (Union[str, int]): subnet mask to set
        """
        if type(mask) == int:

            ipv4_ifs(self.object)[0]['PrefixLength'] = mask
        elif type(mask) == str:
            
            ipv4_ifs(self.object)[0]['PrefixLength'] = len_of_mask(mask)
        else:
            raise TypeError('unsupported type')

    @property
    def mac(self) -> str:
        """mac address

        Returns:
            str: mac address
        """
        return ethii_ifs(self.object)[0]['SourceMac']

    @mac.setter
    def mac(self, address:str) -> NoReturn:
        """set mac address

        Args:
            address (str): mac address to set
        """
        ethii_ifs(self.object)[0]['SourceMac'] = address


class DHCPv4Client(Device):
    """DHCP Client Device
    """

    def _create_device(self, **kwargs) -> STCObject:
        """create DHCPv4 client

        Returns:
            STCObject: STCObject wrapped device handle
        """
        # create device
        dhcp_ret = self._dhcp_config(mode='create', port_handle=self.port.handle)

        # set default encap
        if 'encap' not in kwargs.keys():
            kwargs['encap'] = 'ethernet_ii'
        
        # set default num_sessions
        if 'num_sessions' not in kwargs.keys():
            kwargs['num_sessions'] = 1

        dhcp_group_ret = self._dhcp_group_config(mode='create', handle=dhcp_ret.handles, **kwargs)

        # return
        return STCObject(dhcp_group_ret.handle)

    def _dhcp_config(self, **kwargs)  -> dotdict:
        """short for sth_emulation_dhcp_config
        """

        return SpirentAPI.instance.sth_emulation_dhcp_config(**kwargs)

    def _dhcp_group_config(self, **kwargs) -> dotdict:
        """short for sth_emulation_dhcp_group_config
        """

        return SpirentAPI.instance.sth_emulation_dhcp_group_config(**kwargs)

    def _dhcp_control(self, **kwargs) -> dotdict:
        """short for sth_emulation_dhcp_control
        """

        return SpirentAPI.instance.sth_emulation_dhcp_control(**kwargs)

    def _dhcp_stats(self, **kwargs) -> dotdict:
        """short for sth_emulation_dhcp_stats
        """

        return SpirentAPI.instance.sth_emulation_dhcp_stats(**kwargs)

    def abort(self, **kwargs) -> NoReturn:
        """Aborts DHCP client bindings and resets  the state of the DHCP client
        """
        self._dhcp_control(action='abort', handle=self.handle, **kwargs)

    def bind(self, **kwargs) -> NoReturn:
        """Starts the Discover/Request message exchange between the emulated requesting router(s) and the delegating router(s) that is necessary to establish client bindings
        """
        self._dhcp_control(action='bind', handle=self.handle, **kwargs)

    def inforeq(self, **kwargs) -> NoReturn:
        """Sends an Information-Request message to the server to request configuration parameters without assignment of any IP addresses to the client (for DHCPv6 only)
        """
        self._dhcp_control(action='inforeq', handle=self.handle, **kwargs)

    def release(self, **kwargs) -> NoReturn:
        """Terminates bindings for all currently bound subscribers
        """
        self._dhcp_control(action='release', handle=self.handle, **kwargs)

    def renew(self, **kwargs) -> NoReturn:
        """Renews the lease for all currently bound subscribers
        """
        self._dhcp_control(action='renew', handle=self.handle, **kwargs)

    def rebind(self, **kwargs) -> NoReturn:
        """Rebinds DHCP clients with the DHCP server
        """
        self._dhcp_control(action='rebind', handle=self.handle, **kwargs)

    @property
    def stats(self) -> dotdict:
        """DHCP Client Device Stats

        Returns:
            dotdict: use x.x to access stats information
        """
        ret =  self._dhcp_stats(mode='session', action='collect', handle=self.proto_handle)

        return ret['group'][self.proto_handle]

    def clear_stats(self) -> NoReturn:
        """clear stats
        """
        self._dhcp_stats(mode='session', action='clear', handle=self.proto_handle)

    @property
    def options(self) -> List[DHCPOption]:
        """Option Request List

        Returns:
            List[DHCPOption]: dhcp request option list
        """
        ret = [ ]
        for option in STCObject(self.proto_handle)['OptionList'].split(' '):
            ret.append(DHCPOption(option))
        
        return ret

    @options.setter
    def options(self, optionsList:List[DHCPOption]) -> NoReturn:
        """set options list

        Args:
            optionsList (List[DHCPOption]): DHCP Option Request List
        """
        STCObject(self.proto_handle)['OptionList'] =  optionsList

    @property
    def state(self) -> DHCPState:
        """dhcp state

        Returns:
            DHCPState: dhcp state
        """
        return DHCPState(STCObject(self.proto_handle)['BlockState'])


class DHCPv4Server(Device):
    """DHCP Server Device
    """

    def _create_device(self, **kwargs) -> STCObject:
        """create device

        Returns:
            STCObject: STCObject wrapped device handle
        """
        if 'ip_address' not in kwargs.keys():
            logger.warning('you should specifiy ip_address argument')

        if 'ipaddress_pool' not in kwargs.keys():
            raise RuntimeWarning('you must speicifiy ipaddress_pool argument, and in the same subnetwork as ip_addess')

        dhcp_server_ret = self._dhcp_server_config(mode='create', port_handle=self.port.handle, **kwargs)

        return STCObject(dhcp_server_ret.handle.dhcp_handle)

    def _dhcp_server_config(self, **kwargs) -> dotdict:
        """short for sth_emulation_dhcp_server_config
        """
        return SpirentAPI.instance.sth_emulation_dhcp_server_config(**kwargs)

    def _dhcp_server_control(self, **kwargs) -> dotdict:
        """short for sth_emulation_dhcp_server_control
        """

        return SpirentAPI.instance.sth_emulation_dhcp_server_control(**kwargs)

    def _dhcp_server_stats(self, **kwargs) -> dotdict:
        """short for sth_emulation_dhcp_server_stats
        """

        return SpirentAPI.instance.sth_emulation_dhcp_server_stats(**kwargs)

    def connect(self, **kwargs) -> NoReturn:
        """Connects the DHCP or DHCPv6/PD servers on the  specified ports or DHCP or DHCPv6/PD handles
        """
        self._dhcp_server_control(action='connect', dhcp_handle=self.handle, **kwargs)

    def renew(self, **kwargs) -> NoReturn:
        """Reconnects the DHCP or DHCPv6/PD servers on the specified ports or DHCP or DHCPv6/PD handles  respectively
        """
        self._dhcp_server_control(action='renew', dhcp_handle=self.handle, **kwargs)

    def reset(self, **kwargs) -> NoReturn:
        """Resets the DHCP or DHCPv6/PD servers on the specified  ports or DHCP or DHCPv6/PD handles respectively
        """
        self._dhcp_server_control(action='reset', dhcp_handle=self.handle, **kwargs)

    @property
    def stats(self) -> dotdict:
        """stats

        Returns:
            dotdict: stats accessible by x.x
        """
        ret =  self._dhcp_server_stats(action='COLLECT', dhcp_handle=self.handle)

        return ret['dhcp_handle'][self.handle]

    def clear_stats(self) -> NoReturn:
        """clear stats
        """
        self._dhcp_server_stats(action='CLEAR', dhcp_handle=self.handle)

    @property
    def state(self) -> DHCPServerState:
        """dhcp server state

        Returns:
            DHCPServerState: dhcp server state
        """
        return DHCPServerState(STCObject(self.proto_handle)['ServerState'])


class IGMPDevice(Device):
    """IGMP Device
    """

    def _create_device(self, **kwargs) -> STCObject:
        """create device
        """
        igmp_ret = self._igmp_config(mode='create', port_handle=self.port.handle, **kwargs)

        return STCObject(igmp_ret.handle)

    def _igmp_config(self, **kwargs) -> dotdict:
        """short for sth_emulation_igmp_config
        """
        return SpirentAPI.instance.sth_emulation_igmp_config(**kwargs)

    def _igmp_control(self, **kwarg) -> dotdict:
        """short for sth_emulation_igmp_control
        """
        return SpirentAPI.instance.sth_emulation_igmp_control(**kwarg)

    def _igmp_info(self, **kwargs) -> dotdict:
        """short for sth_emulation_igmp_info
        """
        return SpirentAPI.instance.sth_emulation_igmp_info(**kwargs)

    def restart(self, **kwargs) -> NoReturn:
        """Stops and then restarts the groups
        """
        self._igmp_control(mode='restart', handle=self.proto_handle, **kwargs)

    def join(self, **kwargs) -> NoReturn:
        """Joins all groups
        """
        self._igmp_control(mode='join', handle=self.proto_handle, **kwargs)

    def leave(self, **kwargs) -> NoReturn:
        """Leave all groups
        """
        self._igmp_control(mode='leave', handle=self.proto_handle, **kwargs)

    def leave_join(self, **kwargs) -> NoReturn:
        """Rejoins all groups
        """
        self._igmp_control(mode='leave_join', handle=self.proto_handle, **kwargs)

    @property
    def stats(self) -> dotdict:
        """stats

        Returns:
            dotdict: stats accessible by x.x
        """
        ret = self._igmp_info(mode='stats', handle=self.proto_handle)
  
        return ret['session'][self.proto_handle]
    
    def clear_stats(self) -> NoReturn:
        """clear stats
        """
        self._igmp_info(mode='clear_stats', handle=self.proto_handle)

    @property
    def state(self) -> IGMPState:
        """igmp state

        Returns:
            IGMPState: igmp state
        """

        return IGMPState(STCObject(self.proto_handle)['BlockState'])

    @property
    def version(self) -> IGMPVersion:
        """IGMP Version
        
        Returns:
            IGMPVersion: IGMP Version
        """
        return IGMPVersion(STCObject(self.proto_handle)['Version'])
    
    @version.setter
    def version(self, ver:IGMPVersion) -> NoReturn:
        """set igmp version

        Args:
            ver (IGMPVersion): IGMP Version
        """
        STCObject(self.proto_handle)['Version'] = ver.value

    def _memberships(self) -> List[STCObject]:
        """get memberships objects

        Returns:
            List[STCObject]: memberships objects
        """

        if self.version.value.startswith('IGMP'):
            memberships = list(filter(lambda x : x.type == 'igmpgroupmembership', STCObject(self.proto_handle).children))

        elif self.version.value.startswith('MLD'):
            
            memberships = list(filter(lambda x : x.type == 'mldgroupmembership', STCObject(self.proto_handle).children))
        
        else:
            raise ValueError('unknown version: %s' % self.version)
        
        return memberships

    @property
    def filter_mode(self) -> Union[FilterMode, None]:
        """filter mode

        Returns:
            FilterMode: include or exclude mode, or None if no group assosiated
        """
        memberships = self._memberships()

        if len(memberships) == 0:
                
            return None
        
        elif len(memberships) == 1:

            return FilterMode(memberships[0]['FilterMode'])
        
        else:
            
            raise ValueError('too many memberships')
 
    @filter_mode.setter
    def filter_mode(self, mode:FilterMode) -> NoReturn:
        """set filter mode

        Args:
            mode (FilterMode): filter mode to set
        """
        memberships = self._memberships()

        if len(memberships) == 0:
                
            raise ValueError('can\'t find membership to set filter mode')
        
        elif len(memberships) == 1:

            memberships[0]['FilterMode'] = mode.value
        
        else:
            
            raise ValueError('too many memberships') 


class PPPoXCommonProps:

    @property
    def state(self) -> PPPoXState:
        """PPPoX server state

        Returns:
           PPPoXState : PPPoX server state
        """
        return PPPoXState(STCObject(self.proto_handle)['BlockState'])

    @property
    def auth(self) -> PPPoXAuthMode:
        """pppox authentication mode

        Returns:
            PPPoXAuthMode: pppox authentication mode
        """
        return PPPoXAuthMode(STCObject(self.proto_handle)['Authentication'])

    @auth.setter
    def auth(self, auth_mode:PPPoXAuthMode) -> NoReturn:
        """set pppox authentication mode

        Args:
            auth_mode (PPPoXAuthMode): pppox authentication mode to set
        """
        STCObject(self.proto_handle)['Authentication'] = auth_mode.value

    @property
    def username(self) -> str:
        """username used to auth in pppoe

        Returns:
            str: username
        """
        return STCObject(self.proto_handle)['Username']
    
    @username.setter
    def username(self, username:str) -> NoReturn:
        """set username

        Args:
            username (str): username to set
        """
        STCObject(self.proto_handle)['Username'] = username

    @property
    def password(self) -> str:
        """password used to auth in pppoe

        Returns:
            str: password
        """
        return STCObject(self.proto_handle)['Password']
    
    @password.setter
    def password(self, password:str) -> NoReturn:
        """set password

        Args:
            password (str): password to set
        """
        STCObject(self.proto_handle)['Password'] = password

    @property
    def service_name(self) -> Union[str, None]:
        """service name used in pppoe

        Returns:
            str: service name, or None if not specified
        """
        return STCObject(self.proto_handle)['ServiceName']
    
    @service_name.setter
    def service_name(self, name:str) -> NoReturn:
        """set service name

        Args:
            name (str): service name to set
        """
        STCObject(self.proto_handle)['ServiceName'] = name

    @property
    def chap_include_id(self) -> bool:
        """chap include id

        Returns:
            bool: whether to include chap id
        """
        return True if STCObject(self.proto_handle)['IncludeTxChapId'] == 'true' else False

    @chap_include_id.setter
    def chap_include_id(self, bflag:bool) -> NoReturn:
        """set chap include id

        Args:
            bflag (bool): set if chap include id
        """
        STCObject(self.proto_handle)['IncludeTxChapId'] = 'true' if bflag else 'false'

    @property
    def max_payload_tag(self) -> int:
        """max payload tag in bytes

        Returns:
            int: max payload tag
        """
        return int(STCObject(self.proto_handle)['MaxPayloadBytes'])
    
    @max_payload_tag.setter
    def max_payload_tag(self, value:int) -> NoReturn:
        """set max payload tag in bytes

        Args:
            value (int): max payload tag
        """
        STCObject(self.proto_handle)['MaxPayloadBytes'] = value

    @property
    def is_server(self) -> bool:
        """is server

        creating server and client under same port *may* convert the former created pppox to the other type

        you can use this property to check

        Returns:
            bool: True is server, False is client
        """
        return True if STCObject(self.proto_handle)['IsServer'] == 'true' else False
        

class PPPoXClient(Device, PPPoXCommonProps):
    """PPPoX Client Device
    """
    def _create_device(self, **kwargs) -> STCObject:
        
        pppox_ret = self._pppox_config(mode='create', port_handle=self.port.handle, **kwargs)

        return STCObject(pppox_ret.handle)

    def _pppox_config(self, **kwargs) -> dotdict:

        return SpirentAPI.instance.sth_pppox_config(**kwargs)

    def _pppox_control(self, **kwargs) -> dotdict:

        return SpirentAPI.instance.sth_pppox_control(**kwargs)

    def _pppox_stats(self, **kwargs) -> dotdict:

        return SpirentAPI.instance.sth_pppox_stats(**kwargs)

    def connect(self, **kwargs) -> NoReturn:
        """Establishes all PPPoX sessions
        """
        self._pppox_control(action='connect', handle=self.handle)

    def disconnect(self, **kwargs) -> NoReturn:
        """Disconnects all established PPPoX sessions
        """
        self._pppox_control(action='disconnect', handle=self.handle)

    def retry(self, **kwargs) -> NoReturn:
        """Attempts to connect failed PPPoX sessions
        """
        self._pppox_control(action='retry', handle=self.handle)

    def reset(self, **kwargs) -> NoReturn:
        """Terminates the port
        """
        self._pppox_control(action='reset', handle=self.handle)

    def pause(self, **kwargs) -> NoReturn:
        """Pause all PPPoX sessions that are connecting or disconnecting
        """
        self._pppox_control(action='pause', handle=self.handle)

    def resume(self, **kwargs) -> NoReturn:
        """Resume PPPoX sessions that were paused
        """
        self._pppox_control(action='resume', handle=self.handle)

    def clear(self, **kwargs)  -> NoReturn:
        """Clears the PPPoX statistics
        """
        self._pppox_control(action='clear', handle=self.handle)

    def abort(self, **kwargs)  -> NoReturn:
        """ Aborts all PPPoX sessions and resets the PPP emulation engine
        """
        self._pppox_control(action='abort', handle=self.handle)

    @property
    def stats(self) -> dotdict:
        """stats

        Returns:
            dotdict: stats accessible by x.x
        """
        ret = self._pppox_stats(mode='aggregate', handle=self.handle)

        return ret.aggregate

    def clear_stats(self) -> NoReturn:
        """clear stats
        """
        self.clear()

    @property
    def ipcp_encap(self) -> IPCPEncap:
        """get ipcp encap

        Returns:
            IPCPEncap: ipcap encapsulation
        """
        return IPCPEncap(STCObject(self.proto_handle)['IpcpEncap'])

    @ipcp_encap.setter
    def ipcp_encap(self, encap:IPCPEncap) -> NoReturn:
        """set ipcp encap

        Args:
            encap (IPCPEncap): ipcp encap to set
        """
        STCObject(self.proto_handle)['IpcpEncap'] = encap.value


class PPPoXServer(Device, PPPoXCommonProps):
    """PPPoX Server
    """

    def _create_device(self, **kwargs) -> STCObject:
        """create device
        """
        pppox_server_ret = self._pppox_server_config(mode='create', port_handle=self.port.handle, **kwargs)

        return STCObject(pppox_server_ret.handle)

    def _pppox_server_config(self, **kwargs) -> dotdict:

        return SpirentAPI.instance.sth_pppox_server_config(**kwargs)

    def _pppox_server_control(self, **kwargs) -> dotdict:

        return SpirentAPI.instance.sth_pppox_server_control(**kwargs)

    def _pppox_server_stats(self, **kwargs) -> dotdict:

        return SpirentAPI.instance.sth_pppox_server_stats(**kwargs)

    def connect(self, **kwargs) -> NoReturn:
        """Brings up the configured PPPoX servers
        """
        self._pppox_server_control(action='connect', handle=self.handle, **kwargs)

    def disconnect(self, **kwargs) -> NoReturn:
        """Tears down connected PPPoX servers
        """

        self._pppox_server_control(action='disconnect', handle=self.handle, **kwargs)
    
    def retry(self, **kwargs) -> NoReturn:
        """Attempts to connect PPPoX servers that have previously failed to establish
        """
        self._pppox_server_control(action='retry', handle=self.handle, **kwargs)
    
    def pause(self, **kwargs) -> NoReturn:
        """Pauses the PPPoX servers
        """
        self._pppox_server_control(action='pause', handle=self.handle, **kwargs)
    
    def resume(self, **kwargs) -> NoReturn:
        """Resumes the PPPoX servers
        """
        self._pppox_server_control(action='resume', handle=self.handle, **kwargs)

    def reset(self, **kwargs) -> NoReturn:
        """Aborts PPPoX sessions and resets the PPP
        """
        self._pppox_server_control(action='reset', handle=self.handle, **kwargs)

    def clear(self, **kwargs) -> NoReturn:
        """Clears the status and statistics of the PPP sessions
        """
        self._pppox_server_control(action='clear', handle=self.handle, **kwargs)

    def abort(self, **kwargs) -> NoReturn:
        """Aborts PPPoX sessions and resets the PPP emulation engine
        """
        self._pppox_server_control(action='abort', handle=self.handle, **kwargs)

    @property
    def stats(self) -> dotdict:
        """stats

        Returns:
            dotdict: dotdict accessible by x.x
        """
        ret = self._pppox_server_stats(mode='aggregate', handle=self.handle)

        return ret.aggregate

    def clear_stats(self):
        """clear stats
        """
        self.clear()

    @property
    def ac_name(self) -> str:
        """ac name

        Returns:
            str: ac name
        """
        return STCObject(self.proto_handle)['AcName']
    
    @ac_name.setter
    def ac_name(self, name:str) -> NoReturn:
        """set ac name

        Args:
            name (str): ac name to set
        """
        STCObject(self.proto_handle)['AcName'] = name


class StreamBlock(ABC):
    """StreamBlock

    base class for RawStreamBlock and BoundStreamBlock
    """

    def __init__(self, **kwargs) -> NoReturn:
        """init
        """
        self._object = self._create(**kwargs)

    @abstractmethod
    def _create(self, **kwargs) -> STCObject:
        """create streamblock
        """
        pass

    @property
    def object(self) ->STCObject:
        """STCObject

        Returns:
            STCObject: STCObject
        """
        return self._object

    @property
    def handle(self) -> str:
        """handle

        Returns:
            str: STCObject handle
        """
        return self.object.handle

    def delete(self) -> NoReturn:
        """delete streamblock
        """
        if self.handle != None:
            self.object.delete()

    def _traffic_config(self, **kwargs) -> dotdict:
        """short for sth::traffic_config

        Returns:
            dotdict: dotdict accessible by dot way
        """

        return SpirentAPI.instance.sth_traffic_config(**kwargs)

    def _traffic_control(self, **kwargs) -> dotdict:
        """short for sth::traffic_control

        Args:
            action (str): action to take， run、stop、reset、destroy、clear_stats、poll

        Returns:
            dotdict: dotdict accessible by dot way
        """

        return SpirentAPI.instance.sth_traffic_control(**kwargs)

    def _traffic_stats(self, **kwargs) -> dotdict:
        """short for sth::traffic_stats

        Returns:
            dotdict: dotdict accessible by dot way
        """

        return SpirentAPI.instance.sth_traffic_stats(**kwargs)

    @property
    def is_running(self) -> bool:
        """check the streamblock is running

        Returns:
            bool: True, running; False, stopped
        """
        state = SpirentAPI.instance.stc_get(self.handle, ['RunningState'])

        if state == 'RUNNING':

            return True
        elif state == 'STOPPED':
            
            return False
        else:
            raise RuntimeWarning('unknown running state：%s' % state)

    @property
    def speed(self) -> int:
        """speed in bps(bit per second)

        Return:
            int: speed in bps
        """
        return self.bpsload

    @speed.setter
    def speed(self, speed) -> NoReturn:
        """set speed

        Args:
            speed (str): speed to set, such as 100bps, 100kbps, 100mbps, 10pps, 10% and so on
        """
        speed_exp = re.compile('(\d+)\s*((b|kb|mb|p)ps+|%)')
        
        match = speed_exp.match(speed.strip().lower())
        if match == None:
            raise ValueError('support following speed format, case-insensitive: 100bps, 100kbps, 100mbps, 10pps, 10%')

        speed_num, speed_format, _ = match.groups()

        config = dotdict()
        config.mode = 'modify'
        config.stream_id = self.handle

        if speed_format == 'bps':
        
            config.rate_bps = speed_num
        
        elif speed_format == 'kbps':
        
            config.rate_kbps = speed_num
        
        elif speed_format == 'mbps':
        
            config.rate_mbps = speed_num
        
        elif speed_format == '%':
        
            config.rate_percent = speed_num
        
        elif speed_format == 'pps':
        
            config.rate_pps = speed_num
        else:
            raise ValueError('unknown speed format:%s' % speed_format) 

        self._traffic_config(**config)

    @property
    def length_mode(self) -> LengthMode:
        """length mode

        Returns:
            LengthMode: length mode: auto, decr, fixed, imix, incr, or random
        """
        return LengthMode(self.object['FrameLengthMode'])

    @length_mode.setter
    def length_mode(self, mode:LengthMode) -> NoReturn:
        """length mode

        Args:
            mode (LengthMode): auto, decr, fixed, imix, incr, or random
        """
        self.object['FrameLengthMode'] = mode.value

    @property
    def fixed_length(self) -> int:
        """fixed frame length in fixed length mode

        Returns:
            int: fixed frame length
        """
        return int(self.object['FixedFrameLength'])
    
    @fixed_length.setter
    def fixed_length(self, len:int) -> NoReturn:
        """set fixed frame length in fixed length mode

        Args:
            len (int): fixed frame length
        """
        self.object['FixedFrameLength'] = len

    @property
    def min_length(self) -> int:
        """min frame length in incr/decr/random length mode

        Returns:
            int: min frame length
        """
        return int(self.object['MinFrameLength'])
    
    @min_length.setter
    def min_length(self, len:int) -> NoReturn:
        """set min frame length in incr/decr/random length mode

        Args:
            len (int): min frame length
        """
        self.object['MinFrameLength'] = len

    @property
    def max_length(self) -> int:
        """max frame length in incr/decr/random length mode

        Returns:
            int: max frame length
        """
        return int(self.object['MaxFrameLength'])
    
    @max_length.setter
    def max_length(self, len:int) -> NoReturn:
        """set max frame length in incr/decr/random length mode

        Args:
            len (int): max frame length
        """
        self.object['MaxFrameLength'] = len

    @property
    def length_step(self) -> int:
        """frame length step in incr/decr/random length mode

        Returns:
            int: length step
        """
        return int(self.object['StepFrameLength'])
    
    @length_step.setter
    def length_step(self, step:int) -> NoReturn:
        """set frame length step in incr/decr/random length mode

        Args:
            len (int): length step, need be power of 2
        """
        self.object['StepFrameLength'] = step

    @property
    def fill_type(self) -> FillType:
        """payload fill type

        Returns:
            FillType: payload fill type
        """
        return FillType(self.object['FillType'])
    
    @fill_type.setter
    def fill_type(self, fillType:FillType) -> NoReturn:
        """fill type

        Args:
            type (FillType): fill type to set
        """
        self.object['FillType'] = fillType.value
    
    @property
    def fill_const(self) -> int:
        """fill constant

        Returns:
            int: fill constant
        """
        return int(self.object['ConstantFillPattern'])

    @fill_const.setter
    def fill_const(self, pattern:int) -> NoReturn:
        """fill constant

        Args:
            pattern (int): fill constant in hex
        """
        self.object['ConstantFillPattern'] = pattern

    def start(self, **kwargs) -> NoReturn:
        """starts traffic

        Args:
            duration (int, optional): duration to run, in second
        """
        if 'enable_arp' not in kwargs.keys():
            kwargs['enable_arp'] = '1'
        
        self._traffic_control(action='run', stream_handle=self.handle, **kwargs)

    def stop(self, **kwargs) -> NoReturn:
        """stops traffic
        """
        if 'db_file' not in kwargs.keys():
            kwargs['db_file'] = '0'

        self._traffic_control(action='stop', stream_handle=self.handle, **kwargs)

    def clear_stats(self) -> NoReturn:
        """clear stats
        """
        self._traffic_control(action='clear_stats', stream_handle=self.handle)

    @property
    def stats(self) -> dotdict:
        """stats

        Args:
            stats (str): stats information

        Returns:
            dotdict: dotdict accessible by dot way
        """
        ret = self._traffic_stats(mode='streams', streams=self.handle)

        return ret[self.handle]

    def __str__(self) -> str:
        """

        Returns:
            str: stream object handle
        """
        return self.handle

    @property
    def name(self) -> str:
        """streamblock name

        Returns:
            str: streamblock name
        """
        return self.object['Name']
    
    @name.setter
    def name(self, value:str) -> NoReturn:
        """set streamblock name

        Args:
            value (str): set streamblock name
        """
        self.object['Name'] = value
        
    @property
    def state(self) -> StreamState:
        """streamblock state

        Returns:
            StreamState: streamblock state
        """
        return StreamState(self.object['RunningState'])


class RawStreamBlock(StreamBlock):
    """Raw StreamBlock
    """

    def _create(self, port, **kwargs) -> STCObject:
        """create raw streamblock
        
        Args:
            port (Port): port under which to create raw streamblock


        Returns:
            STCObject: raw streamblock STCObject
        """

        ret = self._traffic_config(mode='create', port_handle=port.handle, **kwargs)

        streamObject = STCObject(ret.stream_id)

        # insert vlan
        insert_vlan(streamObject, port.vid)

        return streamObject


class BoundStreamBlock(StreamBlock):
    """Bound StreamBlock
    """

    def _create(self, src_handle:str, dst_handle:str, **kwargs) -> STCObject:
        """create bound streamblock

        Args:
            src_handle (str): source device handle str which streamblock to create with 
            dst_handle (str): destination device handle str which streamblock to create with 

        Returns:
            STCObject: bound streamblock STCObject
        """
        try:
            port_handle = SpirentAPI.instance.stc_get(src_handle, ['AffiliatedPort'])
        except TCLWrapperError as error:
            host_handle = SpirentAPI.instance.stc_get(src_handle, ['parent'])
            port_handle = SpirentAPI.instance.stc_get(host_handle, ['parent'])

        ret = self._traffic_config(mode='create', port_handle=port_handle, emulation_src_handle=src_handle, emulation_dst_handle=dst_handle, l2_encap='ethernet_ii_vlan', l3_protocol='ipv4', **kwargs)

        streamObject =  STCObject(ret.stream_id)

        streamObject['EnableResolveDestMacAddress'] = False

        return streamObject

    # TODO:
    def _modify_dst_mac(self, streamObject:STCObject, dst_mac:str) -> NoReturn:
        """modify destination mac address

        notes:
            because of traffic_config can't setup destination mac address correctly, so need modify the destination mac address after creating the streamblock

        Args:
            streamObject (STCObject): streamblock to modify
            dst_mac (str): destination mac address
        """
        ethiiif = ethii_pdus(streamObject)[0]

        ethiiif['dstMac'] = dst_mac


class Port:
    """Port

    present Virtual Spirent TestCenter port
    """

    def __init__(self, location:str, vid:Optional[Union[int, None]]=None) -> None:
        """init port

        Args:
            location (str): port location
            vid (str, optional): vid used for switch port. Defaults to None.
        """
        # save location
        self._location = location.strip()

        # save vid
        if vid != None:
            assert type(vid) == int, 'vid should be int type'
        self._vid = vid

        # create logical port without default host

        # find port object, if non-existence, create one
        ports = list(filter(lambda x : x.type == 'port' and x['Location'] == location, STCObject('project1').children))

        if len(ports) == 0:
            handle = SpirentAPI.instance.stc_create('port', under='project1', UseDefaultHost=False, Location=self.location)
            self._object = STCObject(handle)
        else:
            assert len(ports) == 1, 'unexpected port number, should be only one port'
            self._object = ports[0]
        
        # reserve
        ip, _, _ = break_location(self.location)

        # connect chassis
        if chassis(ip)['IsConnected'] == False:
            SpirentAPI.instance.stc_connect(ip)
        
        # reserve port
        SpirentAPI.instance.stc_perform('ReservePort', Location=self.location, RevokeOwner='True')

        # logical to physical port mapping
        SpirentAPI.instance.stc_perform('setupPortMappings')

        # create device list
        self._devices = [ ]

        # create streamlbock list
        self._streamblocks = [ ]

    @property
    def handle(self) -> str:
        """port handle name

        Returns:
            str: port handle name
        """
        return self.object.handle

    @property
    def object(self) -> STCObject:
        """port STCObject instance

        Returns:
            STCObject: port STCObject instance
        """
        return self._object

    @property
    def mode(self) -> PortMode:
        """Data Path Mode

        Returns:
            DataPathMode: NORMAL or LOCAL_LOOPBACK
        """
        phy = STCObject(self._port['ActivePhy'])
        return PortMode(phy['DataPathMode'])

    @mode.setter
    def mode(self, mode:PortMode) -> NoReturn:
        """set Data Path Mode

        Args:
            mode (DataPathMode): normal or local_loopback
        """
        phy = STCObject(self._object['ActivePhy'])
        phy['DataPathMode'] = mode.value

    @property
    def location(self) -> str:
        """Port Location

        Returns:
            str : Port Location
        """
        return self._location

    @property
    def vid(self) -> int:
        """Port VID

        Returns:
            int: Port VID
        """
        return self._vid

    @property
    def state(self) -> bool:
        """reserved state

        Returns:
            bool: True, reserved by ownself, False, not
        """
        return port(self.location).parent['ReservedByUser']

    @property
    def ownership(self) -> OwnershipState:
        """port ownership state

        Returns:
            OwnershipState: port ownership state
        """
        return OwnershipState(port(self.location).parent['OwnershipState'])

    @property
    def owner_user(self) -> Union[str, None]:
        """port owner userId

        Returns:
            str: owner userId, if not reserved, return None
        """
        return port(self.location).parent['OwnerUserId']

    @property
    def owner_host(self) -> Union[str, None]:
        """port owner hostname

        Returns:
            str: owner hostname, if not reserved, return None
        """
        return port(self.location).parent['OwnerHostname']

    def start_capture(self) -> NoReturn:
        """start capturing
        """
        capture = list(filter(lambda x: x.type == 'capture', self._object.children))[0]
        SpirentAPI.instance.stc_perform('CaptureStart', captureProxyId = capture)

    def stop_capture(self) -> NoReturn:
        """stop capturing
        """
        capture = list(filter(lambda x: x.type == 'capture', self._object.children))[0]
        SpirentAPI.instance.stc_perform('CaptureStop', captureProxyId = capture)

    def save_capture(self, filename:str) -> NoReturn:
        """save capture file

        Args:
            filename (str): file path to save pcap file
        """
        # must replace \ with /, test center only works with /
        filename = os.path.abspath(filename).replace('\\', '/')

        capture = list(filter(lambda x: x.type == 'capture', self._object.children))[0]

        SpirentAPI.instance.stc_perform('CaptureDataSave', captureProxyId = capture, FileName=filename)

    @property
    def devices(self) -> list[Device]:
        """devices under port

        Returns:
            list[Device]: devices under port
        """
        return self._devices

    def create_device(self, type:DeviceType, **kwargs) -> Union[Device, DHCPv4Client, DHCPv4Server, IGMPDevice, PPPoXClient, PPPoXServer]:
        """create device under ports

        Returns:
            device: Device object
        """
        dev = None

        if type == DeviceType.host:
            
            dev = Device(self, **kwargs)

        elif type == DeviceType.dhcpv4_client:
            
            dev = DHCPv4Client(self, **kwargs)

        elif type == DeviceType.dhcpv4_server:

            dev = DHCPv4Server(self, **kwargs)
        
        elif type == DeviceType.igmp:

            dev = IGMPDevice(self, **kwargs)
        
        elif type == DeviceType.pppox_client:

            dev = PPPoXClient(self, **kwargs)
        
        elif type == DeviceType.pppox_server:

            dev = PPPoXServer(self, **kwargs)

        else:
            raise ValueError('unsupported device type: %s' % type.value)

        if dev == None:
            raise RuntimeError('create device failed')

        self._devices.append(dev)

        return dev

    def remove_device(self, dev:Device) -> NoReturn:
        """remove device under ports

        Args:
            device (Device): device to remove
        """
        self._devices.remove(dev)

    def __str__(self) -> str:
        """
        Returns:
            str: port handle
        """
        return self.handle

    @property
    def streamblocks(self) -> List[StreamBlock]:
        """get streamblock list in port

        Returns:
            List[StreamBlock]: streamblocks under port
        """
        return self._streamblocks

    def create_streamblock(self, type, **kwargs) -> StreamBlock:
        """create streamblock

        Args:
            type (StreamType): stream type
            src_handle (str, optional): source device handle str which streamblock to create with 
            dst_handle (str, optional): destination device handle str which streamblock to create with 

        Returns:
            StreamBlock: StreamBlock object
        """
        streamblock = None
        if type == StreamType.bound:

            streamblock = BoundStreamBlock(**kwargs)
        
        elif type == StreamType.raw:
            
            streamblock = RawStreamBlock(port=self, **kwargs)
        
        else:
            raise ValueError('unknown stream type: %s' % type)

        self._streamblocks.append(streamblock)

        return streamblock

    def remove_streamblock(self, streamblock:StreamBlock) -> NoReturn:
        """delete streamblock

        Args:
            streamblock (StreamBlock): streamblock to delete
        """
        self._streamblocks.remove(streamblock)
        streamblock.delete()


class MCGroup:
    """Multicast Group
    """

    def __init__(self, obj:STCObject) -> NoReturn:
        """init
        """
        
        self._object = obj

        self._devices = [ ]
    
    @property
    def handle(self) -> str:
        """handle of MCGroup

        Returns:
            str: handle of MCGroup
        """
        return self.object.handle

    @property
    def object(self) -> STCObject:
        """STCObject

        Returns:
            STCObject: STCObject instance
        """
        return self._object

    @property
    def devices(self) -> List[IGMPDevice]:
        """IGMP Devices in group

        Returns:
            List[IGMPDevice]: IGMPDevice in the group
        """
        return self._devices

    def _igmp_group_config(self, **kwargs) -> dotdict:
        """short for sth_emulation_igmp_group_config

        Returns:
            dotdict: dotdict accessible by dot
        """
        return SpirentAPI.instance.sth_emulation_igmp_group_config(**kwargs)

    def add(self, dev:IGMPDevice) -> NoReturn:
        """add IGMP device to multicast group

        Args:
            dev (IGMPDevice): IGMP device to add
        """
        self._igmp_group_config(mode='create', group_pool_handle=self.handle, session_handle=dev.handle)

    def remove(self, dev:IGMPDevice) -> NoReturn:
        """remove IGMP device from multicast group

        Args:
            dev (IGMPDevice): IGMP device to remove
        """
        self._devices.remove(dev)
        
        # filter out membership belongs to this group
        memberships = list(filter(lambda x : x.type == 'igmpgroupmembership' and x['subscribedgroups-Targets'] == self.handle, dev.object.children))

        # delete membership
        for membership in memberships:
            self._igmp_group_config(mode='delete', handle=membership.handle)

    def _delete(self) -> NoReturn:
        """delete Multicast Group
        """
        if self.handle != None:
            self.object.delete()

    def __str__(self) -> str:
        """
        Returns:
            str: mcgroup handle
        """
        return self.handle

    @property
    def name(self) -> str:
        """streamblock name

        Returns:
            str: streamblock name
        """
        return self.object['Name']
    
    @name.setter
    def name(self, value:str) -> NoReturn:
        """set streamblock name

        Args:
            value (str): set streamblock name
        """
        self.object['Name'] = value
        
    @property
    def ip(self) -> str:
        """multicast group ip

        Returns:
            str: multicast group ip
        """
        return self.object['ipv4networkblock.StartIpList']

    @ip.setter
    def ip(self, ip:str) -> NoReturn:
        """set multicast group ip

        Args:
            ip (str): multicast group ip
        """
        self.object['ipv4networkblock.StartIpList'] = ip


class Chassis:
    """Chassis

    present Virutal Spirent TestCenter

    Virutal Spirent TestCenter is the Combination of SpirentTestCenter and Switch

    You can configure a Virutal Spirent TestCenter Ports
    If you do that, when you use these virtual ports, it will automatically insert a vlan with specified vid upon the ethernetif for you
    For exmaple:
    slot,   port,   vid
    1,      1,      100
    1,      1,      200
    1,      2,      300
    1,      2,      400 
    """

    def __init__(self, ip:str, ports:list[dict]=[ ]) -> None:
        """init chassis

        Args:
            ip(str): chassis ip
            ports(list[dict]): port list of dict type which contains slot, port, vid attributes.
        """
        self._ip = ip.strip()

        self._ports = [ ]
        for port in ports:
            self._ports.append(Port(port['location'], port['vid']))
        
        self._mcgroups = [ ]

        if self.state == False:
            self.connect()
            wait_for_true(lambda : self.state)

    @property
    def ip(self) -> NoReturn:
        """chassis ip
        """
        return self._ip
    
    @property
    def state(self) -> bool:
        """connection state

        Returns:
            bool: True, connected, False, disconnected
        """
        return value(chassis(self.ip)['IsConnected'])

    @property
    def serial(self) -> str:
        """chassis serial number

        Returns:
            str: serial number
        """
        return chassis(self.ip)['SerialNum']

    @property
    def ports(self) -> list[Port]:
        """port list under chassis

        accessing the property will make connect chassis 

        Returns:
            list(Port): port list under chassis
        """

        return self._ports

    @property
    def mcgroups(self) -> list[MCGroup]:
        """multicast groups

        Returns:
            list[MCGroup]: multicast groups
        """
        return self._mcgroups

    def _multicast_group_config(self, **kwargs) -> dotdict:
        """short for sth_emulation_multicast_group_config

        Returns:
            dotdict: dotdict accessible by dot
        """
        return SpirentAPI.instance.sth_emulation_multicast_group_config(**kwargs)

    def create_mcgroup(self, name:Optional[str]=None, ip:Optional[str]='225.0.0.1') -> MCGroup:
        """add multicast group

        Args:
            name (optional, str): multicast group name to add
            ip (optional, str): multicast group address
        
        Returns:
            MCGroup: multicast group
        """
        ret = self._multicast_group_config(mode='create', ip_addr_start=ip)
        obj = STCObject(ret.handle)

        if name != None:
            obj['Name'] = name

        mcgroup = MCGroup(obj)
        self._mcgroups.append(mcgroup)
        return mcgroup

    def remove_mcgroup(self, mcgroup:MCGroup) -> NoReturn:
        """remove multicast group

        Args:
            group (MCGroup): multicast group to remove
        """
        self._mcgroups.remove(mcgroup)
        mcgroup._delete()

    def connect(self) -> NoReturn:
        """connect chassis
        """
        SpirentAPI.instance.stc_connect(self.ip)

    def disconnect(self) -> NoReturn:
        """disconnect chassis
        """
        SpirentAPI.instance.stc_disconnect(self.ip)

    def apply(self) -> NoReturn:
        """apply
        """
        SpirentAPI.instance.stc_apply()

    def save(self, filename:str) -> NoReturn:
        """save configuration

        Args:
            filename (str): filename to save
        """
        SpirentAPI.instance.sth_save_xml(filename=filename)