#!/usr/bin/env python3

import serial
import time
import datetime
import json
import argparse
import sys


class MHZ14A():
    PACKET = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
    ZERO = [0xff, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]

    def __init__(self, ser):
        self.serial = serial.Serial(ser, 9600, timeout=1)
        time.sleep(2)

    def zero(self):
        self.serial.write(bytearray(MHZ14A.ZERO))

    def get(self):
        self.serial.write(bytearray(MHZ14A.PACKET))
        res = self.serial.read(size=9)
        res = bytearray(res)
        checksum = 0xff & (~(res[1] + res[2] + res[3] + res[4] + res[5] + res[6] + res[7]) + 1)
        if res[8] == checksum:
            return {
                "ppm": (res[2] << 8) | res[3],
                "dt": datetime.datetime.today().isoformat(),
                "ts": datetime.datetime.today().timestamp(),
            }
        else:
            raise Exception("checksum: " + hex(checksum))

    def close(self):
        self.serial.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    args = parser.parse_args()
    mode = args.mode or "co2"

    co2 = MHZ14A("/dev/ttyS0")

    if mode == "zero":
        co2.zero()
    else:
        try:
            print(json.dumps(co2.get()))
        except:
            # エラーハンドリングをする
            print("hoge")
            pass
    co2.close()


if __name__ == '__main__':
    main()