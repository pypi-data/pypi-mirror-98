import cstruct

class veryHighPriorityData_t(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ =""" 
       int16_t imuAxes[6];
       uint32_t epoch;
       """

    def get_dict(self):
        m_json = {}
        m_json['imuAxes'] = self.imuAxes
        m_json['epoch'] = self.epoch
        return m_json

    def get_binary(self, json_data):
        self.imuAxes = json_data['imuAxes']
        self.epoch = json_data['epoch']


class highPriorityData_t(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ =""" 
       uint16_t rpm;
       int32_t batteryShuntCurrent;
       uint32_t batteryG3Timestamp;
       int8_t buckCurrent;
       uint16_t throttle;
       """

    def get_dict(self):
        m_json = {}
        m_json['rpm'] = self.rpm
        m_json['batteryShuntCurrent'] = self.batteryShuntCurrent
        m_json['batteryG3Timestamp'] = self.batteryG3Timestamp
        m_json['buckCurrent'] = self.buckCurrent
        m_json['throttle'] = self.throttle
        return m_json

    def get_binary(self, json_data):
        self.rpm = json_data['rpm']
        self.batteryShuntCurrent = json_data['batteryShuntCurrent']
        self.batteryG3Timestamp = json_data['batteryG3Timestamp']
        self.buckCurrent = json_data['buckCurrent']
        self.throttle = json_data['throttle']


class normalPriorityData_t(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ =""" 
       uint32_t batteryG2Timestamp;
       int16_t batteryThermistorTemp[7];
       int16_t batteryIcTemp;
       int16_t batteryMosfetTemp;
       uint16_t distance;
       uint8_t brake;
       float coordinates[2];
       """

    def get_dict(self):
        m_json = {}
        m_json['batteryG2Timestamp'] = self.batteryG2Timestamp
        m_json['batteryThermistorTemp'] = self.batteryThermistorTemp
        m_json['batteryIcTemp'] = self.batteryIcTemp
        m_json['batteryMosfetTemp'] = self.batteryMosfetTemp
        m_json['distance'] = self.distance
        m_json['brake'] = self.brake
        m_json['coordinates'] = self.coordinates
        return m_json

    def get_binary(self, json_data):
        self.batteryG2Timestamp = json_data['batteryG2Timestamp']
        self.batteryThermistorTemp = json_data['batteryThermistorTemp']
        self.batteryIcTemp = json_data['batteryIcTemp']
        self.batteryMosfetTemp = json_data['batteryMosfetTemp']
        self.distance = json_data['distance']
        self.brake = json_data['brake']
        self.coordinates = json_data['coordinates']


class lowPriorityData_t(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ =""" 
       uint32_t batteryG1Timestamp;
       uint16_t batteryCellVoltages[15];
       uint16_t batteryStackVoltage;
       float batterySoc;
       float batterySoh;
       float estimatedRange;
       int32_t vimIcTemp;
       """

    def get_dict(self):
        m_json = {}
        m_json['batteryG1Timestamp'] = self.batteryG1Timestamp
        m_json['batteryCellVoltages'] = self.batteryCellVoltages
        m_json['batteryStackVoltage'] = self.batteryStackVoltage
        m_json['batterySoc'] = self.batterySoc
        m_json['batterySoh'] = self.batterySoh
        m_json['estimatedRange'] = self.estimatedRange
        m_json['vimIcTemp'] = self.vimIcTemp
        return m_json

    def get_binary(self, json_data):
        self.batteryG1Timestamp = json_data['batteryG1Timestamp']
        self.batteryCellVoltages = json_data['batteryCellVoltages']
        self.batteryStackVoltage = json_data['batteryStackVoltage']
        self.batterySoc = json_data['batterySoc']
        self.batterySoh = json_data['batterySoh']
        self.estimatedRange = json_data['estimatedRange']
        self.vimIcTemp = json_data['vimIcTemp']


class veryLowPriorityData_t(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ =""" 
       uint32_t batteryG4Timestamp;
       uint8_t batteryChgMosStatus;
       uint8_t batteryDsgMosStatus;
       uint8_t batteryPreMosStatus;
       uint16_t batteryBalancingStatus;
       """

    def get_dict(self):
        m_json = {}
        m_json['batteryG4Timestamp'] = self.batteryG4Timestamp
        m_json['batteryChgMosStatus'] = self.batteryChgMosStatus
        m_json['batteryDsgMosStatus'] = self.batteryDsgMosStatus
        m_json['batteryPreMosStatus'] = self.batteryPreMosStatus
        m_json['batteryBalancingStatus'] = self.batteryBalancingStatus
        return m_json

    def get_binary(self, json_data):
        self.batteryG4Timestamp = json_data['batteryG4Timestamp']
        self.batteryChgMosStatus = json_data['batteryChgMosStatus']
        self.batteryDsgMosStatus = json_data['batteryDsgMosStatus']
        self.batteryPreMosStatus = json_data['batteryPreMosStatus']
        self.batteryBalancingStatus = json_data['batteryBalancingStatus']


class asyncData_t(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ =""" 
       uint32_t timestamp;
       uint8_t fault;
       uint8_t batteryId[20];
       """

    def get_dict(self):
        m_json = {}
        m_json['timestamp'] = self.timestamp
        m_json['fault'] = self.fault
        m_json['batteryId'] = self.batteryId
        return m_json

    def get_binary(self, json_data):
        self.timestamp = json_data['timestamp']
        self.fault = json_data['fault']
        self.batteryId = json_data['batteryId']

