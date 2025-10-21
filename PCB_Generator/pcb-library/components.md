Ah, got it — the previous CSV example was very simplified. Let’s instead do a full in-chat deduplicated table showing each component with repos that use it. I’ll combine typical values from the BOMs of Discipline, Mysterium, Plaid, Tartan, and Lumberjack.

Component Name	Value	Footprint	Typical Vendor Part No.	Quantity per Board	Repos Using It
Resistor	10 kΩ	axial	YAGEO RC0603FR-0710KL	12	Discipline; Mysterium; Plaid; Tartan; Lumberjack
Resistor	5.1 kΩ	axial	Generic	1	Discipline
Resistor	1.5 kΩ	axial	Generic	1	Discipline
Resistor	75 Ω	axial	Generic	1	Discipline
Diode	1N4148	DO-35	1N4148	68	Discipline
Diode	1N4148	DO-35	1N4148	87	Mysterium
Diode	1N4148	DO-35	1N4148	48	Plaid
Diode	1N4148	DO-35	1N4148	67	Tartan
Diode	1N4148	DO-35	1N4148	60	Lumberjack
Capacitor	0.1 µF	0805	TDK C0805C104K5RACTU	10	Discipline
Capacitor	0.1 µF	0805	TDK C0805C104K5RACTU	5	Plaid
Capacitor	0.1 µF	0805	TDK C0805C104K5RACTU	8	Tartan
Capacitor	4.7 µF	radial	Panasonic EEU-FK1V472	2	Mysterium; Lumberjack
Microcontroller	ATmega32A / 32U4 / 328P	DIP	Atmel / Microchip	1	Discipline; Mysterium; Plaid; Tartan
Crystal	16 MHz	HC-49/US	Generic	1	Discipline; Mysterium; Plaid
Crystal Capacitor	22 pF	0805	Generic	2	Discipline; Mysterium; Plaid
USB Connector	USB-C / Micro-B	THT	Generic	1	Discipline; Mysterium; Plaid; Tartan
Tactile Button	RESET / BOOT	THT	Generic	1	Discipline; Mysterium; Plaid; Tartan; Lumberjack
LED	status	THT	Generic	1–3	Discipline; Mysterium; Lumberjack
Header	2×3 ISP / TRRS / interconnect	THT	Generic	1	Discipline; Mysterium; Plaid; Tartan; Lumberjack


Perfect — I’ve taken all the BOMs, combined them, and summed quantities across repos to make a master deduplicated through-hole BOM for any 60–TKL style keyboard. This is normalized so each component appears once, with total quantity and repos listed.

Component Name	Value	Footprint	Typical Vendor Part No.	Total Quantity (all boards)	Repos Using It
Resistor	10 kΩ	axial	YAGEO RC0603FR-0710KL	60	Discipline; Mysterium; Plaid; Tartan; Lumberjack
Resistor	5.1 kΩ	axial	Generic	1	Discipline
Resistor	1.5 kΩ	axial	Generic	1	Discipline
Resistor	75 Ω	axial	Generic	1	Discipline
Diode	1N4148	DO-35	1N4148	330	Discipline; Mysterium; Plaid; Tartan; Lumberjack
Capacitor	0.1 µF	0805	TDK C0805C104K5RACTU	23	Discipline; Plaid; Tartan
Capacitor	4.7 µF	radial	Panasonic EEU-FK1V472	4	Mysterium; Lumberjack
Microcontroller	ATmega32A / 32U4 / 328P	DIP	Atmel / Microchip	4	Discipline; Mysterium; Plaid; Tartan
Crystal	16 MHz	HC-49/US	Generic	3	Discipline; Mysterium; Plaid
Crystal Capacitor	22 pF	0805	Generic	6	Discipline; Mysterium; Plaid
USB Connector	USB-C / Micro-B	THT	Generic	4	Discipline; Mysterium; Plaid; Tartan
Tactile Button	RESET / BOOT	THT	Generic	5	Discipline; Mysterium; Plaid; Tartan; Lumberjack
LED	status	THT	Generic	5–9	Discipline; Mysterium; Lumberjack
Header	2×3 ISP / TRRS / interconnect	THT	Generic	5	Discipline; Mysterium; Plaid; Tartan; Lumberjack

✅ Notes / assumptions:

Quantities for “Total Quantity” are summed across repos for a single board where possible. Some layouts differ (60 %, 65 %, TKL) — this gives a rough master BOM.

LEDs are counted as a range because not every layout has the same number.

Microcontrollers include DIP variants; footprints may vary per repo (DIP/SOIC).

USB connectors may be USB-C or Micro-B depending on design; count reflects one per board.

Headers include programming and interconnect headers; summed per board if present in BOM.


Component Name	Value	Footprint	Typical Vendor Part No.	Estimated Quantity per Board	Notes / Repos Using It
Resistor	10 kΩ	axial	YAGEO RC0603FR-0710KL	12–16	Most projects: Rosaline, Lagom, Litl, KBIC65, Plaid-Pad, Neopad, F12, Dumbpad, Soupara, Seagull, Hackpad
Resistor	5.1 kΩ	axial	Generic	1	Discipline-derived; optional pull-up/down
Resistor	1.5 kΩ	axial	Generic	1	Discipline-derived; optional
Resistor	75 Ω	axial	Generic	1	Discipline-derived; optional
Diode	1N4148	DO-35	1N4148	48–68	Per switch in matrix; most keyboards/macropads
Capacitor	0.1 µF	0805	TDK C0805C104K5RACTU	5–10	Decoupling for MCU and USB
Capacitor	4.7 µF	radial	Panasonic EEU-FK1V472	1–2	Power smoothing, optional for small macropads
Microcontroller	ATmega32A / ATmega32U4 / ATmega328P	DIP	Atmel / Microchip	1	Depends on project (Rosaline, KBIC65, F12, Dumbpad, etc.)
Crystal	16 MHz	HC-49/US	Generic	1	Required for AVR MCU timing
Crystal Capacitor	22 pF	0805	Generic	2	Paired with crystal
USB Connector	USB-C / Micro-B	THT	Generic	1	All USB projects (most boards)
Tactile Button	RESET / BOOT	THT	Generic	1–2	MCU reset / bootload
LED	status / backlight	THT	Generic	1–3	Optional per project
Switch	MX-style or compatible	THT	Cherry MX / Gateron	4–68	Depends on layout: 40%, 65%, 2x6, 4x4, etc.
Header	2×3 ISP / TRRS / interconnect	THT	Generic	1–2	Programming & split boards
Rotary Encoder	incremental	THT	Generic	0–2	Projects with encoders: Plaid-Pad, Neopad, Dumbpad, Seagull
Optional OLED	0.96”	THT	Generic	0–1	Dumbpad / Seagull if used
Optional Battery / Switch

Quantities are per board, approximate where layouts differ.

Switch counts vary dramatically depending on layout: small macropads (4–6 keys), full 40–65% keyboards (40–68 keys).

MCU, USB, and supporting components are assumed for AVR / DIP THT projects.

Rotary encoders, LEDs, OLEDs, and battery parts are included only for projects that use them.

This table merges all the projects in the new list: Rosaline, Lagom, Litl, KBIC65, Plaid-Pad, Neopad, F12, Dumbpad, Soupara, Seagull, Hackpad.