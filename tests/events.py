"""Events sent to the test component"""

from homeassistant.core import Event

foo_btn1_event = Event('type', data={
    'id': 'switch.foo',
    'event': 1002
})

bar_btn1_event = Event('type', data={
    'id': 'switch.bar',
    'event': 1002
})

group_two_btn1_event = Event('type', data={
    'id': 'switch.two',
    'event': 1002
})

group_two_off_btn1_event = Event('type', data={
    'id': 'switch.two_off',
    'event': 1002
})

group_three_btn1_event = Event('type', data={
    'id': 'switch.three',
    'event': 1002
})

weak_brightness_btn1_event = Event('type', data={
    'id': 'switch.weak',
    'event': 1002
})

non_mapped_btn1_event = Event('type', data={
    'id': 'switch.unmapped',
    'event': 1002
})

dim_up_253_event = Event('type', data={
    'id': 'switch.dim_253',
    'event': 2002
})

dim_up_3_event = Event('type', data={
    'id': 'switch.dim_3',
    'event': 2002
})

dim_down_253_event = Event('type', data={
    'id': 'switch.dim_253',
    'event': 3002
})

dim_down_3_event = Event('type', data={
    'id': 'switch.dim_3',
    'event': 3002
})

start_dim_up_3_event = Event('type', data={
    'id': 'switch.dim_3',
    'event': 2001
})

start_dim_down_253_event = Event('type', data={
    'id': 'switch.dim_253',
    'event': 3001
})

stop_dim_up_3_event = Event('type', data={
    'id': 'switch.dim_3',
    'event': 2003
})

stop_dim_down_253_event = Event('type', data={
    'id': 'switch.dim_253',
    'event': 3003
})
