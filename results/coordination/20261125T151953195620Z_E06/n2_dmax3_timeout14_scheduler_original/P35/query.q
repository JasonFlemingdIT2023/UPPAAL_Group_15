// P35: No drone exhausts command retries
A[] forall (i : drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])
