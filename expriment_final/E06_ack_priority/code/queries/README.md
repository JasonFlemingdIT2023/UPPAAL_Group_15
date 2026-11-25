# 查询 / Queries

以下文件用于 verifyta，编号后缀表示同一性质的不同公式或注释版本。 / These files are verifier inputs. Suffixes distinguish formula or comment variants of a property.

## [ContinuationDone.q](ContinuationDone.q)

```text
A<> Supervisor.Done
```

## [P01.q](P01.q)

```text
E<> Supervisor.Done
```

## [P02.q](P02.q)

```text
A[] forall (i : drone_id) (armed[i] imply missionInstalled[i])
```

## [P03.q](P03.q)

```text
A[] forall (i : drone_id) (started[i] imply armed[i])
```

## [P04.q](P04.q)

```text
A[] (Supervisor.Done imply forall (i : drone_id) cmdAccepted[i][START])
```

## [P05.q](P05.q)

```text
A[] (deadlock imply (Supervisor.Done || Supervisor.Aborted))
```

## [P06.q](P06.q)

```text
Link.Transmitting --> Link.Idle
```

## [P07.q](P07.q)

```text
A[] ((Link.Delivered || Link.Lost) imply (Link.t >= D_MIN && Link.t <= D_MAX))
```

## [P13.q](P13.q)

```text
A[] (Supervisor.Done imply forall (i : drone_id) started[i])
```

## [P14.q](P14.q)

```text
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)))
```

## [P15.q](P15.q)

```text
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]
```

## [P24.q](P24.q)

```text
E<> forall (i : drone_id) heartbeatSeen[i]
```

## [P25.q](P25.q)

```text
Supervisor.Prepared --> Supervisor.Done
```

## [P29.q](P29.q)

```text
A[] ((ackPending[0] == CommandServer(0).Decide) && (ackPending[1] == CommandServer(1).Decide) && (ackPending[2] == CommandServer(2).Decide))
```

## [P29_2.q](P29_2.q)

```text
A[] ((ackPending[0] == CommandServer(0).Decide))
```

## [P29_3.q](P29_3.q)

```text
A[] ((ackPending[0] == CommandServer(0).Decide) && (ackPending[1] == CommandServer(1).Decide))
```

## [P30.q](P30.q)

```text
HBSender(0).Pending --> HBSender(0).Waiting
```

## [P31.q](P31.q)

```text
HBSender(1).Pending --> HBSender(1).Waiting
```

## [P32.q](P32.q)

```text
HBSender(2).Pending --> HBSender(2).Waiting
```

## [P34.q](P34.q)

```text
E<> (Supervisor.Done && forall (i : drone_id) heartbeatSeen[i])
```

## [P35.q](P35.q)

```text
A[] forall (i : drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])
```

## [P36.q](P36.q)

```text
A[] (CommandClient(0).retries == 0 && CommandClient(1).retries == 0 && CommandClient(2).retries == 0)
```

## [P36_2.q](P36_2.q)

```text
A[] (CommandClient(0).retries == 0)
```

## [P36_3.q](P36_3.q)

```text
A[] (CommandClient(0).retries == 0 && CommandClient(1).retries == 0)
```

## [P37.q](P37.q)

```text
A[] ((CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX) && (CommandClient(1).WaitAck imply CommandClient(1).x <= 2 * D_MAX) && (CommandClient(2).WaitAck imply CommandClient(2).x <= 2 * D_MAX))
```

## [P37_2.q](P37_2.q)

```text
A[] ((CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX))
```

## [P37_3.q](P37_3.q)

```text
A[] ((CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX) && (CommandClient(1).WaitAck imply CommandClient(1).x <= 2 * D_MAX))
```

## [P38.q](P38.q)

```text
E<> (Link.Delivered && Link.packet.kind == PK_ACCEPTED && Link.packet.peer == 0 && Link.packet.cmd == START && cmdAccepted[0][START] && CommandClient(0).x == 2 * D_MAX)
```

## [P39.q](P39.q)

```text
CommandClient(0).Sending --> CommandClient(0).Idle
```

## [P40.q](P40.q)

```text
CommandClient(1).Sending --> CommandClient(1).Idle
```

## [P41.q](P41.q)

```text
CommandClient(2).Sending --> CommandClient(2).Idle
```

## [P42.q](P42.q)

```text
Supervisor.Arming --> Supervisor.Starting
```

## [P43.q](P43.q)

```text
Supervisor.Starting --> Supervisor.Done
```

## [P44.q](P44.q)

```text
Supervisor.Prepared --> Supervisor.Arming
```

## [PreparedBoundary.q](PreparedBoundary.q)

```text
A[] (Supervisor.Prepared imply (forall (i : drone_id) (uploadDone[i] && missionInstalled[i] && !armed[i] && !started[i] && !ackPending[i] && !Supervisor.armSent[i] && !Supervisor.startSent[i] && forall (c : cmd_id) (!cmdAccepted[i][c] && !cmdDenied[i][c] && !cmdFailed[i][c])) && (Link.Idle || Link.Delivered || (Link.Transmitting && Link.packet.kind == PK_HEARTBEAT)) && Sender0.Done && Drone0.Uploaded && CommandClient(0).Idle && CommandClient(0).current == ARM && CommandClient(0).retries == 0 && CommandServer(0).Idle && CommandServer(0).current == ARM && ((HBSender(0).Waiting && HBSender(0).period <= HB_PERIOD) || (HBSender(0).Pending && HBSender(0).period >= HB_PERIOD)) && Sender1.Done && Drone1.Uploaded && CommandClient(1).Idle && CommandClient(1).current == ARM && CommandClient(1).retries == 0 && CommandServer(1).Idle && CommandServer(1).current == ARM && ((HBSender(1).Waiting && HBSender(1).period <= HB_PERIOD) || (HBSender(1).Pending && HBSender(1).period >= HB_PERIOD)) && Sender2.Done && Drone2.Uploaded && CommandClient(2).Idle && CommandClient(2).current == ARM && CommandClient(2).retries == 0 && CommandServer(2).Idle && CommandServer(2).current == ARM && ((HBSender(2).Waiting && HBSender(2).period <= HB_PERIOD) || (HBSender(2).Pending && HBSender(2).period >= HB_PERIOD))))
```

## [bound.q](bound.q)

```text
A[] ((completionStarted && !Supervisor.Done) imply completionAge <= 120)
```

