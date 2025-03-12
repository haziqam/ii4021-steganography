from random import Random

def create_sequence(sequence_length: int, rand_seed: int | None = None):
    sequence = [i for i in range(sequence_length)]
    if rand_seed is not None:
        prng = Random(rand_seed)
        for i in range(sequence_length):
            target = prng.randint(0, sequence_length-1)
            temp = sequence[i]
            sequence[i] = sequence[target]
            sequence[target] = temp
    return sequence
