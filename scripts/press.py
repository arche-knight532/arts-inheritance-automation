import argparse
import sys
import time
from configparser import ConfigParser

import serial


config = ConfigParser()
config.read("config.ini")
port = config["DEFAULT"]["port"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=port)
    parser.add_argument('--duration', type=float, default=.1)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('key')
    args = parser.parse_args()

    with serial.Serial(args.serial, 9600) as ser:
        for _ in range(args.count):
            ser.write(args.key.encode())
            time.sleep(args.duration)
            ser.write(b'0')
            time.sleep(.05)
    return 0


if __name__ == '__main__':
    main()
