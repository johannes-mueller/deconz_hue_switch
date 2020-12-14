import datetime

import logging

from homeassistant.const import ATTR_ENTITY_ID, SERVICE_TURN_ON, SERVICE_TURN_OFF
import homeassistant.components.light
from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_TRANSITION

from . import DOMAIN

DEFAULT_DIM_STEP_NUMBER = 8

def setup(hass, config):
    def toggle_lights(lights):
        turn_on = any([not homeassistant.components.light.is_on(hass, light) for light in lights])
        turn_command = SERVICE_TURN_ON if turn_on else SERVICE_TURN_OFF
        for light, attrs in lights.items():
            data = {
                ATTR_ENTITY_ID: light
            }
            if attrs is not None:
                data.update(attrs)
            _LOGGER.info("%s %s", turn_command, light)
            hass.async_add_job(hass.services.async_call('light', turn_command, data))

    def dim_up(lights):
        change_brightness(lights, dim_step)

    def dim_down(lights):
        change_brightness(lights, -dim_step)

    def start_dim(lights, target):
        for light in filter(lambda l: l not in dimming_lights, lights):
            dimming_lights[light] = (
                brightness_of(light), target, datetime.datetime.now()
            )
            make_brightness_transition(light, target, transition=10.0)

    def start_dim_up(lights):
        start_dim(lights, 255)

    def start_dim_down(lights):
        start_dim(lights, 0)

    def stop_dim(lights):
        for light in lights:
            dimming = dimming_lights.pop(light, None)
            if dimming is None:
                continue
            brightness, target, start_time = dimming
            seconds = (datetime.datetime.now() - start_time).total_seconds()
            stop_target = round(brightness + (target - brightness) / 10.0 * seconds)
            make_brightness_transition(light, stop_target, transition=0.0)

    def change_brightness(lights, amount):
        for light in lights:
            target = min(max(brightness_of(light) + amount, 0), 255)
            make_brightness_transition(light, target, transition=0.25)

    def make_brightness_transition(light, brightness, transition):
        data = {
            ATTR_ENTITY_ID: light,
            ATTR_BRIGHTNESS: brightness,
            ATTR_TRANSITION: transition
        }
        _LOGGER.info("changing brighness of %s to %.2f; transition: %.2f", light, brightness, transition)
        hass.async_add_job(hass.services.async_call('light', SERVICE_TURN_ON, data))

    def handle_event(event):
        _LOGGER.info("deconz_event received %s %s", event.data['id'], event.data['event'])
        lights = switch_map.get(event.data['id'])
        if lights is None:
            return
        lights = flatten_lights_groups(lights)
        button = event.data['event']
        handler_function = button_map.get(button)
        if handler_function is not None:
            handler_function(lights)

    def flatten_lights_groups(lights):
        ret = {}
        for light, attrs in lights.items():
            ret.update(turn_group_into_lights(light, attrs))
        return ret

    def turn_group_into_lights(light, attrs):
        if not light.startswith('group'):
            return {light: attrs}
        group, name = light.split('.')
        return {light.strip(): attrs for light in config[group][name]['entities'].split(',')}

    def brightness_of(light):
        if not homeassistant.components.light.is_on(hass, light):
            return 0.0
        return hass.states.get(light).attributes[ATTR_BRIGHTNESS]

    dim_step = 256 / config.get('dim_step_number', DEFAULT_DIM_STEP_NUMBER)

    dimming_lights = dict()

    button_map = {
        1002: toggle_lights,
        2001: start_dim_up,
        2002: dim_up,
        2003: stop_dim,
        3001: start_dim_down,
        3002: dim_down,
        3003: stop_dim
    }

    _LOGGER = logging.getLogger(__name__)

    switch_map = config[DOMAIN]['switch_map']
    hass.bus.listen('deconz_event', handle_event)

    return True
