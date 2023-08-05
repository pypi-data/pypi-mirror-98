import gym
from rlberry.seeding import Seeder


class MultiBinary(gym.spaces.MultiBinary, Seeder):
    """

    Inherited from gym.spaces.MultiBinary for compatibility with gym.

    rlberry wraps gym.spaces to make sure the seeding
    mechanism is unified in the library (rlberry.seeding)

    Attributes
    ----------
    rng : numpy.random._generator.Generator
        random number generator provided by rlberry.seeding

    Methods
    -------
    reseed()
        get new random number generator
    """
    def __init__(self, n):
        gym.spaces.MultiBinary.__init__(self, n)
        Seeder.__init__(self)

    def sample(self):
        return self.rng.integers(low=0, high=2,
                                 size=self.n, dtype=self.dtype)
