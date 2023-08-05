from vstc import IP, MAC, len_of_mask, group_mac

def test_ip():
    ip = IP()
    assert ip.next() == '192.168.0.1'

    ip = IP('192.168.1.0')
    assert ip.next() == '192.168.1.1'

def test_mac():
    mac = MAC()
    assert mac.next() == '00:10:94:00:00:01'

def test_mask_len():

    assert len_of_mask('255.255.254.0') == 23

def test_group_mac():

    assert group_mac('225.0.0.1') == '01:00:5e:00:00:01'