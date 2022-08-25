#!/usr/bin/python3

import subprocess
from shutil import which


class BTdevice():
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac

    def getProperties(self):
        return self.name, self.mac
    
    def __str__(self) -> str:
        return f"BTdevice({self.name}, {self.mac})"

def build_devices():
    cmd_bt_devices = 'bluetoothctl devices'
    devices = set()
    t = subprocess.Popen([cmd_bt_devices], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    lines = [t.split(' ') for t in t.stdout.read().decode('utf-8').split('\n') if t]
    for line in lines:
        devices.add(BTdevice(mac = line[1], name = " ".join(line[2:])))

    return devices



if __name__ == "__main__":
    if which("bluetoothctl") is not None:
        bt_connected = "no"
        bt_devices = build_devices()

        for dev in bt_devices:
            name, mac = dev.getProperties()
            cmd_bt_connected = 'bluetoothctl info ' + mac + ' | grep -i connected | awk \'{print $2}\''
            t = subprocess.Popen([cmd_bt_connected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            bt_connected = t.stdout.read().decode('utf-8').strip('\n')
            if bt_connected == "yes":
                print(name)
                break
        if bt_connected == "no":
            print("None")
    else:
        print("bluetoothctl missing")