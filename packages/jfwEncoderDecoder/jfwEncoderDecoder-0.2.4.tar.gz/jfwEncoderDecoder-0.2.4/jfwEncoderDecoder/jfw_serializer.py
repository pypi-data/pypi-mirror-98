from jfwEncoderDecoder import jfw_structs
from jfwEncoderDecoder import jfw_common
import cstruct


class serializer():
    def __init__(self, buf, len):
        self.buf = buf
        self.sync_char = [0xb5, 0x62]
        self.common = jfw_common.jfw()
    
    def encode(self, debug = False):
        try:
            temp_data = self.buf
            msg_id = 0
            pkt_size = 0
            pkt_data = []
            fundamental_structures = []
            for i in range(0, 6):
                fundamental_structures.append(0)
            fundamental_structures[0] = jfw_structs.veryHighPriorityData_t()
            fundamental_structures[1] = jfw_structs.highPriorityData_t()
            fundamental_structures[2] = jfw_structs.normalPriorityData_t()
            fundamental_structures[3] = jfw_structs.lowPriorityData_t()
            fundamental_structures[4] = jfw_structs.veryLowPriorityData_t()
            fundamental_structures[5] = jfw_structs.asyncData_t()
            for i in range(0, len(self.common.fundamental_structs)):
                if self.common.fundamental_structs[i][0] in temp_data:
                    msg_id          |=  self.common.fundamental_structs[i][1]
                    fundamental_structures[i].get_binary(temp_data[str(self.common.fundamental_structs[i][0])])
                    pkt_size        +=  fundamental_structures[i].size
                    pkt_data.append(fundamental_structures[i].pack())
            j_data = {}
            j_data['sync_char']  =   self.sync_char
            j_data['len']        =   pkt_size
            j_data['msg_id']     =   msg_id
            temp_header = jfw_common.header()
            temp_header.get_binary(j_data)
            pkt = b""
            pkt += temp_header.pack()
            for i in range(0, len(pkt_data)):
                pkt += pkt_data[i]
            checksum = jfw_common.calcultate_checksum(pkt, len(pkt) + 2)
            temp_footer = jfw_common.footer()
            temp_footer.get_binary(checksum)
            pkt += temp_footer.pack()
            return pkt
        except:
            pass