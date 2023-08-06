from time import time
from threading import Lock


class PaceMaker(object):
    '''
        Implementation of https://en.wikipedia.org/wiki/Token_bucket#Algorithm


        Args:
            no_token_sleep_in_seconds: Seconds to nap when there are no tokens to spend. 
                                        Defaults to 1.
    '''
    @classmethod
    def _epoch_in_seconds(self):
        return round(time())

    def __init__(self, no_token_sleep_in_seconds=1):
        self.tokens = 0
        self.rate_per_second = 0
        self.last = self._epoch_in_seconds() #Granularity of seconds is good enough
        self.lock = Lock() # for thread safety
        self.no_token_sleep_in_seconds = no_token_sleep_in_seconds
        
    def set_rate_per_second(self, rate_per_second):
        '''
            Sets the rate/sec
            Args:
                rate_per_second: rate/sec
        '''
        with self.lock:
            self.rate_per_second = rate_per_second
            self.tokens = self.rate_per_second

    def consume(self, tokens=1):
        '''
            Consumes the tokens and returns sleep time

            Args:
                tokens: Number of tokens to consume. Defaults to 1
        '''

        with self.lock: 
            # if the rate_per_second is set to 0, throw exception
            if self.rate_per_second == 0:
                raise Exception('Cannot use the pace maker without setting the heart rate_per_second!!!')

            now = self._epoch_in_seconds()
            time_lapsed = now - self.last
            self.last = now
            # Add rate_per_second x seconds lapsed
            self.tokens += time_lapsed * self.rate_per_second
            # If the bucket is full, discard
            if self.tokens > self.rate_per_second:
                self.tokens = self.rate_per_second

            # subtract the number of tokens being consumed
            self.tokens -= tokens
            if self.tokens > 0:
                # Calculate the pace based on the tokens left
                return round(self.tokens/self.rate_per_second, 3)
            else:
                return self.no_token_sleep_in_seconds

