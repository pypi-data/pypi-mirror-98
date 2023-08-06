# coding:utf-8

from .pacemaker import PaceMaker
import time
from functools import wraps
import logging
import sys

def pace_me(data_gen, rate_per_second, logger='pacemaker', **data_gen_kwargs):
    """
        Returns decorator for backoff and retry triggered by predicate.
        Args:
            data_gen: A generator yielding data that the target function needs
            rate_per_second: Rate.
            number_of_tokens_per_call: Number of tokens to consume per target function call
            logger: Name of logger or Logger object to log to. Defaults to
            'pacemaker'.
            data_gen_kwargs: Any additional keyword args specified will be
-            passed to data_gen function.
    """
    def decorate(target):
        logger_ = logger
        if isinstance(logger_, str):
            logger_ = logging.getLogger(logger_)
            logger_.setLevel(logging.INFO)
            logger_.addHandler(logging.StreamHandler(sys.stdout))

        @wraps(target)
        def wrapper(**target_kwargs):
            p = PaceMaker()
            p.set_rate_per_second(rate_per_second)
            for d in data_gen(**data_gen_kwargs):
                target(d, **target_kwargs)
                # Do not import sleep directly as we want to monkey patch this during tests.
                nap = p.consume()
                if(logger_ is not None):
                    logger_.info('Napping for {0} seconds'.format(nap))
                time.sleep(nap)
        
        return wrapper

    return decorate
