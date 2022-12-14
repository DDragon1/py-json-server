from array import array
from enum import Enum
from random import uniform,choices,randint,choice
from string import *
from time import time
from datetime import datetime
from functools import partial
import uuid

GEO_DECIMAL_POINT = 6

def randomInt(min: int = 0, max: int = 100) -> int:
    return randint(min,max)

def randomFloat(min: float = 0, max: float = 100, decPlace : int = 2) -> float :
    return round(uniform(min,max), decPlace)

def randomString(size:int = 8, chars=printable) -> str:
    if (chars in globals().keys() and isinstance(globals().get(chars), str)):
        chars = (globals().get(chars))
    return ''.join(choices(chars, k=size))

def randomGEO(minX: float = 32.0, maxX: float = 33.5, minY: float = 35.0, maxY: float = 36.5) -> tuple[float, float]:
    return (randomFloat(minX, maxX, GEO_DECIMAL_POINT), randomFloat(minY, maxY, GEO_DECIMAL_POINT))

def randomTimestamp(delta: int = 4) -> datetime:
    k = datetime.now().timestamp() - randint(0,delta) # get time as seconds
    return datetime.fromtimestamp(k).isoformat() # return time as timestamp

def randomUUID():
    return str(uuid.uuid4())

def randomEnum(enums: array = []):
    return choice(enums)

def insertObject(obj = None):
    return obj

def keepValue(curr_value):
    return curr_value

def relativeInt(curr_value : int, min: int = 0, max: int = 100):
    return curr_value + randomInt(min, max)

def relativeFloat(curr_value: float, min: float = 0, max: float = 100, decPlace : int = 2):
    return curr_value + randomFloat(min, max)

def relativeGEO(curr_value: tuple[float, float], minX: float = 0.0, maxX: float = 0.5, minY: float = 0.0, maxY: float = 0.5):
    return (relativeFloat(curr_value[0], minX, maxX, GEO_DECIMAL_POINT) , relativeFloat(curr_value[1], minY, maxY, GEO_DECIMAL_POINT))
class RandomsEnums(Enum):
    randomString = partial(randomString)
    randomGEO = partial(randomGEO)
    randomFloat = partial(randomFloat)
    randomInt = partial(randomInt)
    randomTimestamp = partial(randomTimestamp)
    randomEnum = partial(randomEnum)
    insertObject = partial(insertObject)
    randomUUID = partial(randomUUID)

    def __call__(self, args = {}):
        if (args == None):
            args = {}
        return self.value(**args)

class RelativeRandomsEnums(Enum):
    keepValue = partial(keepValue)
    relativeInt = partial(relativeInt)
    relativeFloat = partial(relativeFloat)
    relativeGEO = partial(relativeGEO)

    def __call__(self, curr_value, args = {}):
        if (args == None):
            args = {}
        return self.value(curr_value, **args)