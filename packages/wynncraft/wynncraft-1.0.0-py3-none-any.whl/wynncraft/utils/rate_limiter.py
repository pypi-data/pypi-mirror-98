import time

import utils.constants


class RateLimiter:
    def __init__(self):
        self.rl_reset = 0
        self.rl_remaining = 0

    def limit(self):
        if utils.constants.RL_ENABLE:
            if self.rl_reset > self.rl_remaining:
                time.sleep(self.rl_reset - self.rl_remaining)

    def update(self, info):
        self.rl_reset = int(info["RateLimit-Reset"])
        self.rl_remaining = int(info["RateLimit-Remaining"])
