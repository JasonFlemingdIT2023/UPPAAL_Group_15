# 查询 / Queries

以下文件用于 verifyta，编号后缀表示同一性质的不同公式或注释版本。 / These files are verifier inputs. Suffixes distinguish formula or comment variants of a property.

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

## [P08.q](P08.q)

```text
E<> CommandClient(0).Failed
```

## [P10.q](P10.q)

```text
E<> (cmdFailed[0][ARM] && armed[0])
```

## [P11.q](P11.q)

```text
E<> (cmdFailed[0][ARM] && !armed[0])
```

## [P12.q](P12.q)

```text
E<> Link.Lost
```

## [P13.q](P13.q)

```text
A[] (Supervisor.Done imply forall (i : drone_id) started[i])
```

## [P14.q](P14.q)

```text
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)))
```

## [P14_2.q](P14_2.q)

```text
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)))
```

## [P15.q](P15.q)

```text
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]
```

## [P16.q](P16.q)

```text
Supervisor.Prepared --> (Supervisor.Done || Supervisor.Aborted)
```

## [P21.q](P21.q)

```text
A[] (Link.Lost imply (Link.packet.kind == PK_COMMAND || Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))
```

## [P25.q](P25.q)

```text
Supervisor.Prepared --> Supervisor.Done
```

## [P26.q](P26.q)

```text
A<> Supervisor.Done
```

## [P27.q](P27.q)

```text
A[] Link.lossCount <= LOSS_BUDGET
```

## [P28.q](P28.q)

```text
E<> (Supervisor.Done && Link.lossCount == LOSS_BUDGET)
```

