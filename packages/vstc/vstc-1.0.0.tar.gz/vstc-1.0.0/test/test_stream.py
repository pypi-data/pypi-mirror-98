from vstc.testcenter import DHCPState, FillType, LengthMode, StreamState
from vstc import Chassis, PortMode, DeviceType, StreamType
from spirentapi import SpirentAPI
from wait import wait_for_true

def test_chassis_raw_streamblock():

    
    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/6', 'vid': 100}])
    port = chassis.ports[0]
    try:
        port.mode = PortMode.local_loopback
        raw_streamblock = port.create_streamblock(StreamType.raw)
        assert raw_streamblock.is_running == False
        port.start_capture()
        raw_streamblock.start()
        assert raw_streamblock.is_running == True
        raw_streamblock.stop()
        port.stop_capture()
        port.save_capture('test.pcap')
        import os
        assert os.path.exists('test.pcap')
        os.remove('test.pcap')
        assert raw_streamblock.is_running == False
        
        assert SpirentAPI.instance.stc_get(port.handle, ['children-streamblock']) == raw_streamblock.handle

        port.remove_streamblock(raw_streamblock)
        assert SpirentAPI.instance.stc_get(port.handle, ['children-streamblock']) == None

    finally:
        port.mode = PortMode.normal

def test_chassis_bound_streamblock():

    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/6', 'vid': 100}])
    
    port = chassis.ports[0]
    port.mode = PortMode.local_loopback
    
    client = port.create_device(DeviceType.dhcpv4_client)
    server = port.create_device(DeviceType.dhcpv4_server, ip_address='192.168.1.254', ipaddress_pool='192.168.1.1')

    assert client.mask == 24
    client.mask = 24
    client.gateway = '192.168.1.254'
    client.gwmac = '00:10:94:00:00:03'

    assert server.mask == 24
    server.mask = 24
    server.gateway = '192.168.1.254'
    server.gwmac = '00:10:94:00:00:03'
    server.mac = '00:10:94:00:00:03'
    
    port.start_capture()

    server.connect()
    client.bind()

    wait_for_true(lambda : client.state == DHCPState.bound)

    assert client.state == DHCPState.bound

    streamblock = port.create_streamblock(StreamType.bound, src_handle=client.handle, dst_handle=server.handle)

    assert streamblock.is_running == False

    assert streamblock.length_mode == LengthMode.fixed

    streamblock.length_mode = LengthMode.incr
    streamblock.min_length = 100
    streamblock.max_length = 1500
    streamblock.length_step = 64

    streamblock.fill_type = FillType.constant
    assert streamblock.fill_type == FillType.constant
    streamblock.fill_const = 0x1234
    assert streamblock.fill_const == 0x1234
    
    streamblock.start()

    wait_for_true(lambda : streamblock.state == StreamState.running)

    assert streamblock.is_running == True
    
    streamblock.stop()
    
    assert streamblock.is_running == False
    
    port.stop_capture()
    
    port.save_capture('test.pcap')

    chassis.save('test.xml')

    port.mode = PortMode.normal
    
    port.remove_streamblock(streamblock)