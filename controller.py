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
from scipy.interpolate import interp1d


# TIME IS ALWAYS IN SECONDS HERE
INI_T = 0
END_T = 60 * 60 * 24


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

    def _make_time_function(self, ts, values):
        ts = [INI_T] + list(ts) + [END_T]
        values = [values[0]] + list(values) + [values[-1]]
        return interp1d(ts, values, kind='linear')

class LightControl(TimeController):
    '''
    Controls a light compoment using a spline function over time.
    '''

    def __init__(self, config):
        TimeController.__init__(config)
        self.compoment = components.LightChannel()
        self.compoment.pin_number = config['pin']
        self.reconfig(config)

    def reconfig(self, config):
        self.function = self._make_function(config['control'].keys(), config['control'].values())

    def update(self, time):
        self.compoment.potency(self.function(time))


class PeristalticPumpControl(TimeController):

    '''
    Controls a peristaltic pump over time.
    '''
    DOSE_INTERVAL = 60 * 15

    def __init__(self, config):
        TimeController.__init__(config)
        self.compoment = components.Peristaltic()
        self.compoment.pin_number = config['pin']
        self.reconfig(config)

    def reconfig(self, config):
        self.compoment.flow_rate = config.get('flow_rate', components.Solenoid.DEFAULT_FLOW)
        total_volume = config['total_volume_per_day']
        self.dose = total_volume / (END_T / self.DOSE_INTERVAL)
        self.last_dose = 0

    def update(self, time):
        if time - self.last_dose > self.DOSE_INTERVAL:
            self.compoment.pump(self.dose)
            self.last_dose = time
