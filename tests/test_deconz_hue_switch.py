"""Unit tests"""
import sys
import os
import types

from unittest import mock

import pytest

from freezegun import freeze_time

from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF
)
from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_TRANSITION

from .conftest import *
from .config import config
from .events import *

import custom_components.deconz_hue_switch as DHS


def test_setup_component(mock_hass):
    assert DHS.setup(mock_hass, config)
    mock_hass.bus.listen.assert_called_once_with('deconz_event', mock.ANY)
    assert isinstance(mock_hass.bus.listen.mock_calls[0].args[1], types.FunctionType)


@pytest.mark.parametrize('event, lights, on_off, state_data', [
    (foo_btn1_event, ['light.foo'], SERVICE_TURN_ON, [{}]),
    (bar_btn1_event, ['light.bar'], SERVICE_TURN_OFF, [{}]),
    (weak_brightness_btn1_event, ['light.weak'], SERVICE_TURN_ON, [{ATTR_BRIGHTNESS: 128}]),
    (multiple_two_btn1_event, ['light.two1', 'light.two2'], SERVICE_TURN_ON, [{}]),
    (multiple_two_off_btn1_event, ['light.two_off1', 'light.two_off2'], SERVICE_TURN_OFF, [{}, {}]),
    (multiple_three_btn1_event, ['light.three1', 'light.three2', 'light.three3'], SERVICE_TURN_ON, [{}, {}, {}]),
    (group_foobar_btn1_event, ['light.foo', 'light.foobar'], SERVICE_TURN_ON, [{}, {}, {}])])
def test_component_event_switch(mock_hass, event, lights, on_off, state_data):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    handler(event)
    assert mock_hass.async_add_job.call_count == len(lights)
    for i, (light, state_attrs) in enumerate(zip(lights, state_data)):
        call = mock_hass.services.async_call.mock_calls[i]
        assert call.args[1] == on_off
        assert call.args[2][ATTR_ENTITY_ID] == light
        for key, value in state_attrs.items():
            assert call.args[2][key] == value


def test_component_event_switch_unmapped(mock_hass):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    handler(non_mapped_btn1_event)

    mock_hass.services.async_call.assert_not_called()
    mock_hass.async_add_job.assert_not_called()


def test_component_event_unknown_button(mock_hass):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    handler(unknown_button_event)

    mock_hass.services.async_call.assert_not_called()
    mock_hass.async_add_job.assert_not_called()


@pytest.mark.parametrize('event, lights, brightness, transition', [
    (dim_up_253_event, ['light.dim_253'], 255, 0.25),
    (dim_up_3_event, ['light.dim_3'], 7, 0.25),
    (dim_down_253_event, ['light.dim_253'], 249, 0.25),
    (dim_down_3_event, ['light.dim_3'], 0, 0.25),
    (start_dim_up_3_event, ['light.dim_3'], 255, 10.0),
    (start_dim_down_253_event, ['light.dim_253'], 0, 10.0),
    (dim_up_event_from_zero_brightness, ['light.foo'], 4, 0.25),
    (start_dim_up_event_from_zero_brightness, ['light.foo'], 255, 10.0)
])
def test_dim_event(mock_hass, event, lights, brightness, transition):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    handler(event)

    mock_hass.async_add_job.assert_called_once()
    mock_hass.services.async_call.assert_called_with('light', SERVICE_TURN_ON, mock.ANY)
    assert mock_hass.services.async_call.mock_calls[0].args[2][ATTR_ENTITY_ID] == lights[0]
    assert mock_hass.services.async_call.mock_calls[0].args[2][ATTR_BRIGHTNESS] == brightness
    assert mock_hass.services.async_call.mock_calls[0].args[2][ATTR_TRANSITION] == transition


def test_start_dim_after_start(mock_hass):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    handler(start_dim_down_253_event)
    mock_hass.reset_mock()

    handler(start_dim_down_253_event)
    mock_hass.services.async_call.assert_not_called()
    mock_hass.async_add_job.assert_not_called()


def test_stop_dim_no_start(mock_hass):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    handler(stop_dim_down_253_event)

    mock_hass.services.async_call.assert_not_called()
    mock_hass.async_add_job.assert_not_called()


@pytest.mark.parametrize('start_event, stop_event, stop_time, light, brightness', [
    (start_dim_down_253_event, stop_dim_down_253_event, '2020-12-13 00:00:02', 'light.dim_253', 202),
    (start_dim_down_253_event, stop_dim_down_253_event, '2020-12-13 00:00:05', 'light.dim_253', 126)
])
def test_stop_dim_after_start(mock_hass, start_event, stop_event, stop_time, light, brightness):
    DHS.setup(mock_hass, config)
    handler = mock_hass.bus.listen.mock_calls[0].args[1]
    with freeze_time('2020-12-13 00:00:00'):
        handler(start_event)
    mock_hass.reset_mock()

    with freeze_time(stop_time):
        handler(stop_event)
    mock_hass.async_add_job.assert_called_once()
    mock_hass.services.async_call.assert_called_with('light', SERVICE_TURN_ON, mock.ANY)
    assert mock_hass.services.async_call.mock_calls[0].args[2][ATTR_ENTITY_ID] == 'light.dim_253'
    assert mock_hass.services.async_call.mock_calls[0].args[2][ATTR_BRIGHTNESS] == brightness
    assert mock_hass.services.async_call.mock_calls[0].args[2][ATTR_TRANSITION] == 0.0
