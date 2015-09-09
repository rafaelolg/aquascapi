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

import schedule
import datetime
import time
import controller

from config import load_configuration
import wiringpi2 as wpi
import pprint


def get_time():
    now = datetime.datetime.now()
    t = (now.hour * 3600) + (now.minute * 60) + now.second
    return t


def create_update_callback(compoment, calculate_time_function):
    def up_cb():
        t = calculate_time_function()
        compoment.update(t)
    return up_cb


def setup(config_file_name, calculate_time_function=get_time, wiringpi=wpi):
    wiringpi.wiringPiSetupGpio()
    loaded_config = load_configuration(config_file_name)
    controllers = set()
    print(loaded_config)
    for name in loaded_config.keys():
        print(name)
        cfg = loaded_config[name]
        c = controller.CONTROLLER_FOR_TYPE[cfg['type']](cfg)
        f = create_update_callback(c, calculate_time_function)
        schedule.every().second.do(f)
        controllers.add(c)
    return controllers


def run():
    while True:
        schedule.run_pending()
        time.sleep(1)
