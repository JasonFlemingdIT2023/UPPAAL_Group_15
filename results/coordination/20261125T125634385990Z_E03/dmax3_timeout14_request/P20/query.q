// P20: Command acknowledgement loss reachable
E<> (Link.Lost && (Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))
