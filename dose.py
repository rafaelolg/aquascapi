#!/usr/bin/env python
#
# This file is part of Aquascapi.
# Aquascapi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Aquascapi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Aquascapi.  If not, see <http://www.gnu.org/licenses/>.
# Copyright Rafael Lopes

import argparse
import logging
import logging.handlers
from demo import create_demo_get_time
from wiringpi_wrapper import WirinpiWrapper
import components

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dose: force a dose from a given dosing pump " +
                                     "raspberry aquarium controller")
    parser.add_argument("pin_number", help="Dosing pump pin", type=int)
    parser.add_argument("dose_time", help="Total seconds of dose", type=int)
    args = parser.parse_args()

    wiringpi = WirinpiWrapper()
    wiringpi.wiringPiSetupGpio()
    doser = components.Peristaltic(args.pin_number, wiringpi)
    doser.pump(args.dose_time * doser.DEFAULT_FLOW)