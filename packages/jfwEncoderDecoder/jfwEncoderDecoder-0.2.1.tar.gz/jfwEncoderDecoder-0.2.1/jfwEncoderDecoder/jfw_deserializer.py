import jfw_structs
import cstruct
import json
import glob
import os

HAS_VHPD    =   (1<<0)
HAS_HPD     =   (1<<1)
HAS_NPD     =   (1<<2)
HAS_LPD     =   (1<<3)
HAS_VLPD    =   (1<<4)
HAS_ASYNC   =   (1<<5)

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

class footer(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        uint8_t checksum[2];
     """
    def print_info(self):
        print("Checksum:  %s" % "".join([" %d" % x for x in self.checksum]))

def calcultate_checksum(data, len):
    ck_a    =   0
    ck_b    =   0
    for i in range(2,len-2):
        ck_a += data[i]
        ck_b += ck_a
    ck_a &= 0xFF
    ck_b &= 0xFF
    return ck_a, ck_b


class serializer():
    def __init__(self, buf, len):
        self.buf = buf
        self.max_size = len
        self.sync_char_off = []
        self.decode_idx = 0
        self.decoded_data = 0
        
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
            msg_header  =   header()
            header_data =   data[off:(off+5)]
            msg_header.unpack(header_data)
            packet_len  = msg_header.len
            msg_id      = msg_header.msg_id
            msg_footer  = footer()
            chcksum_offset = off+packet_len+5
            footer_data = data[(chcksum_offset): (chcksum_offset+2)]
            msg_footer.unpack(footer_data)
            packet      = data[off:(chcksum_offset+2)] #Checksum function takes the complete Frame as Input
            ck          = calcultate_checksum(packet, packet_len+7) #The Checksum function internally offsets and trims the header and footer
            
            
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
            if(msg_id & (HAS_VHPD)):
                vhpd = jfw_structs.veryHighPriorityData_t()
                vhpd_data = data[off:(off+vhpd.size)]
                off += vhpd.size
                vhpd.unpack(vhpd_data)
                imu = []
                for i in range(0,6):
                    imu.append(vhpd.imuAxes[i])
                if(debug):
                    vhpd.print_info()
                # vhpd_json = {
                # "epoch": vhpd.epoch,
                # "imu" : imu 
                # }
                # temp_json['vhpd'] = vhpd_json
                temp_json['vhpd'] = vhpd.get_dict()

            if(msg_id & (HAS_HPD)):
                hpd = jfw_structs.highPriorityData_t()
                hpd_data = data[off:(off+hpd.size)]
                off += hpd.size
                hpd.unpack(hpd_data)
                if(debug):
                    hpd.print_info()
                # hpd_json = {
                #         "rpm":hpd.rpm,
                #         "batteryShuntCurrent":hpd.batteryShuntCurrent,
                #         "batteryG3Timestamp":hpd.batteryG3Timestamp,
                #         "buckCurrent":hpd.buckCurrent,
                #         "throttle":hpd.throttle
                # }
                # temp_json['hpd'] = hpd_json
                temp_json['hpd'] = hpd.get_dict()

            if(msg_id & (HAS_NPD)):
                npd = jfw_structs.normalPriorityData_t()
                npd_data = data[off:(off+npd.size)]
                off += npd.size
                npd.unpack(npd_data)
                if(debug):
                    npd.print_info()
                # thermistor = []
                # coordinates = []
                # for i in range(0,7):
                #     thermistor.append(npd.batteryThermistorTemp[i])
                # for i in range(0,2):
                #     coordinates.append(npd.coordinates[i])
                # npd_json = {
                #         "batteryG2Timestamp":npd.batteryG2Timestamp,
                #         "batteryThermistorTemp":thermistor,
                #         "batteryIcTemp":npd.batteryIcTemp,
                #         "batteryMosfetTemp":npd.batteryMosfetTemp,
                #         "distance":npd.distance,
                #         "brake":npd.brake,
                #         "coordinates":coordinates
                # }
                # temp_json['npd'] = npd_json
                temp_json['npd'] = npd.get_dict()

            if(msg_id & (HAS_LPD)):
                lpd = jfw_structs.lowPriorityData_t()
                lpd_data = data[off:(off+lpd.size)]
                off += lpd.size
                lpd.unpack(lpd_data)
                if(debug):
                    lpd.print_info()
                # CellVoltage = []
                # for i in range(0,15):
                # CellVoltage.append(lpd.batteryCellVoltages)
                # lpd_json = {
                #         "batteryG1Timestamp":lpd.batteryG1Timestamp,
                #         "batteryCellVoltages":lpd.batteryCellVoltages,
                #         "batteryStackVoltage":lpd.batteryStackVoltage,
                #         "batterySoc":lpd.batterySoc,
                #         "batterySoh":lpd.batterySoh,
                #         "vimIcTemp":lpd.vimIcTemp
                # }
                # temp_json['lpd'] = lpd_json
                temp_json['lpd'] = lpd.get_dict()

            if(msg_id & (HAS_VLPD)):
                vlpd = jfw_structs.veryLowPriorityData_t()
                vlpd_data = data[off:(off+vlpd.size)]
                off += vlpd.size
                vlpd.unpack(vlpd_data)
                if(debug):
                    vlpd.print_info()
                # vlpd_json = {
                #         "batteryG4Timestamp":vlpd.batteryG4Timestamp,
                #         "batteryChgMosStatus":vlpd.batteryChgMosStatus,
                #         "batteryDsgMosStatus":vlpd.batteryDsgMosStatus,
                #         "batteryPreMosStatus":vlpd.batteryPreMosStatus,
                #         "batteryBalancingStatus":vlpd.batteryBalancingStatus
                # }
                # temp_json['vlpd'] = vlpd_json
                temp_json['vlpd'] = vlpd.get_dict()

            if(msg_id & (HAS_ASYNC)):
                ASYNC = jfw_structs.asyncData_t()
                off = (max_size-self.len)
                ASYNC_data = data[off:(off+ASYNC.size)]
                ASYNC.unpack(ASYNC_data)
                if(debug):
                    ASYNC.print_info()
                # id = ""
                # id.join(["%c" % x for x in ASYNC.batteryId])
                # async_json = {
                #     "timestamp":ASYNC.timestamp,
                #     "fault":ASYNC.fault,
                #     "batteryId":id
                # }
                # temp_json['async'] = async_json
                temp_json['async'] = ASYNC.get_dict() 

            self.decoded_data += (packet_len+7)

            return json.dumps(temp_json)
        except:
            return None
