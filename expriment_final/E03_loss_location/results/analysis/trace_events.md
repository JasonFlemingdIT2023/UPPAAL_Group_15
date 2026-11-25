# E03 diagnostic witness events

Times below are concrete model times relative to drone 0 first command admission. They are witness values, not bounds.

## request_P10

Raw log: [UPPAAL trace](../traces/dmax3_timeout14_request_P10.txt)

| Relative time | Event |
|---:|---|
| 0 | CMD0 admitted / ACK timer reset |
| 3 | CMD0 lost |
| 14 | Timeout; retry pending |
| 14 | CMD0 admitted / ACK timer reset |
| 17 | CMD0 lost |
| 28 | Timeout; retry pending |
| 28 | CMD0 admitted / ACK timer reset |
| 40 | ARM0 executes; ACK0 admitted |
| 42 | Confirmation FAILED |

Final locations: `( Supervisor.Arming Sender0.Done Sender1.Done Sender2.Done Drone0.Uploaded Drone1.Uploaded Drone2.Uploaded Link.Transmitting CommandClient(0).Failed CommandClient(1).WaitAck CommandClient(2).Idle CommandServer(0).Idle CommandServer(1).Idle CommandServer(2).Idle )`
Final armed[0]=1, cmdFailed[0][ARM]=1.

## request_P18

Raw log: [UPPAAL trace](../traces/dmax3_timeout14_request_P18.txt)

| Relative time | Event |
|---:|---|
| 0 | CMD0 admitted / ACK timer reset |
| 3 | CMD0 lost |
| 14 | Timeout; retry pending |
| 14 | CMD0 admitted / ACK timer reset |
| 15 | CMD0 lost |
| 28 | Timeout; retry pending |
| 28 | CMD0 admitted / ACK timer reset |
| 29 | CMD0 lost |
| 42 | Confirmation FAILED |
| 42 | Supervisor aborts coordination |

Final locations: `( Supervisor.Aborted Sender0.Done Sender1.Done Sender2.Done Drone0.Uploaded Drone1.Uploaded Drone2.Uploaded Link.Idle CommandClient(0).Failed CommandClient(1).Idle CommandClient(2).Idle CommandServer(0).Idle CommandServer(1).Idle CommandServer(2).Idle )`
Final armed[0]=0, cmdFailed[0][ARM]=1.

## reply_P10

Raw log: [UPPAAL trace](../traces/dmax3_timeout14_reply_P10.txt)

| Relative time | Event |
|---:|---|
| 0 | CMD0 admitted / ACK timer reset |
| 14 | Timeout; retry pending |
| 14 | CMD0 admitted / ACK timer reset |
| 17 | ARM0 executes; ACK0 admitted |
| 18 | ACK0 lost |
| 28 | Timeout; retry pending |
| 28 | CMD0 admitted / ACK timer reset |
| 31 | ARM0 executes; ACK0 admitted |
| 32 | ACK0 lost |
| 42 | Confirmation FAILED |

Final locations: `( Supervisor.Arming Sender0.Done Sender1.Done Sender2.Done Drone0.Uploaded Drone1.Uploaded Drone2.Uploaded Link.Idle CommandClient(0).Failed CommandClient(1).Idle CommandClient(2).Idle CommandServer(0).Idle CommandServer(1).Idle CommandServer(2).Idle )`
Final armed[0]=1, cmdFailed[0][ARM]=1.

## reply_P11

Raw log: [UPPAAL trace](../traces/dmax3_timeout14_reply_P11.txt)

| Relative time | Event |
|---:|---|
| 0 | CMD0 admitted / ACK timer reset |
| 14 | Timeout; retry pending |
| 14 | CMD0 admitted / ACK timer reset |
| 28 | Timeout; retry pending |
| 28 | CMD0 admitted / ACK timer reset |
| 42 | Confirmation FAILED |

Final locations: `( Supervisor.Arming Sender0.Done Sender1.Done Sender2.Done Drone0.Uploaded Drone1.Uploaded Drone2.Uploaded Link.Transmitting CommandClient(0).Failed CommandClient(1).WaitAck CommandClient(2).WaitAck CommandServer(0).Decide CommandServer(1).Idle CommandServer(2).Idle )`
Final armed[0]=0, cmdFailed[0][ARM]=1.
