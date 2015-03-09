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

import config
#import components
import schedule
import sys
import datetime
import time
import controller


def create_update_callback(compoment):
    def up_cb():
        now = datetime.datetime.now()
        t = (now.hour * 3600) + (now.minute * 60) + now.second
        compoment.update(t)
    return up_cb


def setup(config):
    import wiringpi2 as wiringpi
    wiringpi.wiringPiSetupGpio()
    controllers = set()
    for name in config:
        cfg = config[name]
        c = controller.CONTROLLER_FOR_TYPE[cfg['type']](cfg)
        f = create_update_callback(cfg['type'])
        schedule.every().minute.do(f)
        controllers.add(c)
    return controllers


if __name__ == '__main__':
    config_file = open(sys.argv[1])
    cfg = config.load_configuration(config_file)
    controllers = setup(cfg)
    while True:
        schedule.run_pending()
        time.sleep(1)
