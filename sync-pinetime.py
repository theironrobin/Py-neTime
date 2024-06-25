import datetime
import gatt
from argparse import ArgumentParser

def get_current_time():
    now = datetime.datetime.now()
    year_strip_0x = hex(now.year)[2:]
    lsb_raw = year_strip_0x[1:]
    if (len(lsb_raw) <= 1):
        hex_year_a = "0" + lsb_raw
    else:
        hex_year_a = lsb_raw
    split_by_lsb_raw = year_strip_0x.split(lsb_raw)
    msb_raw = split_by_lsb_raw[0]
    if (len(msb_raw) <= 1):
        hex_year_b = "0" + msb_raw
    else:
        hex_year_b = msb_raw

    month_strip_0x = hex(now.month)[2:]
    if (len(month_strip_0x) <=1 ):
        hex_month = "0" + month_strip_0x
    else:
        hex_month = month_strip_0x

    day_strip_0x = hex(now.day)[2:]
    if (len(day_strip_0x) <= 1):
        hex_day = "0" + day_strip_0x
    else:
        hex_day = day_strip_0x

    hour_strip_0x = hex(now.hour)[2:]
    if (len(hour_strip_0x) <= 1):
        hex_hour = "0" + hour_strip_0x
    else:
        hex_hour = hour_strip_0x

    minute_strip_0x = hex(now.minute)[2:]
    if (len(minute_strip_0x) <= 1):
        hex_minute = "0" + minute_strip_0x
    else:
        hex_minute = minute_strip_0x

    second_strip_0x = hex(now.second)[2:]
    if (len(second_strip_0x) <= 1):
        hex_second = "0" + second_strip_0x
    else:
        hex_second = second_strip_0x

    weekday_strip_0x = hex(now.weekday() + 1)[2:]
    if (len(weekday_strip_0x) <= 1):
        hex_weekday = "0" + weekday_strip_0x
    else:
        hex_weekday = weekday_strip_0x

    hexasecond = hex(int((now.microsecond * 256) / 1000000))
    hexasecond_strip_0x = hexasecond[2:]
    if (len(hexasecond_strip_0x) <= 1):
        hex_fractions = "0" + hexasecond_strip_0x
    else:
        hex_fractions = hexasecond_strip_0x
    hex_answer = hex_year_a + " " + hex_year_b + " " + hex_month + " " + hex_day + " " + hex_hour + " " + hex_minute + " " + hex_second + " " + hex_weekday + " " + hex_fractions
    print(hex_answer)
    return bytearray.fromhex(hex_answer)


class AnyDevice(gatt.Device):
    verbose = False
    uuid_map = {
        "00002a2b-0000-1000-8000-00805f9b34fb": "Time",
        "00002a26-0000-1000-8000-00805f9b34fb": "Firmware Version",
        "00002a19-0000-1000-8000-00805f9b34fb": "Battery Level",
        "00002a37-0000-1000-8000-00805f9b34fb": "Heart Rate",

        "00001534-1212-efde-1523-785feabcd123": "DFU Version",
        "00002a25-0000-1000-8000-00805f9b34fb": "Serial Number",
        "00002a28-0000-1000-8000-00805f9b34fb": "Software Revision",
        "00002a24-0000-1000-8000-00805f9b34fb": "Model Number",
        "00002a27-0000-1000-8000-00805f9b34fb": "Hardware Revision",
        "00002a29-0000-1000-8000-00805f9b34fb": "Manufacturer Name",
        # https://codeberg.org/prograde/InfiniTime/src/branch/main/doc/MotionService.md
        "00030002-78fc-48fe-8e23-433b3a1942d0": "Raw motion values",
        "00030001-78fc-48fe-8e23-433b3a1942d0": "Step Count",

    }

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self, action="set_time"):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        uuids = {}
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                uuid = str(characteristic.uuid)
                if uuid == "00002a2b-0000-1000-8000-00805f9b34fb":
                    print("Current Time")
                    value = get_current_time()
                    if False:
                        characteristic.write_value(value)
                    else:
                        #print("CHAR", dir(characteristic))
                        val = characteristic.read_value()
                        month = int(val[2])
                        day = int(val[3])
                        hour = int(val[4])
                        minute = int(val[5])
                        second = int(val[6])

                        print("TIME", "%d/%d %d:%d:%d" % (month, day, hour, minute,  second))
                        if False:
                            for one_val in val:
                                print(int(one_val))
                elif uuid == "00030001-78fc-48fe-8e23-433b3a1942d0": # Step count
                    dbus_array = characteristic.read_value()
                    byte_values = [int(byte) for byte in dbus_array]
                    step_count = int.from_bytes(byte_values, byteorder='little')
                    print("STEP COUNT", step_count)

                elif uuid in self.uuid_map:
                    print(self.uuid_map[uuid], uuid, "=", characteristic.read_value())
                else:
                    pass
                    #print(uuid, "=", characteristic.read_value())
                uuids[uuid] = True
                if self.verbose:
                    print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))

        #print("uuids", "\n".join(uuids.keys()))

arg_parser = ArgumentParser(description="GATT Connect")
arg_parser.add_argument('mac_address', help="MAC address of device to connect")
args = arg_parser.parse_args()
mac_address = args.mac_address

print("Connecting to device %s..." % (mac_address))

manager = gatt.DeviceManager(adapter_name='hci0')

device = AnyDevice(manager=manager, mac_address=mac_address)
device.connect()

manager.run()


