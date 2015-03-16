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
import datetime
import sys

def get_time(starttime =datetime.datetime.now()):
    t0 = (starttime.hour * 3600) + (starttime.minute * 60) + starttime.second
    now = datetime.datetime.now()
    t = (now.hour * 3600) + (now.minute * 60) + now.second + t0
    return t

if __name__ == '__main__':
    controllers = core.setup(sys.argv[1], get_time)
    core.run()
