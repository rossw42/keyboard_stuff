Yesterday 9:18 PM
Thinking about Learing more about the esp32 .  Which ones should I get

Given the kinds of projects you've been working on—QMK keyboards, nice!nano, Raspberry Pi, ZMK, custom PCBs, and controller projects—I would skip the absolute cheapest ESP32 boards and build a small "lab" of a few different variants. That gives you room to experiment without buying dozens of boards.

My recommended starter kit
1. ESP32-S3 DevKit (Get 2 of these)
5

This would be my first choice.

Why:

USB-C
Native USB (acts as keyboard, mouse, MIDI, etc.)
Plenty of RAM
AI/ML instructions
Excellent Arduino and ESP-IDF support
Great for HID projects

Perfect for:

Custom macro pads
Keyboard controllers
Bluetooth devices
Wi-Fi dashboards
Touch interfaces
MIDI controllers

I'd specifically look for:

ESP32-S3 N16R8
16 MB Flash
8 MB PSRAM

The extra memory is worth the few extra dollars.

2. ESP32-C3 SuperMini (Get 3–5)
4

These are tiny and inexpensive.

Great for:

Sensors
Home automation
BLE devices
Small keyboard accessories
Battery-powered projects

Advantages:

Very low power
USB-C
Native USB
Usually around $3–6 each
3. ESP32-C6 (Get 1)
4

This is the "future-looking" board.

Adds:

Wi-Fi 6
Thread
Matter
Zigbee
BLE 5

Worth learning if you're interested in smart home projects.

4. ESP32-CAM (Optional)

Just because they're fun.

Projects:

Timelapse cameras
Bird feeder camera
Security camera
AI vision experiments
QR code scanner
Things I'd skip for now
Original ESP32-WROOM (older design unless it's extremely cheap)
ESP8266 (still useful, but I'd start with ESP32 today)
ESP32-P4 (interesting but still early for most hobbyists)
Accessories

I'd also pick up:

USB-C data cables (some cheap cables are charge-only)
Breadboard
Jumper wires
Logic analyzer (you've been doing enough embedded work that one becomes very useful)
A few small OLED displays (0.96" I²C)
Addressable RGB LEDs (WS2812B—you already have experience with these)
MPU6050 or similar IMU
Rotary encoders
Environmental sensors like the BME280
Projects that fit your interests

Based on what we've discussed before, here are some projects I think you'd genuinely enjoy:

A Wi-Fi-enabled QMK macro pad that updates layers or macros over a web interface.
A keyboard switch tester that logs actuation statistics over Wi-Fi.
A small status display for your Proxmox or Docker servers.
A wireless BNK16-style macro pad using BLE HID.
A photo workflow controller that integrates with your Canon R8 editing process.
A companion display for Cities: Skylines 2 showing system stats or game-related controls.
A Wi-Fi-enabled environmental monitor for your woodworking shop.
If I were placing one order today

I'd buy:

2 × ESP32-S3 N16R8 DevKit
5 × ESP32-C3 SuperMini
1 × ESP32-C6 DevKit
2 × 0.96" OLED displays
5 × rotary encoders
5 × BME280 sensor modules
A pack of WS2812B LEDs

That collection would cost roughly $40–70 depending on where you buy it and would cover nearly every ESP32 project you're likely to tackle over the next year.

I also think you'll enjoy the ESP32 ecosystem because it feels like a natural step beyond Pico/QMK development: you get Wi-Fi, Bluetooth, USB HID, and plenty of GPIO while still programming in C/C++ (or even MicroPython or Rust if you want to explore those later).