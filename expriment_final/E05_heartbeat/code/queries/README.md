# 查询 / Queries

以下文件用于 verifyta，编号后缀表示同一性质的不同公式或注释版本。 / These files are verifier inputs. Suffixes distinguish formula or comment variants of a property.

## [P01.q](P01.q)

```text
E<> Supervisor.Done
```

## [P03.q](P03.q)

```text
A[] forall (i : drone_id) (started[i] imply armed[i])
```

## [P08.q](P08.q)

```text
E<> CommandClient(0).Failed
```

## [P24.q](P24.q)

```text
E<> forall (i : drone_id) heartbeatSeen[i]
```

