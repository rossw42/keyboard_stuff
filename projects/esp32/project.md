# ESP32 Learning Lab — Project Plan

**Status:** Planning — reviewing initial ChatGPT brainstorm, deciding what to order and which first project to build.
**Source material:** `esp32.md` (ChatGPT board-selection chat), `pi-headers.md` (related but separate Pi Zero 2 W carrier-board idea — tracked as its own future project, not part of this ESP32 order).

---

## 1. Where this came from

`esp32.md` is a ChatGPT conversation about which ESP32 dev boards to buy to start learning the ESP32 ecosystem. The chat recommended a small "lab" of board variants (S3, C3, C6, CAM) rather than one board, plus a grab-bag of sensors/accessories, and suggested several project ideas loosely tied to your existing keyboard/Pi/homelab interests.

This doc reviews that advice, fact-checks/annotates it against what's actually true about these boards, and turns it into (a) a concrete order list and (b) a ranked project shortlist that connects to things you're already building (Vial/QMK keyboards, the switch tester, Pi Zero cyberdeck work, homelab).

---

## 2. Review of the ChatGPT recommendation

Overall the advice is **reasonable and not wrong**, but it's generic and glosses over a few gotchas that matter in practice. Verdict per board:

| Board | Verdict | Notes / corrections |
|---|---|---|
| **ESP32-S3 DevKit, N16R8 (16MB flash / 8MB PSRAM)** | ✅ Good primary pick | Real native USB (USB-OTG peripheral) — but it's only wired to **specific GPIO pins (19/20)**. Cheap clone boards sometimes only expose a UART-to-USB bridge on the single USB-C port and never route the native-USB pins to a connector. **When ordering, check the listing/photos for a board with two USB ports** (often labeled "USB" and "UART") — that's the tell that native USB HID/MIDI is actually usable, which is the whole reason to pick S3 over C3 for keyboard/HID work. Also double check the listing explicitly says **N16R8** — a lot of "ESP32-S3 DevKit" listings are actually N8R2 or N4R2 (less flash/PSRAM) at the same price point. |
| **ESP32-C3 SuperMini** | ✅ Good, cheap, useful | Legit tiny BLE/Wi-Fi board with native USB via a **single** USB-C port (this one *does* have native USB with no separate UART bridge — simpler than the S3 in that respect). Early production batches had a marginal onboard antenna/3.3V regulator; buy from a listing with recent reviews. |
| **ESP32-C6 DevKit** | ✅ Worth the one unit | Real Wi-Fi 6 + 802.15.4 (Zigbee/Thread/Matter) + BLE5 chip — genuinely the "future" chip if smart-home/Matter is ever of interest. Prefer the **official Espressif DevKitC-1/DevKitM-1** over random clones for this one specifically, since radio certification/antenna matching matters more for 802.15.4 mesh use than for simple Wi-Fi. |
| **ESP32-CAM (optional)** | ✅ Fine, but flag the gotcha | Fun board, cheap, but the classic AI-Thinker ESP32-CAM has **no onboard USB port at all** — you need a separate 5V FTDI/CP2102 USB-TTL adapter to flash it, plus a jumper-wire dance (GPIO0 to GND while resetting) to enter flash mode. The original chat didn't mention this — added to the order list below. |
| Original WROOM / ESP8266 / P4 (skip) | ✅ Agreed, skip for now | No disagreement — WROOM is strictly worse than S3/C3 for the same money today, and the P4 ecosystem is still too immature for a first project. |

### Important correction the chat didn't make: this is *not* QMK/ZMK territory

Because your recent work has been QMK (vial-qmk) and ZMK, it's worth being explicit: **neither QMK nor ZMK supports the ESP32.** QMK has no ESP32 architecture target, and ZMK is Zephyr-based — while Zephyr itself has ESP32 support, no ZMK board definitions exist for it and it isn't a supported target. So an ESP32 "keyboard controller" project means either:
- **Arduino/ESP-IDF native USB HID** (S3/C3 only, via `USB.h`/TinyUSB — you write the HID report descriptor and matrix scan yourself), or
- **BLE HID** via NimBLE-Arduino or ESP-IDF's Bluedroid/NimBLE stack (works on any BLE-capable ESP32, including C3/C6), or
- **Bluepad32** or similar community libraries that already implement HID host/device logic if you don't want to hand-roll it.

This is a genuinely different (and good) skill to build alongside QMK/ZMK — lower-level than QMK's abstraction, closer to "how does keyboard firmware actually talk USB HID" — but go in expecting to write more of the plumbing yourself.

---

## 3. Recommended order (refined BOM)

See [`esp32_bom.csv`](./esp32_bom.csv) for the full order list in the same format as the other BOMs in this repo (`BOM/dumbpad_bom.csv`). Summary:

