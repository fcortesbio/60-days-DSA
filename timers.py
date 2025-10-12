#!/usr/bin/env python3
import timeit
import time
import random

randint_timer = timeit.timeit(
    stmt='random.randint(0,1)',
    setup='import random',
    number=100000000,
    timer=time.perf_counter)

print(randint_timer)

random_timer = timeit.timeit(
    stmt='random.random()',
    setup='import random',
    number=100000000,
    timer=time.perf_counter)

print(random_timer)