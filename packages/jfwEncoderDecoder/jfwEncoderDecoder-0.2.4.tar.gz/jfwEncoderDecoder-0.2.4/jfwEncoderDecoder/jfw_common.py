import cstruct

HAS_VHPD    =   (1<<0)
HAS_HPD     =   (1<<1)
HAS_NPD     =   (1<<2)
HAS_LPD     =   (1<<3)
HAS_VLPD    =   (1<<4)
HAS_ASYNC   =   (1<<5)


def calcultate_checksum(data, len):
    ck_a    =   0
    ck_b    =   0
    for i in range(2,len-2):
        ck_a += data[i]
        ck_b += ck_a
    ck_a &= 0xFF
    ck_b &= 0xFF
    return ck_a, ck_b

class jfw():
    def __init__(self):
        self.vhpd_mask           = HAS_VHPD
        self.hpd_mask            = HAS_HPD
        self.npd_mask            = HAS_NPD
        self.lpd_mask            = HAS_LPD
        self.vlpd_mask           = HAS_VLPD
        self.async_mask          = HAS_ASYNC
        self.fundamental_structs = [["vhpd", HAS_VHPD],["hpd", HAS_HPD],["npd", HAS_NPD],["lpd", HAS_LPD],["vlpd", HAS_VLPD],["async", HAS_ASYNC]]

class header(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        uint8_t sync_char[2];
        uint16_t len;
        uint8_t msg_id;
     """
    def print_info(self):
        print("Sync Char:  %s" % "".join([" %d" % x for x in self.sync_char]))
        print("Len :"+str(self.len))
        print("Msg Id: "+str(self.msg_id))
    
    def get_binary(self, json_data):
        for i in range(0,2):
            self.sync_char[i] = json_data['sync_char'][i]
        self.len = json_data['len']
        self.msg_id = json_data['msg_id']


class footer(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        uint8_t checksum[2];
     """
    def print_info(self):
        print("Checksum:  %s" % "".join([" %d" % x for x in self.checksum]))

    def get_binary(self, data):
        for i in range(0, 2):
            self.checksum[i] = data[i]
