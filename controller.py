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

import components


class TimeController(object):
    """Abstract class to control a compoment in a timed basis"""
    def __init__(self, config):
        super(TimeController, self).__init__()
        self.name = config['name']
        self.reconfig(self, config)

    def reconfig(self, configuration):
        raise NotImplemented("Abstract Class")

    def update(self, time):
        raise NotImplemented("Abstract Class")


class LightControl(TimeController):
    '''
    Control a light compoment using a linear interpolated function over time.
    '''
    def __init__(self, config):
        TimeController.__init__(config)
        self.compoment = components.LightChannel()
        self.compoment.pin_number = config['pin']

    def reconfig(self, configuration):
        raise NotImplemented("Abstract Class")

    def update(self, time):
        raise NotImplemented("Abstract Class")
