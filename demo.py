#!/usr/bin/env python
#
# This file is part of Aquascapi.
# Aquascapi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option later version.
# Aquasca distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Aquascapi.  If not, see <http://www.gnu.org/licenses/>.
# Copyright Rafael Lopes

import datetime
import logging
import time
START = time.time()

def create_demo_get_time(demonstration_total_time=120):
    '''
    Create a day in demonstration_total_time seconds.
    '''
    def get_time():
        global START
        delta =  time.time() - START
        logging.debug('delta = %s', delta)
        if delta > 120:
            raise Exception('End of demo')
        t = (delta/float(demonstration_total_time)) * (60 * 60 * 24)
        print('#### TIME  = %s%%'%(delta/float(demonstration_total_time)))
        return t
    return get_time
