import re
from typing import NoReturn

class MAC:
    """MAC class
    
    used to generate mac address
    such as 
        mac = MAC('00:10:94:00:00:00')
        mac.next() will generate 00:10:94:00:00:01
    """
    def __init__(self, addr:str='00:10:94:00:00:00') -> NoReturn:
        """init

        Args:
            addr (str, optional): base mac address。default is 00:10:94:00:00:00
        """
        self.macExp = re.compile('([A-Fa-f0-9]{2,2}):([A-Fa-f0-9]{2,2}):([A-Fa-f0-9]{2,2}):([A-Fa-f0-9]{2,2}):([A-Fa-f0-9]{2,2}):([A-Fa-f0-9]{2,2})')
        assert self.macExp.match(addr) != None, 'invalid mac addr: %s' % addr
        self.addr = addr

    def _incrHex(self, hex) -> int:
        """increase hex
        
        increase specified hex, and check if it should need carry

        Args:
            hex (str or int): hex to increase
        
        Returns:
            tuple: (carry, increased hex str)
        """
        if type(hex) == str:
            hex = int(hex, 16)
            
        hex = hex + 1

        if hex > 255:
            return 1, '00'
        else:
            return 0, '%02x' % hex
       
    def next(self) -> NoReturn:
        """generate next mac address

        Returns:
            str: mac address
        """
        m1, m2, m3, m4, m5, m6 = self.macExp.match(self.addr).groups()

        incr, m6 = self._incrHex(m6)
        if incr == 1:
            incr, m5 =self._incrHex(m5)
            if incr == 1:
                incr, m4 = self._incrHex(m4)
                assert incr == 0
        
        self.addr = '%s:%s:%s:%s:%s:%s' % (m1, m2, m3, m4, m5, m6)
        return self.addr

class IP:
    """IP class
    
    such as 
        ip = IP('192.168.0.0')
        ip.next() will generate 192.168.0.1
    """

    def __init__(self, addr='192.168.0.0') -> NoReturn:
        """init

        Args:
            addr (str, optional): base ip address
        """

        self.ipExp = re.compile('(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})')

        match = self.ipExp.match(addr)
        assert match != None, 'invalid ip address: %s' % addr
        a, b, c, d = match.groups()
        intA, intB, intC, intD = int(a), int(b), int(c), int(d)

        assert intD == 0, 'invalid ip address: %s, expected %s.%s.%s.0' % (addr, intA, intB, intC)

        self.addr = addr
        self.gateway = '%s.%s.%s.254' % (intA, intB, intC)

    def next(self) -> str:
        """generate next ip address

        Returns:
            str: generated ip address
        """
                
        a, b, c, d = self.ipExp.match(self.addr).groups()
        intA, intB, intC, intD = int(a), int(b), int(c), int(d)
        intD = intD + 1
        assert intD < 254, 'out of range: %d.%d.%d.%d' % (intA, intB, intC, intD)

        self.addr = '%d.%d.%d.%d' % (intA, intB, intC, intD)

        return self.addr

def group_mac(ip:str) -> str:
    """generate group mac address based on ip address

    Args:
        ip (str): ip address

    Returns:
        str: mac address
    """
    assert type('ip') ==  str


    ipExp = re.compile('(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})')

    # validate ip address
    match = ipExp.match(ip)
    assert match != None, 'invalid ip address: %s' % ip

    # convert ip address to binary str with 32 length
    a, b, c, d = match.groups()
    a, b, c, d = int(a), int(b), int(c), int(d)
    strBinary = bin(((a << 8 | b ) << 8 | c) << 8 | d)[2:]
    
    # validate if valid group address
    assert strBinary[0:4] == '1110', 'group ip address should be started with 1110, but started with %s' % strBinary[0:4]

    # convert to binary mac address
    strMac = '00000001' + '00000000' + '01011110' + '0' + strBinary[9:]

    # convert to hex mac address
    a, b, c, d, e, f = int(strMac[0:8], 2), int(strMac[8:16], 2), int(strMac[16:24], 2), int(strMac[24:32], 2), int(strMac[32:40], 2), int(strMac[40:48], 2)
    strHexMax = '%02x:%02x:%02x:%02x:%02x:%02x' % (a, b, c, d, e, f)
    
    return strHexMax

def len_of_mask(mask) -> int:
    """calculate length of mask

    Args:
        mask (str): dot type mask

    Return:
        int: length of mask. such as 255.255.255.0 to 24
    """
    maskExpr = re.compile('(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})')
    match = maskExpr.match(mask)
    a, b, c, d = match.groups()
    a, b, c, d = int(a), int(b), int(c), int(d)
    strBinary = bin(((a << 8 | b ) << 8 | c) << 8 | d)[2:]

    length = 0
    zero = False
    for i in strBinary:
        if i == '1' and zero == False:
            length = length + 1
        
        if i == '1' and zero == True:
            raise RuntimeWarning('invalid subnet mask: %s' % strBinary)
        
        if i == '0':
            zero = True

    return length