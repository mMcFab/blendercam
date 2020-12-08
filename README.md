# Custom fork of BlenderCAM with some simple (but potentially useful) features and changes!

* Scene menu selection is no longer "Cam", but "BlenderCAM", to really remind you what it is you're using!
* Reworked UI with a new, more compact default layout that tries to create better "flow" when setting up operations, as well as new names that I find easier to understand
* Added an experimental g-code post-processor compatible with [Marlin](https://github.com/MarlinFirmware/Marlin) based machines
* Custom tool-changing routine compatible with Marlin based machines
* Completely re-designed "tool-shelf" system - define cutters once in a tool shelf and select them, instead of defining per-operation. 
* Updated method of passing tool definitions to post-processors to give greater control
* A few bug-fixes I should create PRs for probably but I've never done that before

Unfortunately, old tool pre-sets can't just be imported directly into my modified system, so you'll need to manually copy the values over if you switch from the original repo. Operation presets will copy around mostly, but step-over and tools will need to be specified

I haven't tested this with OpenCAMLib yet, since I don't have the disk space free to install the tools to build it oops. I did update the code that seems to update it though

A few more specific changes: 

* "Distance between lines" is no longer a constant measurement and has been replaced with "Tool Stepover", which is a percentage of the diameter of the active tool instead
* Lots of names have been changed for consistency with other programs and hopefully reducing confusion - eg. Chains -> Sequences, Bridges -> Tabs, etc
* Menus that require an operation are now nested within the operations menu. Menu options have been moved around and re-organised to be grouped in a semi-logical order
* Lots of labelling and layout.box() used to make it easier to scan for options. The subtle changes in grey that Blender uses by default make it very difficult for me to distinguish when one set of options ends and another set starts - boxes help a lot
* Names of tools, operations and sequences are validated and made unique whenever possible, since some things depend on the names being unique and consistent. 
* Operation names are properly sync'd with chains/sequences, and are removed from a sequence when deleted. This may require you to "rename" a sequence or operation to the same name for it to prepare the correct things to work properly if your chain/operation was created in a different/earlier version of BlenderCam
* Process in background was hidden since it doesn't seem to work right now
* Unused settings are hidden for now
* Exporting now uses a file dialog instead of silently outputting the file into the Blender document directory. Default names are formatted as "\[document\]_\[operation/sequence\].extension
* (fixed) and made sequence simulation use the full material bounds of all the operations it performs, rather than just the first

# WARNING:
**RIGHT NOW THE MARLIN EXPORT DOES NOT FULLY WORK, IT MOVES TO MACHINE ORIGIN AND STARTS BURYING THE TOOL HEAD. WAIT WHILE I GET A FIX AND REMOVE THIS MESSAGE**

The Marlin export sets the machine position to 0,0,0 at the start of the job and **disables software endstops** so that it can cut at negative Z - this means if you are not careful, you could damage your machine! Please test, check and simulate your exported g-code carefully before use! I won't be liable for any damage you may cause with the generated G-Codes

You may also need to home X and Y before a job, then move to the 0 position after (that usually being the bottom-left of the job, with the tool tip touching the workpiece)


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