| Board/Part | Qty | Why |
|---|---|---|
| ESP32-S3 DevKit (confirmed **N16R8**, dual USB ports) | 2 | Primary board — native USB HID, plenty of RAM for real projects |
| ESP32-C3 SuperMini | 5 | Cheap, tiny, great for BLE HID / sensors / battery projects |
| ESP32-C6 DevKit (official Espressif) | 1 | Future-proofing — Wi-Fi 6 / Thread / Matter / Zigbee |
| ESP32-CAM (AI-Thinker) | 1 | Optional fun project (camera) |
| FTDI/CP2102 USB-TTL adapter (5V) | 1 | **Required if buying the CAM** — it has no onboard USB |
| 0.96" I2C OLED (SSD1306, 4-pin) | 2 | Status displays |
| EC11 rotary encoder | 5 | You already use these (DumbPad) — reuse spares if you have them |
| BME280 breakout | 3 | Environmental monitor project |
| WS2812B LEDs | 1 pack/strip | You already have RGB keyboard experience — reuse stock if possible |
| MPU6050 IMU | 1 | Optional — only if a motion project is planned soon |
| Verified data-capable USB-C cables | 4 | Cheap charge-only cables are the #1 "board won't flash" support issue |
| Breadboards + jumper wires | a few | Standard prototyping |
| USB logic analyzer (8ch, sigrok-compatible) | 1 | You already do embedded debugging — genuinely useful here too |

Estimated total: **~$60–90** depending on vendor (a bit above the chat's $40–70 estimate once the FTDI adapter and verified-data cables are added — those are real requirements, not optional).

---

## 4. Project shortlist (ranked)

Picking a **first project** that plugs into things you're already doing, rather than a generic tutorial, will make the learning stick faster. Ranked by fit + learning value + low friction:

1. **BLE HID macro pad on an ESP32-C3** — directly comparable to your Vial/QMK macro pad work, but hand-rolled: matrix scan → BLE HID reports. Best "aha" project for understanding what QMK/ZMK normally hide from you. Natural next step after this: port the switch-tester's macro-string idea to a tiny BLE test rig.
2. **Homelab/Proxmox status display** — ESP32-S3 or C3 + 0.96" OLED, polls a small HTTP/Prometheus endpoint on your Proxmox box and shows CPU/RAM/container status. Good first real Wi-Fi + HTTP client + display project, low hardware complexity (no matrix, no HID).
3. **Woodworking shop environmental monitor** — ESP32-C3 + BME280 + OLED (or just Wi-Fi + a dashboard/MQTT), battery-friendly. Good second project once Wi-Fi basics from #2 are solid.
4. **Cities: Skylines 2 companion display** — same shape as #2 (poll a local stat source, render on OLED) but more fun/game-flavored; could reuse the exact same firmware skeleton as the Proxmox display with a different data source.
5. **ESP32-CAM timelapse/bird-feeder camera** — optional, fun, but lowest priority since it needs the extra FTDI adapter and is the least connected to your other work.
6. **ESP32-C6 Matter/Zigbee experiment** — lowest priority for now; worth doing once you actually want a smart-home device, not just to "learn C6."

**Suggested order to tackle them:** #2 (Wi-Fi + OLED basics, no HID complexity) → #1 (BLE HID, the most novel/valuable skill) → #3 or #4 (reuse #2's skeleton) → #5/#6 whenever curiosity strikes.

---

## 5. Next steps

- [ ] Review/adjust the BOM in `esp32_bom.csv` (quantities, vendor choice) and place the order
- [ ] Confirm the S3 DevKit listing explicitly states N16R8 and shows two USB ports before buying
- [ ] While waiting on parts: skim ESP-IDF vs Arduino framework decision (Arduino is faster to start; ESP-IDF gives more control over USB HID/BLE stacks — no need to decide until boards arrive)
- [ ] Build project #2 (homelab status display) first as the "hello world" once an S3 or C3 + OLED arrive
- [ ] Revisit `pi-headers.md` separately — that's a standalone Pi Zero 2 W carrier-board PCB idea (screw-terminal GPIO breakout for the Micro Journal / cyberdeck work), unrelated to this ESP32 order; worth its own project doc once the ESP32 lab is up and running

## 6. Open questions

1. **Vendor preference** — Amazon (fastest, US-based, easiest returns) vs AliExpress (cheaper, especially for the C3 SuperMini/CAM, but 2–4 week shipping) vs Adafruit/SparkFun (most reliable QA, priciest). Default assumption below is Amazon-first for anything needed soon, AliExpress acceptable for the cheap boards if you don't mind the wait.
2. **Budget ceiling** — is ~$60–90 the right range, or is there a harder cap?
3. **Framework preference** — Arduino (faster onboarding, huge library ecosystem) vs raw ESP-IDF (more control, steeper learning curve, needed eventually for custom USB HID descriptors)? No need to decide before ordering, but worth deciding before writing the first line of firmware.
