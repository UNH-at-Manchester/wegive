"""
Module for tags. Includes the tags list, and methods to deal with tags from
the database.
NOTE: It would probably be a good idea to put at least the names of the tags
in the database.
"""

import csv

tags = ["Religious", "Animals", "Education", "Public Opinion", "Other",]

class Echo():
    """
    Class for a bogus "file-like object" that doesn't buffer anything.
    """
    def write(self, data):
        return data


def write_csv(data):
    """
    Usage: write_csv(data)
    Converts a list to a CSV string.

    Parameters:
    list data: list of data to convert.

    Returns:
    A CSV string of the converted data.
    """
    if type(data) != list:
        raise ValueError("write_csv in tags.py:20: data must be a list.")
    nobuffer = Echo()
    writer = csv.writer(nobuffer)
    return writer.writerow(data)


def read_csv(data):
    """
    Usage: read_csv(data)
    Converts a CSV string to a list.
    Uses the accumulator pattern, likely not very compliant.

    Parameters:
    string data: string CSV data.

    Returns:
    A list of the converted data.
    """
    if type(data) != str:
        raise ValueError("read_csv in tags.py:31: data must be a string")
    
    res = [""]
    ignore = False
    idx = 0

    for ch in data:
        if ch in ("\"", "'"):
            ignore = not ignore
            continue
        if not ignore:
            if ch == ",":
                print(res)
                print(ch)
                res += [""]
                idx += 1
                continue
            if ch == "\r":
                continue
            if ch == "\n":
                break
        res[idx] += ch
    return res
