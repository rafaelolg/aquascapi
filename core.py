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
import components
import schedule


def schedule_transition(light_channel_component, start_hour, 
	                    start_poetency, end_potency, transition_duration=15):
    delta = end_potency - start_poetency
	for i in range(transition_duration):
		hour = "%02d:%02d" % (start_hour, i)
		potency =  start_poetency + (i * (delta / transition_duration))
		schedule.every().day.at(hour).do(
			light_channel_component.potency, percentage=potency)
		)


if __name__ == '__main__':
    light_channel1 = components.LightChannel(config.PINS['light_channel1'])
    light_channel2 = components.LightChannel(config.PINS['light_channel2'])
    solenoid_co2 = components.Solenoid(config.PINS['solenoid_co2'])
    peristaltic_kno3 = components.Peristaltic(config.PINS['peristaltic_kno3'])

    # LIGHT SCHEDULE
    # first ramp up from 30% to 80% in config.LIGHT_TRANSITION minutes
    schedule_transition(light_channel_component=light_channel1, 
    	                start_hour=13, 
    	                start_poetency=5, end_potency=75)
    schedule_transition(light_channel_component=light_channel2, 
    	                start_hour=13,
    	                start_poetency=5, end_potency=75)

    schedule_transition(light_channel_component=light_channel1, 
    	                start_hour=16,
    	                start_poetency=75, end_potency=100)
    schedule_transition(light_channel_component=light_channel2, 
    	                start_hour=16,
    	                start_poetency=75, end_potency=100)



    schedule_transition(light_channel_component=light_channel1, 
    	                start_hour=18, 
    	                start_poetency=100, end_potency=75)
    schedule_transition(light_channel_component=light_channel2, 
    	                start_hour=18, 
    	                start_poetency=100, end_potency=75)

    schedule_transition(light_channel_component=light_channel1, 
    	                start_hour=21, 
    	                start_poetency=75, end_potency=0)
    schedule_transition(light_channel_component=light_channel2, 
    	                start_hour=21, 
    	                start_poetency=75, end_potency=0)
