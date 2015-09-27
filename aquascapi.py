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
from wiringpi_wrapper import WirinpiWrapper

LOG_FILENAME = "/tmp/aquascapi.log"
LOG_LEVEL = logging.WARNING  # Could be e.g. "DEBUG" or "WARNING"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Aquascapi: the " +
                                     "raspberry aquarium controller")
    parser.add_argument("-c", "--config", help="configuration file",
                        default='configuration.json')
    parser.add_argument("-d", "--debug",
                        action='store_const',
                        const=True,
                        help="start in debug mode",
                        default=False)
    args = parser.parse_args()

    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    if args.debug:
        LOG_LEVEL = logging.DEBUG
    logging.getLogger().setLevel(LOG_LEVEL)
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,
                                                        when="midnight",
                                                        backupCount=3)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    print('log(DEBUG=%s) : %s'%(str(args.debug), LOG_FILENAME))
    print('configuration = (%s)'% args.config)
    wiringpi = WirinpiWrapper(mocking=args.debug)
    import core
    core.setup(args.config, wiringpi)
    core.run()
