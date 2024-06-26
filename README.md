

# Py-neTime
Python script to set your PineTime (with Infinitime) to the current time, accurate to the nearest 1/256th of a second

Other features demonstrated:

  - Get current watch time
  - Read step count
  - Send notification

big thanks to https://github.com/getsenic/gatt-python

# Dependancy List

Install Python requirements:

```console
sudo pip3 install -r requirements.txt
```

Install system requirements:

```console
sudo apt-get install python3-dbus
```


# To Run

Pair your PineTime device to your machine with the `bluetoothctl` tool.

Run at the console:

```console
bluetoothctl
```

If your device is already paired, you should see the device with your mac address like this:

```console
[NEW] Device EF:C0:ED:C1:68:52 InfiniTime
```

You can list all of the available bluetoothctl commands by running `help` and you will see the list, scan, and pair commands.

Once you have paired your device and recorded the mac address, run this command to set the time on the PineTime:

```console
python3 sync-pinetime.py PINETIME-MAC-ADDRESS (E.g., EF:C0:ED:C1:68:52)
```

# Useful Links

  - https://github.com/InfiniTimeOrg/InfiniTime/blob/main/doc/ble.md#heart-rate
  - https://dbus.freedesktop.org/doc/dbus-python/dbus.html
  - https://bluedot.readthedocs.io/en/latest/pairpipi.html#using-the-command-line
  - https://wiki.pine64.org/wiki/PineTime
  - Bluetooth GATT SDK for Python -- https://github.com/getsenic/gatt-python
  - https://codeberg.org/prograde/InfiniTime/src/branch/main/doc/MotionService.md


![alt text](https://ironrobin.net/clover/droppy/$/PZvVn)
