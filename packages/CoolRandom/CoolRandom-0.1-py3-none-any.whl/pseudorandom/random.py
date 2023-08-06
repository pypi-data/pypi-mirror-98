from time import time

class _Random:

    def __init__(self):

        self.seed()

    def seed(self, seed=None):

        if seed:
            t1 = seed * 3
            t2 = seed * 5
            t3 = seed * 11

            s1 = t1 * t2
            s2 = (t1 + t3) * t2
            s3 = (t1 * t3) / t2
            
        else:
            _now = time()
            _str_now = str(_now).replace(".", "")[::-1]

            s1 = int(_str_now[:4])
            s2 = int(_str_now[4:8])
            s3 = int(_str_now[7:11])

        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def random(self):

        self.s1 = (171 * self.s1) % 30269
        self.s2 = (172 * self.s2) % 30307
        self.s3 = (170 * self.s3) % 30323

        return (self.s1 / 30269.0 + self.s2 / 30307.0 + self.s3 / 30323.0) % 1

    def randint(self, a, b):

        r1 = self.random()

        return round((b - a) * r1) + a

    def choice(self, seq):

        upper = len(seq) - 1
        lower = 0

        index = self.randint(lower, upper)

        return seq[index]

    def shuffle(self, seq):

        upper = len(seq) - 1
        lower = 0

        for i in range(len(seq)):

            j = self.randint(lower, upper)

            seq[i], seq[j] = seq[j], seq[i]
