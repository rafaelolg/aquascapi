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

import core
import sys


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s\
                                %(filename)s:%(lineno)-4d: %(message)s',
                        datefmt='%m-%d %H:%M',
                        )

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s')
    controllers = core.setup(sys.argv[1])
    core.run()
