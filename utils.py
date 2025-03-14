from random import Random

def create_sequence(
        sequence_length: int, 
        max_capacity: int, 
        rand_seed: int | None = None
    ) -> list[int]:
    sequence = [i for i in range(max_capacity)]
    if rand_seed is not None:
        prng = Random(rand_seed)
        prng.shuffle(sequence)
    return sequence[:sequence_length]
