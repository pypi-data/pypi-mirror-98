from binascii import hexlify
from past.builtins import xrange

class Motion(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, trigger_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.trigger_id = trigger_id
        self.trigger_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic

    def connected(self):
        self.is_connected = 1
        print("Motion" + str(self.id) + " connected")
        
    def disconnected(self):
        self.is_connected = 0
        print("Motion" + str(self.id) + " disconnected")

    def get_motion(self, topic=None):
        packet_size = 0x03
        command_id = 0x83
        payload_size = 0x01
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])

        if topic is None:
            topic = self.default_topic
        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                status = hexlify(self.BLE.read_from_robo())
                status = [status[i:i+2] for i in xrange(0, len(status), 2)]

                if len(status) != 4:
                    return
                motion = int(status[-2], 16)
                return motion

            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id])
                self.MQTT.message = "None"
                self.MQTT.publish(topic, command)
                while self.MQTT.message[0:2] != '83':
                  time.sleep(0.01)
                status = self.MQTT.message
                status = [status[i:i+2] for i in xrange(0, len(status), 2)]
                if status is None:
                    return
                if status[0] == '83':
                    if status[2] == '01':
                        return 1
                    if status[2] == '00':
                        return 0
                return
        print(self.name + " is NOT Connected!")

    def set_trigger(self, condition, topic=None):
        packet_size = 0x05
        command_id = 0xB3
        payload_size = 0x03
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.trigger_id, module_id, condition])

        if topic is None:
            topic = self.default_topic

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, self.trigger_id, module_id, condition])
                self.MQTT.publish(topic, command)
                return 
        print(self.name + " is NOT Connected!")

    def triggered(self, cmd_id, cmd_status):
        if self.trigger_id == cmd_id:
            self.trigger_status = cmd_status

    def check_trigger(self):
        value = self.trigger_status
        if value is None:
            return False
        self.trigger_status = None
        return True
