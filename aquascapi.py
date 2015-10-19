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
import core

LOG_FILENAME = "/tmp/aquascapi.log"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Aquascapi: the " +
                                     "raspberry aquarium controller")
    parser.add_argument("-c", "--config", help="configuration file",
                        default='configuration.json')
    parser.add_argument("-d", "--demostration",
                    action='store_const',
                    const=True,
                    help="start demo mode showing a day in 2 minutes",
                    default=False)
    parser.add_argument("-m", "--mocking",
                    action='store_const',
                    const=True,
                    help="Dont really do anything other than print stuff",
                    default=False)
    args = parser.parse_args()


    if args.demostration:
        get_time = create_demo_get_time()
        logging.basicConfig(format='{%(module)s:%(lineno)d[%(levelname)s ]}  %(message)s',level=logging.INFO)
        logging.info('### Starting demostration')
        logging.info('### configuration = (%s)'% args.config)
    else:
	import core
        get_time = core.get_time
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        logging.getLogger().setLevel(logging.WARNING)
        handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,
                                                            when="midnight",
                                                            backupCount=3)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

    logging.getLogger('schedule').setLevel(logging.WARNING)
    wiringpi = WirinpiWrapper(mocking=args.mocking)
    print args.config
    core.setup(config_file_name=args.config, 
               wiringpi=wiringpi, 
               calculate_time_function=get_time)
    core.run()
