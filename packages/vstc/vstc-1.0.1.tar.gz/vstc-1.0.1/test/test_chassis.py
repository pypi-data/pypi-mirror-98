from vstc import Chassis



def test_chassis_init():
    chassis = Chassis('10.182.32.138')
    assert len(chassis.ports) == 0

    chassis = Chassis('10.182.32.138', [{ 'location' : '//10.182.32.138/1/1', 'vid': None}])
    assert len(chassis.ports) == 1

def test_chassis_connection():

    chassis = Chassis('10.182.32.138')

    if chassis.state == False:
        chassis.connect()

    chassis.disconnect()
    assert chassis.state == False, 'chassis should not be connected'
    
    chassis.connect()
    assert chassis.state == True, 'chassis should be connected'
    
    chassis.disconnect()
    assert chassis.state == False, 'chassis should not be connected'

def test_chassis_serials():
    chassis = Chassis('10.182.32.138')
    assert chassis.serial == 'E18421031'

def test_chassis_ip():
    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/1', 'vid': None}])
    assert chassis.ip == '10.182.32.138'

def test_chassis_save():
    chassis = Chassis('10.182.32.138', [{'location': '//10.182.32.138/1/1', 'vid': None}])
    import os
    if os.path.exists('test.xml'):
        os.remove('test.xml')
    
    chassis.save('test.xml')
    assert os.path.exists('test.xml')
    os.remove('test.xml')
