# WiFi UFO Drone
This Python script allows remote control of some drone models via computer keyboard.

## Requirements
 - pygame
 - scapy

## Constants
 - Constants can be edited in [dronecontrol.py](https://github.com/LukasMaly/wifi-ufo-drone/blob/master/wifi_ufo_drone/dronecontrol.py "LukasMaly/dronecontrol.py").
 - Source IP: `192.168.0.2`
 - Network Interface: `en0`
 - Destination IP: `192.168.0.1`
 - TCP Port: `7060`
 - UDP Port: `40000`

## Keyboard Controls
| Key | Control |
| --- | --- |
| Esc | Exit Control |
| Spacebar | Vertical Takeoff/Land |
| Tab | Cycle Speeds |
| W/A/S/D | Pitch Forward/Left/Down/Right |
| ↑ | Throttle Up |
| ↓ | Throttle Down |
| → | Yaw Right |
| ← | Yaw Left |

## License
 - MIT License
