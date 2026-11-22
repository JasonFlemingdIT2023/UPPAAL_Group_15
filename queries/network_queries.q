// Queries for models/network_model.xml (standalone network test).
// The same 18 queries are embedded in the XML.
// Results are saved in results/network_results.csv. If a line does not say
// otherwise, the query was satisfied in all four saved runs.

// N1: Reachability: a packet can be delivered.
E<> delivered > 0

// N2: Reachability: a packet can be lost. Saved runs: NOT satisfied with LOSS_MODE = 0, satisfied with 1 and 2.
E<> lost > 0

// N3: Reachability: both producers wait while the link is busy, so they really compete for the slot.
E<> (pending[0] && pending[1] && Link.Transmitting)

// N4: Safety: every delivered packet has the fields it was sent with, reaches the right receiver and arrives once.
A[] !integrityError

// N5: Safety: no test packet is delivered twice.
A[] forall (i : packet_id) deliveries[i] <= 1

// N6: Accounting: every packet the link took is in flight, delivered or lost.
A[] (admitted == delivered + lost + (Link.Transmitting ? 1 : 0))

// N7: Accounting: status 2 (delivered) always matches exactly one delivery.
A[] forall (i : packet_id) ((status[i] == 2) == (deliveries[i] == 1))

// N8: Timing: delivery or loss happens between D_MIN and D_MAX after the link takes the packet.
A[] ((Link.Delivered || Link.Lost) imply (Link.x >= D_MIN && Link.x <= D_MAX))

// N9: Timing: the link clock never goes over D_MAX. This restates the invariant, so it only means something together with N10 and N11.
A[] (Link.Transmitting imply Link.x <= D_MAX)

// N10: Liveness: a packet in the link always leaves it (delivered or lost).
Link.Transmitting --> Link.Idle

// N11: The only deadlock is the normal end of the test: both senders done, link idle, all packets delivered or lost.
A[] (deadlock imply (Sender0.Done && Sender1.Done && Link.Idle && delivered + lost == N_PACKETS))

// N12: Reachability: all four packets can be delivered.
E<> (delivered == N_PACKETS)

// N13: Liveness: every run ends with all test packets delivered or lost.
A<> (delivered + lost == N_PACKETS)

// N14: Bounded loss: with K_LOSS = 1 no producer loses both of its packets. Only a real test with LOSS_MODE = 2, trivially true otherwise.
A[] (LOSS_MODE != 2 || !((status[0] == 3 && status[1] == 3) || (status[2] == 3 && status[3] == 3)))

// N15: Reachability: all packets can be lost. Saved runs: satisfied only with LOSS_MODE = 1.
E<> lost == N_PACKETS

// N16: Safety: a packet with status 1 is the one the link is holding right now.
A[] forall (i : packet_id) (status[i] == 1 imply (Link.Transmitting && Link.packet.id == i))

// N17: Safety: a lost packet was never delivered.
A[] forall (i : packet_id) (status[i] == 3 imply deliveries[i] == 0)

// N18: Measure: longest time producer 1 waits before the link takes its packet (admission wait, not transmission time). Saved runs: 9 with D_MAX = 3, 15 with D_MAX = 5.
sup{Sender1.Waiting} : Sender1.wait
