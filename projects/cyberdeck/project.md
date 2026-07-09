This project aims to use some of the parts from the micro-journal-rev-2.1 by unkyulee. I want to remove the Raspberry Pi Pico (RP2040) and wire the matrix keyboard to the Raspberry Pi Zero 2W.

Goals: 
Reduce the number of parts
Write the code for the Pi Zero 2W

Assumptions:
Assume I have all the parts and do not need to buy anything.

Websites:
The Micro Journal Rev 2.1 
https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1

The 68 key matrx keyboard
https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-2.1/keyboard

The Micro Journal Rev 2.1 build guide and BOM

https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-2.1/build.md

The Micro Journal Rev 2.1 another build guide.
https://github.com/unkyulee/micro-journal/blob/main/micro-journal-rev-2.1/guide.md

Info about the PCB
The PCB layout is optimized specifically for Micro Journal firmware and hardware architecture, with a 68-key matrix configuration and dedicated pinouts for direct integration with Micro Journal mainboards. In the original build the keyboard PCB is wired to the RP2040 - i want to remove that complexity and wire to the Pi Zero 2W. I would like the wires connecting to the Pi Zero 2W to be removable via a screw terminal or some other commercially avalible solution.

Longer term goal:
To redo the case for the The Micro Journal Rev 2.1 so that it is more like the folding case of the https://github.com/unkyulee/micro-journal/tree/main/micro-journal-rev-8

