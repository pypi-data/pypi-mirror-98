from .random import _Random

_random = _Random()

seed = _random.seed
random = _random.random
randint = _random.randint
choice = _random.choice
shuffle = _random.shuffle