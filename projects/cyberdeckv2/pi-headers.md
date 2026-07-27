



I do remember! It was for your Micro Journal Rev 2.1 project where you were wiring the keyboard matrix directly to the Pi Zero 2 W.

What you're looking for is usually called a GPIO screw terminal breakout or terminal block HAT.

My favorite option is a compact terminal breakout like this:

Mini Terminal Breakout Board for Raspberry Pi
$16.05
•
The Pi Hut
It plugs directly onto the 40-pin header and gives you a screw terminal for every GPIO pin. No more Dupont wires pulling loose.

Another nice option, if you don't mind a slightly larger board, is:


GPIO Screw Terminal HAT
$17.39 · The Pi Hut
It has:

Screw terminals for every GPIO

Printed pin labels

GPIO status LEDs, which are surprisingly handy when debugging keyboard matrices and GPIO code. 

For your keyboard project...
I'd actually recommend something a little different:

Pi Zero 2 W

40-pin stacking header

Mini GPIO screw terminal breakout

That gives you secure screw terminals and keeps the top of the Pi accessible if you later decide to add another HAT or custom board.

Since I know how you work, I have one more suggestion that I think you'll really like. Instead of a generic breakout, we could design a custom carrier board for the Pi Zero 2 W. It would include:

Screw terminals for every GPIO

Clearly silk-screened GPIO numbers

A power switch

Reset button

Status LEDs

I²C/Qwiic connector

JST battery connector (optional)

Mounting holes that match your Micro Journal enclosure

It's essentially a "development motherboard" for the Pi Zero that you could reuse across all of your projects. Given how many Pi Zero and keyboard projects you've built, I think you'd get far more value from a custom board than buying several different breakout adapters. I think it'd make a great KiCad project once you've had some fun with the ESP32 boards.


Show me

    40-pin stacking header
* Mini GPIO screw terminal breakout

I think this is exactly what you want for the Micro Journal project.

Option 1 (My favorite): 40-pin Stacking Header
This plugs into the Pi and gives you another full-height GPIO header on top, so you can stack another board or breakout.

Geekworm 2×20 40-Pin GPIO Stacking Header Kit
$7.00
•
Geekworm
Why I like it:

Gives you extra clearance above the Pi.

Lets you add another HAT or breakout later.

Inexpensive.

Option 2 (What I think you were remembering): Mini GPIO Screw Terminal Breakout
This plugs directly onto the GPIO header and gives you a screw terminal for every pin.


Mini Terminal Breakout Board for Raspberry Pi
$16.05 · The Pi Hut
This is great because:

Every GPIO has its own screw terminal.

No more Dupont wires pulling out.

Pin numbers are clearly labeled.

Very compact.

Option 3 (Even nicer)
This one has LEDs that show the state of every GPIO while still giving you screw terminals.


GPIO Screw Terminal HAT with LEDs
$13.74 · The Pi Hut Business
The LEDs are surprisingly useful when debugging keyboard matrices, encoders, and switches.

If it were my build...
For your Pi Zero 2 W keyboard computer, I'd use:

✅ Pi Zero 2 W

✅ 40-pin stacking header

✅ Mini GPIO screw terminal breakout

That combination lets you:

Secure every keyboard matrix wire with screw terminals.

Remove and reconnect wiring easily while developing.

Still have expansion options later if you decide to add another board.

One thought, though: after following your Micro Journal project over the past few weeks, I'm starting to think you're outgrowing generic breakout boards. A custom carrier PCB that plugs onto the Pi Zero 2 W might be a better long-term solution. It could have:

Screw terminals for just the GPIOs you actually use.

Labels matching your keyboard matrix (instead of BCM numbers).

Connectors for the encoders.

A power switch and reset button.

Optional I²C/Qwiic connectors for sensors or displays.

It would make wiring cleaner, reduce mistakes, and fit your enclosure perfectly. I think that would be a fun KiCad project once you've gotten comfortable with the ESP32 ecosystem too.


Ok interesting 

I think it could actually be a really enjoyable project for you because it combines several of your interests: keyboard PCBs, Raspberry Pi, and learning KiCad without being overwhelmingly complex.

Here's what I have in mind:

             ┌─────────────────────────┐
             │     Pi Zero 2 W         │
             └─────────┬───────────────┘
                       │ 40-pin header
      ┌────────────────┴─────────────────┐
      │      Micro Journal Carrier        │
      │                                   │
      │ [Screw terminals]  Rows           │
      │ [Screw terminals]  Columns        │
      │                                   │
      │ [JST] Left Encoder                │
      │ [JST] Right Encoder               │
      │                                   │
      │ Power LED                         │
      │ User LED                          │
      │ Reset Button                      │
      │                                   │
      │ I²C/Qwiic Connector               │
      │ Optional RTC                      │
      └───────────────────────────────────┘
Some things we could do that commercial breakouts don't:

Label the terminals as R0, R1, R2... C0, C1, C2... instead of GPIO 17, GPIO 22, etc., matching your keyboard firmware.

Put the screw terminals exactly where the wires enter your enclosure.

Add JST connectors for the encoders so they're plug-and-play.

Include mounting holes that line up with your Micro Journal case.

Break out a few spare GPIOs for future sensors or LEDs.

Since you've already designed keyboard PCBs, this is actually a fairly approachable board. It's mostly connectors and traces rather than complex circuitry.

And here's another idea that I think fits your style: instead of making it specific to the Micro Journal, make it a Pi Zero Embedded Baseboard.

It could become your standard development platform whenever you use a Pi Zero 2 W:

Keyboard projects

Cyberdecks

Home automation controllers

Small robotics

Test fixtures

Embedded Linux experiments

You'd build one good board once and reuse it for years.

When you're ready, we could make it a polished open-source project with:

KiCad source files

3D-printable enclosure

BOM with DigiKey/LCSC part numbers

Assembly guide

GPIO pinout documentation

That feels like the kind of project that would be genuinely useful beyond a single build, and it would give you another solid open-source hardware design to add to your collection.


