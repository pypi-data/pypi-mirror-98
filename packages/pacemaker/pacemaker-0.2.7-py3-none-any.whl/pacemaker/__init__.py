# coding:utf-8
"""
Function decoration for pacing calls to an old man
This module provides function decorators which can be used to wrap a
function such that it will be paced to given rate.
For examples and full documentation see the README at
https://github.com/mkeshav/pace-maker
"""
from ._decorator import pace_me

__all__ = [
    'pace_me'
]

__version__ = '0.2.7'
