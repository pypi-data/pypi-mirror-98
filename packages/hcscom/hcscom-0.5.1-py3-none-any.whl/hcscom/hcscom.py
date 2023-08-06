""" hcscom
an interface class to manson hcs lab power supplies

(c) Patrick Menschel 2021

"""

import serial
import logging

from typing import Union
from enum import Enum, IntEnum

LOGGER = logging.getLogger(__name__)


class ResponseStatus(Enum):
    ok = "OK"


class OutputStatus(IntEnum):
    off = 1
    on = 0


class DisplayStatus(IntEnum):
    cv = 0
    cc = 1


# Format values for printing
FORMAT_THREE_DIGITS = "{:04.1f}"
FORMAT_FOUR_DIGITS = "{:05.2f}"


def format_to_width_and_decimals(fmt: str):
    width, decimals = [int(x) for x in fmt.split(":")[-1].strip("f}").split(".")]
    return width - 1, decimals


def split_data_to_values(data: str = "320160", width: int = 3, decimals: int = 1):
    """ helper function to split the values from device"""
    values = tuple(int(data[idx:idx + width]) / (10 ** decimals) for idx in range(0, len(data), width))
    return values


def format_val(val, fmt):
    ret = fmt.format(val).replace(".", "")
    return ret


class HcsCom:

    def __init__(self, port: Union[str, serial.Serial]):
        if isinstance(port, str):
            try:
                self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)
            except serial.SerialException as e:
                print(e)
                exit(1)

        elif isinstance(port, serial.Serial):
            self.ser = port
        else:
            raise ValueError("Not handling {0}".format(type(port)))
        self.ser.flush()
        self.model = None
        self.max_voltage = None
        self.max_current = None
        self.value_format = None
        self.width = None
        self.decimals = None
        self.set_format(FORMAT_THREE_DIGITS)
        try:
            self.probe_device()
        except BaseException as e:
            print(e)
            exit(1)

    def set_format(self, fmt):
        """ helper function to set the format and keep consistency """
        self.value_format = fmt
        self.width, self.decimals = format_to_width_and_decimals(self.value_format)

    def request(self, msg):
        """ send command to device and receive the response """
        LOGGER.debug(">> {0}".format(msg))
        msg_ = bytearray()
        msg_.extend(msg.encode())
        msg_.extend(b"\r")
        with self.ser as ser:
            ser.write(msg_)
            ret = None
            for i in range(2):
                data = ser.read_until(b"\r")
                LOGGER.debug("<< {0}".format(data.decode()))
                if data == b"OK\r":
                    return ret
                else:
                    ret = data.strip(b"\r").decode()
        raise RuntimeError("Got unexpected response, {0}".format(data))

    def probe_device(self):
        """ probe for a device
            set the formatting and limits accordingly
        """
        self.model = self.get_model()
        data = self.request("GMAX")
        if len(data) == 6:
            fmt = FORMAT_THREE_DIGITS
        elif len(data) == 8:
            fmt = FORMAT_FOUR_DIGITS
        else:
            raise RuntimeError("Could not determine format from {0}".format(data))
        self.set_format(fmt)
        self.max_voltage, self.max_current = split_data_to_values(data, width=self.width, decimals=self.decimals)

    def __str__(self):
        max_values = self.get_max_values()
        return "Device: {0}\nV: {1}V A: {2}".format(self.model, max_values.get("voltage"), max_values.get("current"))

    def get_max_values(self) -> dict:
        """ return the max values """
        # return self.max_voltage, self.max_current
        return {"voltage": self.max_voltage,
                "current": self.max_current}

    def switch_output(self, val):
        """ switch the output """
        assert val in [OutputStatus.off, OutputStatus.on]
        return self.request("SOUT{0}".format(val))

    def set_voltage(self, val):
        """ set the voltage limit """
        return self.request("VOLT{0}".format(format_val(val, self.value_format)))

    def set_current(self, val):
        """ set the current limit """
        return self.request("CURR{0}".format(format_val(val, self.value_format)))

    def get_presets(self):
        """ get the current active presets """
        data = self.request("GETS")
        volt, curr = split_data_to_values(data, width=self.width, decimals=self.decimals)
        return volt, curr

    def get_display_status(self):
        """ get the current display status """
        data = self.request("GETD")
        volt, curr = split_data_to_values(data[:-1], width=4, decimals=2)  # XXXXYYYYZ FORMAT regardless of regular format
        status_ = int(data[-1])
        try:
            status = DisplayStatus(status_)
        except ValueError as e:
            LOGGER.error("get_display_status: {0}".format(e))
            status = status_
        return {"voltage": volt,
                "current": curr,
                "status": status}

    def set_presets_to_memory(self, presets=None):
        """ program preset values into memory
            TODO: check if there are always 3 presets
        """
        if not presets:
            presets = {0: (5, self.max_current),
                       1: (13.8, self.max_current),
                       2: (self.max_voltage, self.max_current),
                       }
        values = []
        for idx in range(len(presets)):
            values.extend(presets.get(idx))
        assert len(values) == 6
        content = "".join([format_val(value, self.value_format) for value in values])
        return self.request("PROM{0}".format(content))

    def get_presets_from_memory(self) -> dict:
        """ get the presets from device memory """
        data = self.request("GETM")
        volt, curr, volt2, curr2, volt3, curr3 = split_data_to_values(data, width=self.width, decimals=self.decimals)

        return {0: (volt, curr),
                1: (volt2, curr2),
                2: (volt3, curr3),
                }

    def load_preset(self, val):
        """ load one of the presets """
        assert val in range(3)
        return self.request("RUNM{0}".format(val))

    def get_output_voltage_preset(self):
        """ get the preset voltage """
        data = self.request("GOVP")
        volt = split_data_to_values(data, width=self.width, decimals=self.decimals)[0]
        return volt

    def set_output_voltage_preset(self, val):
        """ set the preset voltage """
        return self.request("SOVP{0}".format(format_val(val, self.value_format)))

    def get_output_current_preset(self):
        """ get the preset current """
        data = self.request("GOCP")
        volt = split_data_to_values(data, width=self.width, decimals=self.decimals)[0]
        return volt

    def set_output_current_preset(self, val):
        """ set the preset current """
        return self.request("SOCP{0}".format(format_val(val, self.value_format)))

    def get_model(self):
        """ get the model information """
        data = self.request("GMOD")
        LOGGER.info("GMOD returned model {0}".format(data))
        return data


if __name__ == "__main__":
    import argparse
    import numpy as np
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    args = parser.parse_args()
    port = args.port
    hcs = HcsCom(port=port)
    max_volt = hcs.get_max_values().get("voltage")
    input("Testing stepping through the output voltage range - be sure nothing is connected! - Press Enter")
    hcs.set_current(0.5)  # This is a test, so expect user errors as well
    hcs.switch_output(OutputStatus.on)
    for volt in np.arange(1, max_volt, 0.5):
        hcs.set_voltage(volt)
        time.sleep(.5)
    hcs.load_preset(0)  # select a harmless preset with 5V
    hcs.switch_output(OutputStatus.off)
