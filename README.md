# Custom fork of BlenderCAM with some simple (but potentially useful) features and changes!

* Added an experimental g-code post-processor compatible with [Marlin](https://github.com/MarlinFirmware/Marlin) based machines
* Custom tool-changing routine compatible with Marlin based machines
* Made tool definitions actually kind of work

Things I'm still adding are:
* Completely re-designed "tool-shelf" system - define cutters once in a tool shelf and select them, instead of defining per-operation. 

Unfortunately, old tool pre-sets can't just be imported directly into my modified system, so you'll need to manually copy the values over if you switch from the original repo. 

# Below is the original ReadMe, which I have kept since it has a bunch of useful links


![BlenderCAM](./static/logo.png)

# BlenderCam - CNC path addon

Blender CAM is an open source solution for artistic CAM - Computer aided machining - a g-code generation tool.
Blender CAM is an extension for the free open-source Blender 3d package.

It has been used for many milling projects, and is actively developed.
If you are a developer who would like to help, fork and open pull requests


[![Chat on Matrix](https://img.shields.io/matrix/blendercam:matrix.org?label=Chat%20on%20Matrix)](https://riot.im/app/#/room/#blendercam:matrix.org)

## Installation and Usage

See the [Wiki](https://github.com/vilemduha/blendercam/wiki).


## Resources

* [Development](https://github.com/vilemduha/blendercam)
* [Documentation](https://github.com/vilemduha/blendercam/wiki)
* [Freenode IRC](http://webchat.freenode.net/?channels=%23blendercam) (#blendercam)
* [The Matrix](https://riot.im/app/#/room/#blendercam:matrix.org) (#blendercam:matrix.org)
* [Issue Tracker](https://github.com/blendercam/blendercam/issues)


## Dependencies

* Blender 2.80 or 2.90
* OpenCamLib (optional)


## DISCLAIMER

THE AUTHORS OF THIS SOFTWARE ACCEPT ABSOLUTELY NO LIABILITY FOR
ANY HARM OR LOSS RESULTING FROM ITS USE.  IT IS _EXTREMELY_ UNWISE
TO RELY ON SOFTWARE ALONE FOR SAFETY.  Any machinery capable of
harming persons must have provisions for completely removing power
from all motors, etc, before persons enter any danger area.  All
machinery must be designed to comply with local and national safety
codes, and the authors of this software can not, and do not, take
any responsibility for such compliance.

This software is released under the GPLv2.
