from random import Random

def create_sequence(
        max_capacity: int, 
        rand_seed: int | None = None
    ) -> list[int]:
    sequence = [i for i in range(max_capacity)]
    if rand_seed is not None:
        prng = Random(rand_seed)
        prng.shuffle(sequence)
    return sequence
