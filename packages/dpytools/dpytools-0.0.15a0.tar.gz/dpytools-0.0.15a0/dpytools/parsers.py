# -*- coding: utf-8 -*-
"""
This module holds parsers and converters to use with user input
Functions here can be used as type hints which discord.py will use as
custom converters or they can be used as regular functions.
Example:
    ```
    @bot.command()
    async def timedelta(ctx, time: dpytools.parsers.parse_time):
        await ctx.send(f"time delta is: {time}")
    ```
    above command will be called like this: `!timedelta 2h30m`
    and it will send a message with "time delta is: 2:30:00"

    This way you dont have to manually parse the time string to a timedelta object.
    the parameter "time" will be of type timedelta.
"""
import re
from collections import ChainMap
from datetime import timedelta
from typing import Dict



class InvalidTimeString(Exception):
    pass


def to_upper(string: str) -> str:
    """
    Converts :string: to upper case. Intended to be used as argument converter.
    Args:
        string: string to format

    Returns:
        string to upper case
    """
    return string.upper()


def to_lower(string: str) -> str:
    """
    Converts :string: to lower case. Intended to be used as argument converter.
    Args:
        string: string to format

    Returns:
        string to lower case
    """
    return string.lower()



def parse_time(string: str) -> timedelta:
    """
    Converts a string with format <number>[s|m|h|d] to a timedelta object
    <number> must be convertible to float.
    Uses regex to match groups and consumes all groups into one timedelta.

    Units:
        s: second
        m: minute
        h: hour
        d: day
        w: weeks

    Args:
        string: with format <number>[s|m|h|d].
            parse_time("2h") == timedelta(hours=2)

    Returns:
        timedelta

    Raises:
        ValueError: if string number cannot be converted to float
        InvalidTimeString: if string isn't in the valid form.

    """
    units = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks'
    }

    time_pattern = r"(\d+\.?\d?[s|m|h|d|w]{1})\s?"

    def parse(time_string: str) -> Dict:

        unit = time_string[-1]

        amount = float(time_string[:-1])
        return {units[unit]: amount}

    if matched := re.findall(time_pattern, string, flags=re.I):
        time_dict = dict(ChainMap(*[parse(d) for d in matched]))
        return timedelta(**time_dict)
    else:
        raise InvalidTimeString("Invalid string format. Time must be in the form <number>[s|m|h|d|w].")
