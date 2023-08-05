from jfwEncoderDecoder import jfw_structs
from jfwEncoderDecoder import jfw_common
import cstruct
import json

class deserializer():
    def __init__(self, buf, len):
        self.buf = buf
        self.max_size = len
        self.sync_char_off = []
        self.decode_idx = 0
        self.decoded_data = 0
        self.common = jfw_common.jfw()
        
    def search(self):
        ret = False
        for i in range(0, self.max_size):
            x = self.buf.find(b'\xb5b', i, i+2)
            if(x>=0):
                self.sync_char_off.append(x)
                ret = True
        return ret

    def subSearch(self, data, len):
        ret = False
        for i in range(0, len):
            x = data.find(b'\xb5b', i, i+2)
            if(x>=0):
                ret = True
        return ret
    
    def loss(self):
        try:
            return "%0.3f%% (Approx)"%(((self.max_size - self.decoded_data)/self.max_size)*100)
        except Exception as e:
            return str(e)

    def decode(self, debug = False):
        try:
            data = self.buf
            max_size = self.max_size
            off = self.sync_char_off[self.decode_idx]
            self.decode_idx += 1
            temp_json = {}
            packet_len = 0     
            msg_header  =   jfw_common.header()
            header_data =   data[off:(off+5)]
            msg_header.unpack(header_data)
            packet_len  = msg_header.len
            msg_id      = msg_header.msg_id
            msg_footer  = jfw_common.footer()
            chcksum_offset = off+packet_len+5
            footer_data = data[(chcksum_offset): (chcksum_offset+2)]
            msg_footer.unpack(footer_data)
            packet      = data[off:(chcksum_offset+2)] #Checksum function takes the complete Frame as Input
            ck          = jfw_common.calcultate_checksum(packet, packet_len+7) #The Checksum function internally offsets and trims the header and footer
            
            
            if(ck[0] != msg_footer.checksum[0] or ck[1] != msg_footer.checksum[1]):
                # test_packet = data[off+2:(off+7+packet_len)]
                # if(self.subSearch(test_packet, len(test_packet)) == False):
                #     self.bad_data += packet_len+7
                # else:
                #     print("Substring within Data")
                if(debug):
                    msg_header.print_info()
                    msg_footer.print_info()
                return
            off += 5
            if(msg_id & (self.common.vhpd_mask)):
                vhpd = jfw_structs.veryHighPriorityData_t()
                vhpd_data = data[off:(off+vhpd.size)]
                off += vhpd.size
                vhpd.unpack(vhpd_data)
                imu = []
                for i in range(0,6):
                    imu.append(vhpd.imuAxes[i])
                if(debug):
                    vhpd.print_info()
                temp_json['vhpd'] = vhpd.get_dict()

            if(msg_id & (self.common.hpd_mask)):
                hpd = jfw_structs.highPriorityData_t()
                hpd_data = data[off:(off+hpd.size)]
                off += hpd.size
                hpd.unpack(hpd_data)
                if(debug):
                    hpd.print_info()
                temp_json['hpd'] = hpd.get_dict()

            if(msg_id & (self.common.npd_mask)):
                npd = jfw_structs.normalPriorityData_t()
                npd_data = data[off:(off+npd.size)]
                off += npd.size
                npd.unpack(npd_data)
                if(debug):
                    npd.print_info()
                temp_json['npd'] = npd.get_dict()

            if(msg_id & (self.common.lpd_mask)):
                lpd = jfw_structs.lowPriorityData_t()
                lpd_data = data[off:(off+lpd.size)]
                off += lpd.size
                lpd.unpack(lpd_data)
                if(debug):
                    lpd.print_info()
                temp_json['lpd'] = lpd.get_dict()

            if(msg_id & (self.common.vlpd_mask)):
                vlpd = jfw_structs.veryLowPriorityData_t()
                vlpd_data = data[off:(off+vlpd.size)]
                off += vlpd.size
                vlpd.unpack(vlpd_data)
                if(debug):
                    vlpd.print_info()
                temp_json['vlpd'] = vlpd.get_dict()

            if(msg_id & (self.common.async_mask)):
                ASYNC = jfw_structs.asyncData_t()
                off = (max_size-self.len)
                ASYNC_data = data[off:(off+ASYNC.size)]
                ASYNC.unpack(ASYNC_data)
                if(debug):
                    ASYNC.print_info()
                temp_json['async'] = ASYNC.get_dict() 

            self.decoded_data += (packet_len+7)
            return json.dumps(temp_json)
        except:
            return None
