#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class Bot():
    # Please write your code here.
    def __init__(self, command):
        self.command = command['command']
        self.data = command['data']

    def generate_hash(self):
        lst = [self.command, self.data]
        s = 0
        for string in lst:
            ascii_transformed = self.connected_ascii(string)
            if len(ascii_transformed) > 21:
                sn = self.scientificNotation(int(ascii_transformed))
                ascii_transformed = ''.join(re.split(r'e\+|\.', sn)[1:])
            s += int(ascii_transformed)

        self.hash = '%x' % s

    # first step
    # string = 'color' -> return '99111108111114'
    def connected_ascii(self, string):
        return ''.join([str(ord(char)) for char in list(string)])

    # Convert the number into scientific notation with 16 digits after "."
    # If power of e is greater than 20, get the number between "." and "e"
    # Else return the number itself
    def scientificNotation(self, num):
        data = "%.16e" % num
        result = data if (int(data.split("e+")[1]) > 20) else num
        return result
