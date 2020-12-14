"""config for the to the test suite"""

from custom_components.deconz_hue_switch.component import DOMAIN
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import State

config = {
    DOMAIN: {
        'switch_map': {
            'switch.foo': {'light.foo': None},
            'switch.foobar': {'group.foobar': None},
            'switch.bar': {'light.bar': None},
            'switch.weak': {'light.weak': {'brightness': 128}},
            'switch.two': {'light.two1': None, 'light.two2': None},
            'switch.two_off': {'light.two_off1': None, 'light.two_off2': None},
            'switch.three': {'light.three1': None, 'light.three2': None, 'light.three3': None},
            'switch.dim_253': {'light.dim_253': None},
            'switch.dim_3': {'light.dim_3': None}
        }
    },
    'group': {
        'foobar': {
            'entities': 'light.foo, light.foobar'
        }
    }
}

state_dict = {
    'light.foo': (STATE_OFF, None),
    'light.foobar': (STATE_OFF, None),
    'light.bar': (STATE_ON, None),
    'light.weak': (STATE_OFF, None),
    'light.two1': (STATE_OFF, None),
    'light.two2': (STATE_OFF, None),
    'light.two_off1': (STATE_ON, None),
    'light.two_off2': (STATE_ON, None),
    'light.three1': (STATE_OFF, None),
    'light.three2': (STATE_ON, None),
    'light.three3': (STATE_OFF, None),
    'light.dim_253': (STATE_ON, {'brightness': 253}),
    'light.dim_3': (STATE_ON, {'brightness': 3})
}

states = {}
for entity_id, (state, attributes) in state_dict.items():
    states[entity_id] = State(entity_id, state, attributes)
