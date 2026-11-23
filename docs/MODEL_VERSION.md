# Model version index

Current main candidate: [08_final_version.xml](../models/08_final_version.xml). Historical and experimental models remain available.

| Model | Purpose / status | Description | Contributor |
|---|---|---|---|
| [00_baseline.xml](../models/00_baseline.xml) | Empty historical placeholder; not a runnable model | Earlier FL proposal is archived | Not recorded |
| [01_drone_coordination.xml](../models/01_drone_coordination.xml) | Initial infrastructure; saved declaration/channel errors | [Description](model_descriptions/01_drone_coordination.md) | Jason |
| [02_drone_extended_missionProtocol.xml](../models/02_drone_extended_missionProtocol.xml) | Mission-item loop and completion barrier. saved sequence bug | [Description](model_descriptions/02_mission_protocol.md) | Jason |
| [03_mavlink_protocol.xml](../models/03_mavlink_protocol.xml) | Team command extension: ARM/START, outcomes, retries | [Original description](model_descriptions/03_mavlink_command_protocol.md) | Léo and Gabriel|
| [03a_mavlink_protocol_base.xml](../models/03a_mavlink_protocol_base.xml) | Retained command baseline | [Original description](model_descriptions/03_mavlink_command_protocol.md) | Léo and Gabriel |
| [04_heartbeat_protocol_v1.xml](../models/04_heartbeat_protocol_v1.xml) | explicit periodic heartbeat extension | [Description](model_descriptions/04_heartbeat_protocol.md) | Jason |
| [05_network_integration_part1.xml](../models/05_network_integration_part1.xml) | packet interface and inactive TxAdapter milestone | [Integration history](model_descriptions/05_06_network_integration.md) | Jason |
| [06_network_integration_adapter_state_explosion.xml](../models/06_network_integration_adapter_state_explosion.xml) | active adapter/mailbox experiment | [Integration history](model_descriptions/05_06_network_integration.md) | Jason and Faissal |
| [06B_simple_integration.xml](../models/06B_simple_integration.xml) | simplified direct packet network; continuous heartbeat | [Integration history](model_descriptions/05_06_network_integration.md) | Jason and faissal |
| [07_heartbeat_drop_after_done.xml](../models/07_heartbeat_drop_after_done.xml) | finite-preparation heartbeat experiment | [Ablation notes](model_descriptions/07_heartbeat_experiments_and_ablation.md) | Jason |
| [08_final_version.xml](../models/08_final_version.xml) | Main candidate: mission + command + packet network; heartbeat inactive; ACK fix | [Final description](model_descriptions/08_final_mission_command.md) | Jason |
| [STANDALONE_network_model.xml](../models/STANDALONE_network_model.xml) | independent network component and finite test harness | [Original description](model_descriptions/STANDALONE_network_model.md), [interface](model_descriptions/STANDALONE_network_interface.md) | Faissal |
