// P18: ARM still absent at a quiescent aborted outcome
E<> (Supervisor.Aborted && Link.Idle && CommandClient(0).Failed && CommandClient(1).Idle && CommandClient(2).Idle && CommandServer(0).Idle && CommandServer(1).Idle && CommandServer(2).Idle && !armed[0] && cmdFailed[0][ARM])
