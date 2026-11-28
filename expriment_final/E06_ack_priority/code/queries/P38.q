// P38: A START ACK is delivered exactly two maximum service windows after admission
E<> (Link.Delivered && Link.packet.kind == PK_ACCEPTED && Link.packet.peer == 0 && Link.packet.cmd == START && cmdAccepted[0][START] && CommandClient(0).x == 2 * D_MAX)
