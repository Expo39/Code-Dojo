"""Thermostat reading in two scales.

Level: easy
Target: 15

Write class Temperature(celsius=0.0) for a thermostat display. It stores one
reading in degrees Celsius and exposes it through two attributes that can both be
read and assigned:

- `celsius`: assigning a value below absolute zero (-273.15) raises ValueError
  and keeps the old reading.
- `fahrenheit`: reading it converts with F = C * 9 / 5 + 32; assigning to it
  updates the stored reading.

    t = Temperature(25); t.fahrenheit -> 77.0; t.fahrenheit = 212; t.celsius -> 100.0

Trace by hand (work out the result yourself):

    t = Temperature(10); t.celsius = 30; t.fahrenheit = 50; t.celsius = t.celsius - 5; t.fahrenheit -> ?

Before coding: ask your clarifying questions (the tutor answers like an interviewer),
or list your own edge cases and then compare: python dojo.py clarify temperature
"""


class Temperature:
    def __init__(self, celsius=0.0):
        raise NotImplementedError
