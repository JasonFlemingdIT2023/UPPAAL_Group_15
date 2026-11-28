// P39: Drone 0 dispatched command eventually completes
CommandClient(0).Sending --> CommandClient(0).Idle

// P40: Drone 1 dispatched command eventually completes
CommandClient(1).Sending --> CommandClient(1).Idle

// P41: Drone 2 dispatched command eventually completes
CommandClient(2).Sending --> CommandClient(2).Idle

// P42: Arming phase eventually completes
Supervisor.Arming --> Supervisor.Starting

// P43: Starting phase eventually completes
Supervisor.Starting --> Supervisor.Done

// P44: Prepared phase eventually starts arming
Supervisor.Prepared --> Supervisor.Arming
