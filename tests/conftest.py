"""Pytest fixtures for deconz_hue_switch"""

from unittest.mock import MagicMock

import pytest

from homeassistant import core

from .config import states


def is_state(entity_id, entity_state):
    return states[entity_id].state == entity_state


def get_state(entity_id):
    return states.get(entity_id)


@pytest.fixture
def mock_hass():
    hass = MagicMock(spec=core.HomeAssistant)
    hass.bus = MagicMock(spec=core.EventBus)
    hass.services = MagicMock(spec=core.ServiceRegistry)
    hass.states = MagicMock()
    hass.states.is_state = is_state
    hass.states.get = get_state
    return hass
