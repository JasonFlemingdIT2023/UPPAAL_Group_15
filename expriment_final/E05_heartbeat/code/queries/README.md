# Queries

These files are verifier inputs. Suffixes distinguish formula or comment variants of a property.

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
