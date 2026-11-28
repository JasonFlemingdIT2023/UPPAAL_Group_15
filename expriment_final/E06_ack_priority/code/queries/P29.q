// P29: ACK pending flags exactly reflect server reply states
A[] ((ackPending[0] == CommandServer(0).Decide) && (ackPending[1] == CommandServer(1).Decide) && (ackPending[2] == CommandServer(2).Decide))
