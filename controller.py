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
# along with Aquascapi.  If not, see <http://www.gnu.org/licenses/>
# Copyright Rafael Lopes

import components
from scipy.interpolate import interp1d
import logging
import re

# TIME IS ALWAYS IN SECONDS HERE
INI_T = 0
END_T = 24 * 60 * 60  # seconds in a day


def parse_time(timestring):
    '''
    Parse strings like 16h22m01s to number of seconds since 0h0m0s
    '''
    match = re.match(r'(\d+)h(\d+)m(\d+)s', timestring)
    if match:
        [h, m, s] = match.groups()
        return (3600*int(h)) + (int(m)*60) + int(s)
    else:
        raise Exception('not a time string %s' % timestring)


class TimeController(object):

    """Abstract class to control a component in a timed basis"""

    def __init__(self, config):
        super(TimeController, self).__init__()
        self.name = config['name']
        self.reconfig(config)

    def reconfig(self, configuration):
        raise NotImplemented("Abstract Class")

    def update(self, time):
        pass

    def _make_time_function(self, ts, values):
        ts = [INI_T] + list(ts) + [END_T]
        values = [values[0]] + list(values) + [values[-1]]
        return interp1d(ts, values, kind='linear')


class LightControl(TimeController):

    '''
    Controls a light component using a spline function over time.
    '''

    def __init__(self, config):
        TimeController.__init__(self, config)
        self.component = components.LightChannel(config['pin'],
                                                 config['wiringpi'])
        self.reconfig(config)

    def reconfig(self, config):
        x = []
        y = []
        for k in sorted(config['control'].keys()):
            x.append(parse_time(k))
            y.append(config['control'][k])
        self.function = self._make_time_function(x, y)

    def update(self, time):
        TimeController.update(self, time)
        p = self.function(time)
        logging.debug('( Light potency %s)\n', p)
        self.component.potency(p)


class PeristalticPumpControl(TimeController):

    '''
    Controls a peristaltic pump over time.
    '''
    DOSE_INTERVAL = 60 * 15

    def __init__(self, config):
        self.component = components.Peristaltic(config['pin'],
                                                config['wiringpi'])
        TimeController.__init__(self, config)
        self.totalofday = 0
        self.reconfig(config)

    def reconfig(self, config):
        self.component.flow_rate = config.get('flow_rate', components.Peristaltic.DEFAULT_FLOW)
        total_volume = config['total_volume_per_day']
        self.dose = total_volume / (END_T / self.DOSE_INTERVAL)
        self.last_dose = 0

    def update(self, time):
        TimeController.update(self, time)
        if (time - self.last_dose > self.DOSE_INTERVAL) or (time < self.last_dose):
            if time < self.last_dose:
                self.totalofday = 0
            self.component.pump(self.dose)
            self.last_dose = time
            self.totalofday = self.totalofday + self.dose
            logging.debug("(Peristaltic of day) total: %f",  self.totalofday)


CONTROLLER_FOR_TYPE = {
    'light': LightControl,
    "peristaltic": PeristalticPumpControl
}
