# idling-at-home

`idling-at-home` will start and stop Folding@Home based on whether or not your computer is idle.

## Usage

Note: Must be run as administrator!

```
idling_at_home> .\env\Scripts\idling-at-home.exe --help
usage: idling-at-home [-h] [-m MIN_BATTERY] [-M MAX_BATTERY] [-c] [-t IDLE_TIME] [-a AFTERBURNER_PATH]
                      [-f FOLDING_GPU_PROFILE] [-i IDLING_GPU_PROFILE]

optional arguments:
  -h, --help            show this help message and exit
  -m MIN_BATTERY, --min-battery MIN_BATTERY
                        Stop folding when the battery percentage goes below this value. [0, 100]
  -M MAX_BATTERY, --max-battery MAX_BATTERY
                        Start folding when the battery percentage goes above this value. [0, 100]
  -c, --check-battery   Start/stop folding based on battery percentage.
  -t IDLE_TIME, --idle-time IDLE_TIME
                        The length of time in seconds that the machine must be idle before beginning to fold.
  -a AFTERBURNER_PATH, --afterburner-path AFTERBURNER_PATH
                        The path to the MSI Afterburner binary.
  -f FOLDING_GPU_PROFILE, --folding-gpu-profile FOLDING_GPU_PROFILE
                        The Afterburner profile to apply when folding.
  -i IDLING_GPU_PROFILE, --idling-gpu-profile IDLING_GPU_PROFILE
                        The Afterburner profile to apply when idling.
```
