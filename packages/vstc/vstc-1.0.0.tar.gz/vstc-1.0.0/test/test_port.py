from vstc import Chassis, OwnershipState
import getpass
import socket

def test_port():

    chassis = Chassis('10.182.32.138', [{ 'location' : '//10.182.32.138/1/1', 'vid': None}])

    port = chassis.ports[0]

    assert port.location == '//10.182.32.138/1/1'
    assert port.vid == None

    assert port.owner_host == socket.gethostname()
    assert port.owner_user == getpass.getuser()
    assert port.ownership == OwnershipState.RESERVED
