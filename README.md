
# deCONZ Hue Switch for Home Assistant

Custom component for Home Assistant to handle Philips dim switches operated by
a deCONZ integration in a different way.


## Goal

This custom component lets you map your Philips dim switches behind a deCONZ
integration, so without the Philips Hue Bridge, to lights and light groups.


### Button behavior

The Philips Hue Dim switches have four buttons, '1', '+', '-' and '0'. The
usual behavior is that the '1' button switches a light on and the '0' button
off. That behavior has the disadvantage that it actually wastes one button. If
the '1' button toggled the light, thus is used for both switching on and off,
the '0' button could be used for some other gimmick.

That way you can also use switches that don't have the '0' button, like the
IKEA Trådfri ones in the same setup.


### Switch mapping

This custom component allows you to freely map switches to an arbitrary number
of lights. Moreover you can assign any attribute, like brightness, color
temperature, color, etc to each lamp. That way you can switch and dim complex
groups of lights with one dim switch


## Usage

You have to configure this integration in your `configuration.yaml` like in the
following example.

```yaml
deconz_hue_switch:
  dim_step_number: 16  # 16 dim steps from switched off light to full brighness
                       # (default: 8)
  switch_map:
    kitchen_switch:
      group.kitchen_table:
      light.kitchen_sink:
    front_door_switch:
      light.hall:
      group.kitchen_table:
      group.living_room:
    nightly_bathroom_switch:
      light.bedroom_1:
        brightness: 8
      light.hall:
        brightness: 8
      light.bathroom:
        brightness: 8
    ...
```

You assign in the `switch_map` section to every switch a set of lights or light
groups and then can assign to every light attributes like brightness. When you
press the '1' button of a switch all the lights assigned are switched on if *at
least* is switched off. If they are all switched on, they are all switched off.
