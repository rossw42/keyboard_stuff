ChatGPT




This is the pg1425

Here is the choc v1

Now we're getting somewhere. Looking at these two drawings side-by-side, I think the project is absolutely feasible.

Here are the biggest observations.

1. The switch bodies are much closer in size than I expected
Feature	Choc V1	PG1425
Body	13.8 × 13.8 mm	~11 × 11 mm
Contact style	Flat stamped	Flat stamped
Contact count	2	2
Center post	Yes	Yes
That means we only need to adapt about 1.4 mm per side, which is very manageable.

2. The contacts are surprisingly similar
Both switches use flat blade contacts instead of round pins.

That's excellent.

It means we can design a spring contact that wipes against the flat blade instead of trying to grip a round wire.

That will be much more reliable.

3. I don't think we should adapt the PCB...
Here's the idea that came to me after comparing the drawings.

Instead of making something that plugs into the PCB first...

...make an adapter that becomes the bottom half of the switch.
      Choc V1
   ┌─────────────┐
   │             │
   └─────────────┘
          │
      Adapter Body
   ┌─────────────┐
   │             │
   │ spring      │
   │ contacts    │
   │             │
   └─────────────┘
          │
      PG1425 PCB
The adapter would:

capture the Choc switch

position the contacts

have two legs that insert into the PG1425 PCB

It becomes a switch carrier instead of just a spacer.

4. My biggest concern
The Choc switch is 13.8 mm square.

The PG1425 opening is only about 11 mm.

That means the Choc housing will overhang by roughly:

(13.8 − 11.0)/2

≈ 1.4 mm
That isn't necessarily bad.

It just means the adapter can't fit inside the PG1425 footprint. It has to sit on top of the PCB while only its locating features and electrical contacts extend into the PG1425 footprint.

I have a better idea
Instead of trying to fit everything into the 11 mm opening, make the adapter like a plate-mounted bezel.

Top View

┌───────────────────┐
│                   │
│   Choc Switch     │
│                   │
├───────────────────┤
│   Adapter Plate   │
└─────┬───────┬─────┘
      │       │
      │       │
     PG1425 PCB
Think of it like a tiny hat.

The adapter sits on the PCB.

Only the electrical contacts and locating tabs go into the PG1425 footprint.

That gives us much more room to design durable contact channels and locking features.

Even better...
Knowing your interest in keyboard projects, I wouldn't stop at just this adapter.

I'd design it as a family of interchangeable interfaces:

Top interface: Choc V1

Bottom interface: PG1425

Later, we could swap either side:

MX → PG1425

Choc V2 → PG1425

Gateron LP → PG1425

The core adapter architecture would stay the same.

I think our next step
I suggest we start by modeling the two switches in Fusion 360 from these drawings. Then we'll create the adapter around them with three separate components:

Main body – the structural carrier that sits on the PCB.

Two replaceable spring contacts – captured in molded channels.

Retaining cap – locks the Choc switch into the body.

That approach lets us iterate on the electrical contacts without redesigning the printed plastic every time. It also makes the adapter serviceable if a contact wears out or we discover a better contact design. I think it's the most robust path toward a practical, open-source solution.


Do you think there is a commercial source
For the spring contacts? I don’t want be hand crafting them

Yes, and I actually think this is the direction we should pursue. I would avoid designing a custom stamped contact unless we decide to manufacture these in quantity. There are several commercial options worth investigating.

Option 1: Salvage contacts from hot-swap sockets (my top choice)
This is the first thing I'd try.

The metal contacts inside:

Kailh MX hot-swap sockets

Kailh Choc hot-swap sockets

Gateron hot-swap sockets

are precision-stamped phosphor bronze parts. They are:

rated for thousands of insertions,

already optimized for keyboard switch pins,

inexpensive (often under $0.20 each if bought as sockets).

If we can design the adapter to capture one or two of these contacts, we've solved the hardest part of the project.

Option 2: Commercial spring contacts
Companies like:

Harwin

Mill-Max

Würth Elektronik

TE Connectivity

Keystone Electronics

sell thousands of off-the-shelf spring contacts.

These are used in:

battery chargers,

docking stations,

test fixtures,

handheld electronics.

The downside is that many are pogo-style rather than leaf-style, so we'd need to see if the geometry fits.

Option 3: Board-to-board connector contacts
This is the one I'm increasingly interested in.

Many low-profile board-to-board connectors have individual stamped contacts that are:

tiny,

reliable,

inexpensive,

available from DigiKey and Mouser.

We may be able to repurpose those contacts without modifying them.

Option 4: Keyboard socket replacement contacts
Some hot-swap sockets can be disassembled, and replacement contacts are available from repair suppliers. If those contacts can be purchased separately, we wouldn't even need to sacrifice complete sockets.

