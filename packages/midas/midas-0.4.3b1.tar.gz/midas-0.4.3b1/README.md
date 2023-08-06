midas
=====

Python ≥3.5 driver for [Honeywell Midas gas detectors](http://www.honeywellanalytics.com/en/products/Midas).

<p align="center">
  <img src="http://www.honeywellanalytics.com/~/media/honeywell-analytics/products/midas/images/midas.jpg" height="400" />
</p>

Installation
============

```
pip install midas
```

Usage
=====

### Command Line

To test your connection and stream real-time data, use the command-line
interface. You can read the state with:

```
$ midas 192.168.1.100
```

This will output a JSON object which can be further manipulated. See below for
object structure.


### Python

For more complex behavior, you can write a python script. This solely uses
Python ≥3.5's async/await syntax.

```python
import asyncio
from midas import GasDetector

async def get():
    async with GasDetector('192.168.1.100') as detector:
        print(await detector.get())

asyncio.run(get())
```

If the detector is operating at that address, this should output a
dictionary of the form:

```python
{
  'alarm': 'none',             # Can be 'none', 'low', or 'high'
  'concentration': 0.0,        # Current gas concentration reading
  'connected': True,           # Monitors heartbeat for connection
  'fault': {                   # Fault data, when applicable
    'code': 'F39',
    'condition': 'User has generated a simulated fault.',
    'description': 'Simulated fault',
    'recovery': 'Reset simulated fault.',
    'status': 'Instrument fault'
  },
  'flow': 514,                 # Flow rate, in cc / minute
  'high-alarm threshold': 2.0, # Threshold concentration for high alarm trigger
  'ip': '192.168.1.192',       # IP address of connection, can be used to link to Honeywell's own web interface
  'life': 538.95,              # Days until cartridge replacement required
  'low-alarm threshold': 1.0,  # Threshold concentration for low alarm trigger
  'state': 'Monitoring',       # Can be any option in `gas_detector.monitoring_status_options`
  'temperature': 26,           # Detector temperature, in celsius
  'units': 'ppm'               # Units for concentration values
}
```

Additionally, there are four commands which can be sent to the device
* Clear all alarms and faults - `detector.clear_alarms_and_faults()`
* Inhibit alarms - `detector.inhibit_alarms()`
* Inhibit alarms and faults - `detector.inhibit_alarms_and_faults()`
* Turn off inhibition - `detector.remove_inhibit()`
