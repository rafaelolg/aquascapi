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
import json
CONFIG_FILE = 'configuration.json'

def load_configuration(fname=CONFIG_FILE):
    config = json.load(open(fname))
    for c in config:
        config[c]['name'] = c
        if config[c].has_key('control'):
            control = {}
            for k in config[c]['control']:
                control[k] = config[c]['control'][k]
            config[c]['control'] = control
    return config
