# Model descriptions

The versions form a development sequence: communication infrastructure -> complete mission exchange -> command coordination -> heartbeat extension -> packet-network integration -> heartbeat scope experiments -> main verification candidate. The standalone network is an independently developed input to the integration.

| Version | Description | Contributor |
|---|---|---|
| 01 | [Initial drone coordination](01_drone_coordination.md) | Jason |
| 02 | [Extended mission upload](02_mission_protocol.md) | Jason |
| 03 / 03a | [MAVLink command protocol](03_mavlink_command_protocol.md) | Léo and Gabriel |
| 04 | [Explicit heartbeat communication](04_heartbeat_protocol.md) | Jason |
| 05 / 06 / 06B | [Network integration and simplification](05_06_network_integration.md) | Jason and Faissal |
| 07 | [Heartbeat experiments and ablation](07_heartbeat_experiments_and_ablation.md) | Jason |
| 08 | [Main mission and command model](08_final_mission_command.md) | Jason |
| Standalone | [Network model](STANDALONE_network_model.md), [interface](STANDALONE_network_interface.md) | Faissal |

Contributor identifies the work described by an extension, not ownership of every inherited component.

The [complete model index](../MODEL_VERSION.md) links every XML snapshot and states its status. Versions 01 and 02 retain historical errors and are not clean verified baselines. A version number does not establish verification success.



Shared references: [architecture and modelling decisions](../architecture_and_modeling_decisions.md), [experiments and property guide](../experiments_and_property_guide.md).
