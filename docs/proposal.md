# Project proposals

**Group 15 — Formal Methods for Software Engineering.** Historical proposal reconstruction from the project discussion, organised on 19 November 2026. These are design intentions, not claims of completed verification.

## Selected direction: MAVLink-based multi-drone coordination

**Proposed title:** Modelling and Verification of MAVLink-Based Multi-Drone Mission Coordination in UPPAAL.

**Question:** Under which communication and timing conditions can a ground control station correctly coordinate multiple drones using mission transfer, command handling and heartbeat monitoring?

A GCS prepares assigned missions, obtains transfer confirmation, requests selected operations and interprets replies. Delays, lost messages and concurrent drone sessions can make actual drone state differ from GCS knowledge. Predefined symbolic missions keep detailed flight physics outside scope.

The proposed architecture comprises a fleet supervisor, per-drone mission sender/receiver and command client/server components, heartbeat monitoring, and an explicit shared communication model. Parameterised templates represent multiple drones. MAVLink mission, command and heartbeat documentation provides protocol references; the fleet policy and template decomposition are our modelling choices, not an ISO architecture or a complete drone-show standard.

Formal work includes timed automata, precisely stated assumptions and UPPAAL queries for correct mission evidence, addressing/session separation, command prerequisites, acknowledgement handling, timeout response and progress under stated fault assumptions. Experiments vary link timing, loss and retry settings. Counterexamples should explain failures or uncertainty; successful reachability is not a universal progress guarantee.


## Earlier alternative: audio/video playback synchronisation

**Proposed title:** Modelling and Verification of Timestamp-Based Audio/Video Playback Synchronisation in UPPAAL.

**Question:** Under which arrival, buffering and processing conditions can a playback controller maintain bounded audio/video skew while making progress?

The proposed system has independent audio/video sources, delayed arrivals, buffers and a playback controller. Presentation timestamps associate units with positions on one media timeline; audio and video units need not have one-to-one correspondence. The controller can wait for early video and, in a chosen extension, drop or recover from late video. Timestamp and buffer ranges would be bounded to keep the timed-automata model finite.

A lip-synchronisation case study was related work, not a model to copy. The groups proposed contribution would have been its own buffered controller, assumptions and comparisons. Candidate checks included bounded skew, no presentation before availability, valid buffer use, progress under bounded arrivals, and counterexamples under excessive jitter. Waiting, dropping and recovery policies were proposed comparison points, not implemented results. Codec internals and perceptual-quality guarantees were outside scope.

This alternative was not selected for implementation; no lip-sync model or verification result is claimed in this repository.

## Primary protocol references

- [Mission protocol](https://mavlink.io/en/services/mission.html)
- [Command protocol](https://mavlink.io/en/services/command.html)
- [Heartbeat protocol](https://mavlink.io/en/services/heartbeat.html)
