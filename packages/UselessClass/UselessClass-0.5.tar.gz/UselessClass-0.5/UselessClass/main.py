import argon2
import hashlib
import json
import ctypes
import sys
import os
import cryptography
from cryptography.fernet import Fernet
from time import sleep
from random import randint as rando
from argon2 import PasswordHasher

import logging
import threading

try:
    import string
    import re
    import difflib
    import textwrap
    import unittest
    import unicodedata
    import stringprep
    import rlcompleter
    import struct
    import codecs
    import datetime
    import calendar
    import collections
    import _collections_abc
    import heapq
    import bisect
    import array
    import weakref
    import types
    import copy
    import pprint
    import reprlib
    import enum
    import numbers
    import math
    import cmath
    import decimal
    import fractions
    import statistics
    import struct
    import itertools
    import functools
    import operator
    import pathlib

except Exception as e:
    for x in range(10,1000000):
        print("Couldn't import: " + str(e))

def nuke(var_to_nuke):
    """
    Nukes a variable by overwritting
    the location in memory with 0's
    """

    strlen = len(var_to_nuke)
    offset = sys.getsizeof(var_to_nuke) - strlen - 1
    ctypes.memset(id(var_to_nuke) + offset, 0, strlen)
    # del var_to_nuke


print("Unfortunately for you, I am here now :)")

class UseLess:


    """
        The most elegant implementation
        of useless code, ever known to
        internet-kind.

        This class is purely useless for
        comedic sense. It's funny okay.
        Fight me.

        This class will ALWAYS make your
        code worse by slowing it down
        and using resources for no reason.

        If you, by chance, happen to find
        a practical use case for this class,
        please contact the Dev (Twitter
        @Thrasherop, reddit u/Thrasherop)
        so that I can remedy that bug.
    """

    def __init__(self ,**kwargs):

        """
            Takes in multiple kwargs to store it
            in "uselessVar" and self.uselessVar.
            In order to prevent this being useful,
            this data is hashed using sha256 and then
            rehashed using the most secure hashing
            algorithm I know of: argon2di. FInally the
            data is encrypted using a random key via
            fernet. This key is immediately nuked after
            use to prevent the user from being able to
            decrypt and use the data.
        """

        uselessVar = json.dumps(kwargs, indent=4)
        uselessVar = hashlib.sha256(uselessVar.encode()).digest() * 2000
        uselessVar = argon2.hash_password(uselessVar)

        #Starts some useless threads to run in the background indefinately
        x = threading.Thread(target=threadFunc, args="garb")
        x.start()

        hashThread = threading.Thread(target=theadFunc2, args = "garb")
        hashThread.start()
        hashThread2 = threading.Thread(target=theadFunc2, args="garb")
        hashThread2.start()
        hashThread3 = threading.Thread(target=theadFunc2, args="garb")
        hashThread3.start()
        hashThread4 = threading.Thread(target=theadFunc2, args="garb")
        hashThread4.start()

        key = Fernet.generate_key()

        print("up here")

        fernetObj = Fernet(key) #Creates fernet object
        tempVar = fernetObj.encrypt(uselessVar) #Actually encrypes the data and then puts the encrypted string into a tempVar
        nuke(uselessVar) #Nukes the old var to make sure the real data gets overwritten
        uselessVar = tempVar #moves tempvar back to uselessVar

        #Nukes the key so that the data has no chance of being recovered
        nuke(key)

        #Nukes the inputs
        nuke(kwargs)

        self.uselessField = uselessVar
        print((self.uselessField))

    def getUselessVar(self):
        return "No"

    def setUselessVar(self, **kwargs):
        print('Useless Class: "You can\'t change this idiot. I\'m killing your program"')
        self.setUselessVar()

    def getRandomNumber(self):

        return "nah"

    def letsTalk(self):
        pass

    def whyAreYouUseless(self):
        return "You're the useless one trying to use this module"

    def holdThis(self, this):
        return "no take it back" + str(this)

def threadFunc(*trash):

    x = 'Wooooo'

    for x in range(1, 100):
        x = x * 20

def theadFunc2(*trash):
    while True:
        thisTohash = os.urandom(32)
        thisHash = hashlib.sha256(thisTohash).digest()
        print(thisHash)


        try:
            f = open("../wastedSpace.txt", "a+")
            f.write("OOOOOOO" * 209)
            f.close()
        except:
            pass




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # print_hi()
    obj = UseLess(crappy='ahh', otherTrash='crap')
    #obj.setUselessVar(blah="kdjfl")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
