#!/usr/bin/env python3
"""Helper Program to convert the UUID from Windows style to network byte order

Author: Thomas Schlieter
Date created: 2020/07/14
Date last modified: 2021/01/31

Copyright (C) 2020 Thomas Schlieter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import re
from socket import ntohl, ntohs
import argparse


# third group must start with a 4
# fourth group must start with 8, 9, a or b
# 00000000-0000-4000-a000-000000000000

UUID_REGEX = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z"


def uuid2guid(uuid):
    """Convert a uuid string to a guid string

    Returns:
        str: UUID in network byte order

    >>> uuid2guid('6ac1033b-8dd8-4cdb-81ec-b324c077a757')
    '3b03c16a-d88d-db4c-81ec-b324c077a757'"""

    bytefields = map(lambda h: int(h, base=16), uuid.split('-'))
    convert_functions = (ntohl, ntohs, ntohs, int, int)

    guid_fields = [f(v) for f, v in zip(convert_functions, bytefields)]

    guid = '-'.join(map('{:x}'.format, guid_fields))
    return guid


def uuid_regex_type(uuid_string, pat=re.compile(UUID_REGEX, re.I)):
    """Check if arg_value is in correct format.
    
    Raises:
        argparse.ArgumentTypeError:  If uuid not in correct format

    Returns:
        str: UUID when correct format
    """
    
    if not pat.match(uuid_string):
        raise argparse.ArgumentTypeError('Not valid UUID Format')
    return uuid_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert UUID to GUID')
    parser.add_argument('uuid', help='The UUID String in format ' + UUID_REGEX + \
                ' for example: 6ac1033b-8dd8-4cdb-81ec-b324c077a757', type=uuid_regex_type)
    args = parser.parse_args()
    guid = uuid2guid(args.uuid)
    print(guid)


