// P17: ARM accepted after timeout-triggered retry counter increment
E<> (cmdAccepted[0][ARM] && CommandClient(0).current == ARM && CommandClient(0).retries > 0)
