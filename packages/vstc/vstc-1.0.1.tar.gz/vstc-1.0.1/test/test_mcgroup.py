from vstc import Chassis, DeviceType
from spirentapi import SpirentAPI

def test_chassis_mcgroup():
    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/1', 'vid': None}])
    assert len(chassis.mcgroups) == 0, 'chassis should have no mcgroup'

    mcgroup = chassis.create_mcgroup('ipv4group', ip='224.0.0.1')

    assert len(chassis.mcgroups) == 1, 'chassis should have one mcgroup'
    assert mcgroup.object.type == 'ipv4group', 'mcgroup should be ipv4group type'
    assert mcgroup.handle in SpirentAPI.instance.stc_get('project1', ['children-ipv4group']).split(' ')

    assert mcgroup.ip == '224.0.0.1'
    mcgroup.ip = '225.0.0.1'
    assert mcgroup.ip == '225.0.0.1'

    port = chassis.ports[0]
    igmpDevice = port.create_device(DeviceType.igmp)
    mcgroup.add(igmpDevice)

    igmphostconfig_handle = SpirentAPI.instance.stc_get(igmpDevice.handle, ['children-igmphostconfig'])
    assert SpirentAPI.instance.stc_get(igmphostconfig_handle, ['children-igmpgroupmembership']) == SpirentAPI.instance.stc_get(mcgroup.handle, ['subscribedgroups-Sources'])

    handle = mcgroup.handle
    chassis.remove_mcgroup(mcgroup)
    assert SpirentAPI.instance.stc_get('project1', ['children-ipv4group']) == None or handle not in SpirentAPI.instance.stc_get('project1', ['children-ipv4group']).split(' ')