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

## [P09.q](P09.q)

```text
E<> (CommandClient(0).retries > 0)
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
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)))
```

## [P14_3.q](P14_3.q)

```text
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)))
```

## [P14_4.q](P14_4.q)

```text
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)) && (uploadDone[3] imply (missionInstalled[3] && Drone3.receivedCount == MISSION_SIZE)))
```

## [P15.q](P15.q)

```text
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]
```

## [P16.q](P16.q)

```text
Supervisor.Prepared --> (Supervisor.Done || Supervisor.Aborted)
```

## [P17.q](P17.q)

```text
E<> (cmdAccepted[0][ARM] && CommandClient(0).current == ARM && CommandClient(0).retries > 0)
```

## [P23.q](P23.q)

```text
E<> (CommandClient(0).retries > 0)
```

## [P23_2.q](P23_2.q)

```text
E<> (CommandClient(0).retries > 0 || CommandClient(1).retries > 0)
```

## [P23_3.q](P23_3.q)

```text
E<> (CommandClient(0).retries > 0 || CommandClient(1).retries > 0 || CommandClient(2).retries > 0)
```

## [P23_4.q](P23_4.q)

```text
E<> (CommandClient(0).retries > 0 || CommandClient(1).retries > 0 || CommandClient(2).retries > 0 || CommandClient(3).retries > 0)
```

