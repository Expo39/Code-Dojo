"""Thermostat reading in two scales.

Level: easy
Target: 15

Write class Temperature(celsius=0.0) for a thermostat display. It stores one
reading in degrees Celsius and exposes it through two attributes that can both be
read and assigned:

- `celsius`: assigning a value below absolute zero (-273.15 °C) raises ValueError
  and keeps the old reading.
- `kelvin`: reading it converts with K = C + 273.15; assigning to it updates the
  stored reading.

    t = Temperature(25); t.kelvin -> 298.15; t.kelvin = 373.15; t.celsius -> 100.0

Trace by hand (work out the result yourself):

    t = Temperature(10); t.celsius = 30; t.kelvin = 280.15; t.celsius = t.celsius - 5; t.kelvin -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify temperature
"""


class Temperature:
    def __init__(self, celsius=0.0):
        raise NotImplementedError
