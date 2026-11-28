// P21: Mission-message loss unreachable
A[] (Link.Lost imply (Link.packet.kind == PK_COMMAND || Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))