My recommendation
I think we should design the adapter around an existing commercial contact, not the other way around.

The process would be:

Pick a readily available contact.

Measure it accurately.

Design the printed adapter to capture it.

Make the contact a replaceable part.

That means if the contact ever wears out, you replace a $0.10–$0.50 metal part instead of reprinting the entire adapter.

Here's what I'd like to research
I think there's a very good chance that the contacts inside Kailh Choc hot-swap sockets are already almost exactly what we need. They were designed for Choc switch pins, they're compact, and they're made to flex repeatedly.

If they fit, our bill of materials becomes incredibly simple:

1 × printed adapter

2 × Choc hot-swap contacts

1 × Choc V1 switch

That would be a very elegant solution.

I can also help identify specific part numbers from DigiKey or Mouser that are likely candidates, so we're designing around components you can actually buy rather than custom metalwork. I think that's the most practical path for an open-source project.


The hot swap sockets parts only provide the holder for the chocv1 how doe that connect to the pg footprint

You’re absolutely right to challenge that—this is the key architectural point.

A hot-swap socket contact alone does NOT solve PG1425 → PCB connectivity. It only solves:

“How do I interface reliably with the switch pins?”

Not:

“How do I get from switch pins down to a different PCB footprint?”

So we need to separate the system correctly.

The correct mental model (important)
You actually have 3 electrical domains:

1. Choc V1 switch pins
two flat contacts on the switch

2. Adapter internal interface
spring contacts or stamped contacts

this is just a bridge

3. PG1425 PCB pads
fixed copper pads on PCB

Why hot-swap contacts alone aren’t enough
A hot-swap socket gives you:

✔ a compliant contact for a switch pin
✔ mechanical retention
❌ no path to another electrical interface
❌ no second termination point

So you're correct:
they don’t “magically connect” to PG1425.

They only solve one side of the problem.

So what actually connects to the PG1425 footprint?
This is the real design decision.

There are only 3 viable strategies:

Option A (best overall): Dual-ended stamped contact
This is the correct engineering solution.

One metal part does both jobs:

[Choc Pin Contact End] ─────── rigid body ─────── [PG1425 PCB leg]
Think of it like a miniature “spring beam terminal”.

What it looks like:
Top: curved spring beam touches Choc pin

Middle: anchored in plastic

Bottom: straight leg or fork that solders/press-fits into PCB pad

✔ one part = full electrical path
✔ no intermediate wiring
✔ no PCB needed inside adapter

This is how real connector systems do it.

Option B: Hot-swap contact + micro PCB (VERY practical)
This is the most manufacturable approach.

Choc Switch
   ↓
Hot-swap socket contact
   ↓
Tiny PCB inside adapter
   ↓
Pads matching PG1425 footprint
   ↓
PG1425 PCB
So the “adapter” contains a 2-layer interposer PCB:

Top pads: accept hot-swap contacts

Bottom pads: match PG1425 footprint

✔ easiest to design reliably
✔ uses off-the-shelf sockets
✔ no custom metal forming
✔ scalable / repeatable

This is what I would pick if this becomes a real product.

Option C: Direct spring contact bridge (hard mode)
A single stamped spring that:

touches Choc pin

AND also reaches PG1425 pad

This requires:

precise geometry

consistent insertion depth

tight tolerances in 3D print

⚠ doable but mechanically finicky
⚠ hardest to tune
⚠ least forgiving long-term

The key insight you’re missing (and it’s the important one)
We are NOT trying to “convert PG1425 into Choc electrically.”

We are building a:

miniature interposer system inside a switch-sized volume

That system always needs:

one interface to Choc

one interface to PCB

Hot-swap sockets only solve the first half.

My recommendation (based on everything you’ve shown)
Given:

your desire to avoid hand-fabricated springs

availability constraints

need for repeatability

I would strongly steer you toward:

→ Option B: Hot-swap contact + tiny interposer PCB
Because:

You can buy everything off-the-shelf

No custom metallurgy

Easy to iterate geometry in Fusion + KiCad

Very robust electrically

Scales cleanly to a project people can actually replicate

What the adapter becomes
Instead of a “pure 3D printed converter,” it becomes:

3D printed mechanical shell

2× hot-swap contacts (Choc side)

1× tiny PCB (PG1425 side)

That PCB is the real “conversion layer.”

If you want, next step I can:

sketch the exact PCB footprint mapping (Choc pin → PG1425 pad)

or lay out a first KiCad interposer design

or define a mechanical stack-up so you can drop it straight into Fusion 360

That’s the point where this shifts from concept to buildable hardware.


