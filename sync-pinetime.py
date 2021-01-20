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
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                if characteristic.uuid == "00002a2b-0000-1000-8000-00805f9b34fb":
                    print("Current Time")
                    value = get_current_time()
                    characteristic.write_value(value)
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))


arg_parser = ArgumentParser(description="GATT Connect")
arg_parser.add_argument('mac_address', help="MAC address of device to connect")
args = arg_parser.parse_args()

print("Connecting...")

manager = gatt.DeviceManager(adapter_name='hci0')

device = AnyDevice(manager=manager, mac_address=args.mac_address)
device.connect()

manager.run()


