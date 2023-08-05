from vstc import Chassis, DHCPServerState, DHCPState, FilterMode, IGMPState, IGMPVersion, IPCPEncap, PPPoXAuthMode, PPPoXState, PortMode, DeviceType
from wait import wait_for_true

def test_host():
    
    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/6', 'vid': 100}])

    port = chassis.ports[0]

    dev = port.create_device(DeviceType.host)

    dev.ip = '192.168.1.1'
    dev.mac = '00:10:94:00:01:01'
    dev.gateway = '192.168.1.254'
    dev.gwmac = '00:10:94:00:11:11'

    assert dev.ip == '192.168.1.1'
    assert dev.mac == '00:10:94:00:01:01'
    assert dev.gateway == '192.168.1.254'
    assert dev.gwmac == '00:10:94:00:11:11'


    port.remove_device(dev)


def test_dhcp():

    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/6', 'vid': 100}])

    port = chassis.ports[0]
    port.mode = PortMode.local_loopback

    client = port.create_device(DeviceType.dhcpv4_client)
    client.options = client.options

    server = port.create_device(DeviceType.dhcpv4_server, ip_address='192.168.10.1', ipaddress_pool='192.168.10.2')
    server.gateway = '192.168.10.1'
    server.gwmac = '00:10:94:00:00:10'
    
    server.connect()
    wait_for_true(lambda : server.state == DHCPServerState.up)

    assert server.gateway == '192.168.10.1'
    assert server.gwmac == '00:10:94:00:00:10'

    client.bind()
    wait_for_true(lambda : client.state == DHCPState.bound)

    assert client.stats['total_bound'] == '1', client.stats
    assert server.stats['tx']['offer'] == '1', server.stats
    assert server.stats['tx']['ack'] == '1', server.state

    client.clear_stats()
    server.clear_stats()
    
    assert client.stats['total_bound'] == '0', client.stats
    assert server.stats['tx']['offer'] == '0', server.stats
    assert server.stats['tx']['ack'] == '0', server.stats

    chassis.save('test.xml')

    port.remove_device(client)
    port.remove_device(server)

    port.mode = PortMode.normal


def test_igmp():

    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/6', 'vid': 100}])

    mcgroup = chassis.create_mcgroup()

    port = chassis.ports[0]
    port.mode = PortMode.local_loopback

    igmpDev1 = port.create_device(DeviceType.igmp)
    igmpDev2 = port.create_device(DeviceType.igmp)

    mcgroup.add(igmpDev1)
    mcgroup.add(igmpDev2)

    assert igmpDev1.state == IGMPState.non_member
    assert igmpDev2.state == IGMPState.non_member

    igmpDev1.join()
    igmpDev2.join()

    assert igmpDev1.version == IGMPVersion.igmp_v2
    assert igmpDev2.version == IGMPVersion.igmp_v2

    igmpDev1.version = IGMPVersion.igmp_v3
    igmpDev2.version = IGMPVersion.igmp_v3

    assert igmpDev1.version == IGMPVersion.igmp_v3
    assert igmpDev2.version == IGMPVersion.igmp_v3

    assert igmpDev1.filter_mode == FilterMode.include
    assert igmpDev2.filter_mode == FilterMode.include

    igmpDev1.filter_mode = FilterMode.exclude
    igmpDev2.filter_mode = FilterMode.exclude

    assert igmpDev1.filter_mode == FilterMode.exclude
    assert igmpDev2.filter_mode == FilterMode.exclude

    assert igmpDev1.state == IGMPState.member
    assert igmpDev2.state == IGMPState.member

    igmpDev1.leave()
    igmpDev2.leave()

    assert igmpDev1.state == IGMPState.non_member
    assert igmpDev2.state == IGMPState.non_member

    port.mode = PortMode.normal

def test_pppox():

    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/6', 'vid': 100}])

    port = chassis.ports[0]
    port.mode = PortMode.local_loopback

    server = port.create_device(DeviceType.pppox_server)
    client = port.create_device(DeviceType.pppox_client)

    assert server.auth == PPPoXAuthMode.none
    server.auth = PPPoXAuthMode.auto
    assert server.auth == PPPoXAuthMode.auto

    assert server.username == 'spirent'
    assert server.password == 'spirent'
    server.username = 'test'
    server.password = 'testpassword'
    assert server.username == 'test'
    assert server.password == 'testpassword'
    
    assert server.chap_include_id == True
    server.chap_include_id = False
    assert server.chap_include_id == False

    assert server.max_payload_tag == 1500
    server.max_payload_tag = 1400
    assert server.max_payload_tag == 1400

    assert server.service_name == None
    server.service_name = 'testsrvname'
    assert server.service_name == 'testsrvname'


    assert server.ac_name == 'SpirentTestCenter'
    server.ac_name = 'testsrvname'
    assert server.ac_name == 'testsrvname'

    assert client.ipcp_encap == IPCPEncap.ipv4
    client.ipcp_encap = IPCPEncap.ipv4v6
    assert client.ipcp_encap == IPCPEncap.ipv4v6
    client.ipcp_encap = IPCPEncap.ipv4

    assert client.auth == PPPoXAuthMode.none
    client.auth = PPPoXAuthMode.auto
    assert client.auth == PPPoXAuthMode.auto

    assert client.username == 'spirent'
    assert client.password == 'spirent'
    client.username = 'test'
    client.password = 'testpassword'
    assert client.username == 'test'
    assert client.password == 'testpassword'
    
    assert client.chap_include_id == True
    client.chap_include_id = False
    assert client.chap_include_id == False

    assert client.max_payload_tag == 1500
    client.max_payload_tag = 1400
    assert client.max_payload_tag == 1400

    assert client.service_name == None
    client.service_name = 'testsrvname'
    assert client.service_name == 'testsrvname'

    print(server.state)
    print(client.state)

    print(server.stats)
    print(client.stats)

    assert server.is_server
    assert not client.is_server

    server.connect()
    client.connect()

    
    wait_for_true(lambda : server.state == PPPoXState.connecting)
    wait_for_true(lambda : client.state == PPPoXState.connecting)

    assert server.stats['connecting'] == '1'
    assert client.stats['connecting'] == '1'

    server.disconnect()
    client.disconnect()

    wait_for_true(lambda : server.state == PPPoXState.idle, timeout=60)
    wait_for_true(lambda : client.state == PPPoXState.idle, timeout=60)

    assert server.stats['connecting'] == '0'
    assert client.stats['connecting'] == '0'

    port.mode = PortMode.normal