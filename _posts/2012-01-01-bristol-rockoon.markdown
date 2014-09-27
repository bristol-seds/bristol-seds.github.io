---
layout: post
title:  "Bristol Rockoon"
categories: rockoon
asset_path: /assets/posts/bristol-rockoon/
---

{% include old-notice.html %}

## Introduction

Rockoons (Balloon launched rockets) were developed in the 1950's to provide a cheap way to access the space environment for scientific study. These early Rockoons consisted of surplus military rockets from world war two launched from below meteorological high altitude balloons. However with advances in high powered rocketry Rockoons were largely replaced, mostly due to the inherent unreliability and drift of the balloons.

The basic premise behind a rockoon is to use a high altitude balloon to loft the rocket to around 35km, allowing it to launch above the majority of the atmosphere. This can be seen in empirically in graph 1, plotted using data from NASA. This significantly reduces the aerodynamic loading and drag forces on the rocket vehicle, which have the knock-on effect of reducing the amount of fuel needed to reach the Kármán line at 100 km (N.B. The Kármán line is the official edge of space!). A reduced fuel requirement means that either a smaller rocket can be used, or a larger payload can be launched. Basic calculations show that the velocity increment (ΔV) required to reach 100 km from a 35 km launch altitude are as low as 1.1 kms<sup>-1</sup>.

![Flight Profile]({{ "flight-profile.jpg" | prepend: page.asset_path }})
![Atmospheric Density]({{ "atmospheric-density.jpg" | prepend: page.asset_path }})

Because of this a rockoon is the ideal launch system for a student society, and could potentially allow very cheap access to above the Karman line. The aim is therefore to design, build and launch a proof-of-concept Rockoon to around 120km in altitude. At the time of writing, we would be the first student led society to achieve this.

The rockoon has been separated into three main areas:

- The avionics module.
- The Rocket
- The high altitude balloon platform.

## The Avionics module

The Avionics module functions to control in-flight processes, sense and transmit position and store all flight information for post-flight analysis.

The primary in flight processes it will have to deal with are ignition at altitude, supersonic drag system deployment and main drag recovery system deployment. For this it will need to determine its orientation, altitude and velocity.

As most GPS devices cut out above certain altitudes it is necessary to include ‘dead reckoning’ sensors (i.e. accelerometers and gyros) to allow the apogee to be calculated and to give greater accuracy in locating. Due to the extremely low pressures at altitude barometers are unlikely to add much detail but one was included for interest.

Communication will be via amateur radio and an internet dongle. The NTX2 was chosen, with which communication has been reported at distances of over 400km. This transmits data by adjusting the voltage on its TXD pin which in turn changes the transmission frequency. Doing this in a controlled fashion allows 0’s and 1’s (and therefore information) to be transmitted. This is decoded at our end using either our Yaesu FT 790R radio or a computer dongle- we’re currently experimenting with both.

Storage will be done on an SD card.

![The Yaesu FT-790R radio]({{ "yaesu-ft-790r.jpg" | prepend: page.asset_path }})

As the ambient temperature at launch will be approximately 230K and will have dropped to 215K during the ascent it is essential for the unit to regulate its temperature. Many of the components will create their own heat so determining how much extra is required will be one of the aims of the preliminary balloon flights. In the first iteration of the module temperature sensors and heating pads have been included.

Finally, we chose an Mbed as the microcontroller due to its processing power and small size.

![System Diagram]({{ "system-diagram.jpg" | prepend: page.asset_path }})

## The flight-ready module

The components from figure 3 were assembled, programmed and fitted into a custom designed, 3D printed module. This was used for the first launch on the 6th May.

![Assembled Electronics]({{ "assembled-electronics.jpg" | prepend: page.asset_path }})

## The Rocket

This was built to gain experience in model rocketry and test the avionics module during the flight.

The rocket was powered using 4x D12-5 motors, and using a RocketSim model was calculated to achieve an altitude of 275m. This also allowed us to check the stability of the design.

We brought motors for three launches, and with the kind help of FOG rocketry we launched on the 6th of May. The first launch showed stable flight, smooth parachute deployment and good recovery, however a fin came loose when it hit the ground and the INU saturated with launch. It was therefore decided to re-design the fin attachment and some of the programming before the next launches.

![Assembled Rocket]({{ "assembled-rocket.jpg" | prepend: page.asset_path }})

## Launch photos:

![Launch Photos]({{ "launch-photos.jpg" | prepend: page.asset_path }})

## Future rocket work

The main challenges for the rocket system are flight stability, the rocket motor and recovery.

The rocket will be launched at such a high altitude that conventional fins will be ineffective, thus requiring active stabilisation of either the rocket or launch platform. It was eventually decided to attempt active stabilisation of the rocket using jet-tabs - these selectively block small parts of the exhaust thereby altering the overall thrust vector. A more complete explanation can be read in the following paper: Davidovic et al, Jet tab and dome deflector TVC in solid rocket motor mathematical model and test comparison, 2nd ICMEM 2012, p.g.59-63. 

In the interests of safety it was decided to use a hybrid rocket motor. These use propellants in two states of matter, usually a solid fuel and liquid motor. This gives the advantages of a liquid motor (shut-down capability, throttling) while retaining some of the simplicity of solid motors. The fuel grain will be HDPE and the oxidiser NO2. Although these will not give the maximum possible specific impulse they are non-toxic, inert by themselves and easily obtained.

![Diagram of a Hybrid Rocket Motor]({{ "hybrid-engine.jpg" | prepend: page.asset_path }})

An altitude predictor program was written in MATLAB and calculated the following relationships between burn time, thrust and apogee and mass:

![Impulse Relationships]({{ "impulse-relationships.jpg" | prepend: page.asset_path }})

If a 2D ‘slice’ is taken through both graphs where the apogee is equal to 120km the following graphs are produced:

![Thrust Relationships for a 120km Apogee]({{ "thrust-120km-apogee.jpg" | prepend: page.asset_path }})

It can be seen that the lowest launch mass is achieved with the highest possible thrust to burn time ratio. However, as this is increased the launch g force is also increased. In addition the matlab model did not include the guidance system which would favour longer burn times. For these reasons it was decided to limit the g force to 16g, leading to a thrust of 800N and a burn time of 14s.

## Balloon

Three balloon formats were evaluated:

- Single balloon
- 3-arm format- arm out from a central point.
- Triangle format- Triangle with a balloon on each corner.

These were evaluated with 8 different balloon types and the structures were assumed to require balloon separation of 10% diameter and construction of 3/8”, 3/8” & 1/10” thickness aluminium L section. This produced the following graph:

![Graph of launch cost against lift]({{ "cost-against-lift.jpg" | prepend: page.asset_path }})

As the predicted weight of the rocket system is > 1800g it is predicted that a multi-balloon system similar to the dark sky station by JP aerospace will be needed. Our preliminary 3-balloon design was sketched in CAD. The Balloons expand by several times their original diameter, hence the large separation distance. The central triangle is to allow the rocket to launch through the center and will feature a short launch rod to provide some initial stabilization to the rocket. The balloon avionics module will be suspended at the bottom of this and the radar reflector below.

![Launch Platform]({{ "launch-platform.jpg" | prepend: page.asset_path }})

By law the balloon platform is required to include a radar reflector; the CAD sketch and completed model are shown below. The structure was built from aluminium foil stretched over carbon fibre rods.

![Radar Reflector]({{ "radar-reflector.jpg" | prepend: page.asset_path }})