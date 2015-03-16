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

#import components
import schedule
import sys
import datetime
import time
import controller

from config import load_configuration



def get_time():
    now = datetime.datetime.now()
    t = (now.hour * 3600) + (now.minute * 60) + now.second
    return t

def create_update_callback(compoment, calculate_time_function):
    def up_cb():
        t = calculate_time_function()
        compoment.update(t)
    return up_cb


def setup(config_file_name, calculate_time_function = get_time):
    import logging
    logging.basicConfig(level=logging.DE,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    import wiringpi_mock as wiringpi
    wiringpi.wiringPiSetupGpio()

    config_file = open(config_file_name)
    config = load_configuration(config_file)
    controllers = set()
    for name in config:
        cfg = config[name]
        c = controller.CONTROLLER_FOR_TYPE[cfg['type']](cfg)
        f = create_update_callback(cfg['type'])
        schedule.every().minute.do(f)
        controllers.add(c)
    return controllers


def run():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    controllers = setup(sys.argv[1])
    run()

