from numbers import Number
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import StringHelper, LogHelper
from python_helper.api.src.helper import ObjectHelperHelper

GENERATOR_CLASS_NAME = 'generator'
UNKNOWN_OBJECT_CLASS_NAME = c.UNKNOWN.lower()

METADATA_NAME = 'metadata'

NATIVE_CLASS_LIST = [
    bool,
    int,
    str,
    float,
    bytes,
    type(ObjectHelperHelper.generatorInstance())
]

COLLECTION_CLASS_LIST = [
    list,
    dict,
    tuple,
    set
]

def equals(
    expected,
    toAssert,
    ignoreKeyList = None,
    ignoreCharactereList = None,
    visitedIdInstances = None,
    muteLogs = True
) :
    if isNone(expected) or isNone(toAssert) :
        return expected is None and toAssert is None
    if isNativeClass(type(expected)) :
        return expected == toAssert
    if isNone(visitedIdInstances) :
        visitedIdInstances = []
    if isDictionary(expected) and isDictionary(toAssert) :
        innerIgnoreCharactereList = [c.SPACE]
        if isNotNone(ignoreCharactereList) :
            innerIgnoreCharactereList += ignoreCharactereList
        filteredResponse = StringHelper.filterJson(
            str(sortIt(filterIgnoreKeyList(expected,ignoreKeyList))),
            extraCharacterList=innerIgnoreCharactereList
        )
        filteredExpectedResponse = StringHelper.filterJson(
            str(sortIt(filterIgnoreKeyList(toAssert,ignoreKeyList))),
            extraCharacterList=innerIgnoreCharactereList
        )
        return filteredResponse == filteredExpectedResponse
    elif isCollection(expected) and isCollection(toAssert) :
        areEquals = True
        try :
            for a, b in zip(expected, toAssert) :
                areEquals = equals(
                    a,
                    b,
                    ignoreKeyList = ignoreKeyList,
                    ignoreCharactereList = ignoreCharactereList,
                    visitedIdInstances = visitedIdInstances,
                    muteLogs = muteLogs
                )
                if not areEquals :
                    break
            return areEquals
        except Exception as exception :
            areEquals = False
            LogHelper.log(equals, f'Different arguments in {expected} and {toAssert}. Returning "{areEquals}" by default', exception=exception)
    else :
        if isNotNone(toAssert) and id(toAssert) not in visitedIdInstances :
            areEquals = True
            try :
                if not muteLogs :
                    LogHelper.prettyPython(equals, f'expected', expected, logLevel = LogHelper.DEBUG, condition=not muteLogs)
                    LogHelper.prettyPython(equals, f'toAssert', toAssert, logLevel = LogHelper.DEBUG, condition=not muteLogs)
                areEquals = True and ObjectHelperHelper.leftEqual(expected, toAssert, visitedIdInstances, muteLogs=muteLogs) and ObjectHelperHelper.leftEqual(toAssert, expected, visitedIdInstances, muteLogs=muteLogs)
            except Exception as exception :
                areEquals = False
                LogHelper.log(equals, f'Different arguments in {expected} and {toAssert}. Returning "{areEquals}" by default', exception=exception)
            visitedIdInstances.append(id(toAssert))
            return areEquals
        else :
             return True
def sortIt(thing) :
    if isDictionary(thing) :
        sortedDictionary = {}
        for key in getSortedCollection(thing) :
            sortedDictionary[key] = sortIt(thing[key])
        return sortedDictionary
    elif isCollection(thing) :
        newCollection = []
        for innerValue in thing :
            newCollection.append(sortIt(innerValue))
        return getSortedCollection(newCollection)
    else :
        return thing

def getSortedCollection(thing) :
    return thing if isNotCollection(thing) else sorted(
        thing,
        key=lambda x: (
            x is not None, c.NOTHING if isinstance(x, Number) else type(x).__name__, x
        )
    )

def filterIgnoreKeyList(objectAsDictionary,ignoreKeyList):
    if isDictionary(objectAsDictionary) and isNotNone(ignoreKeyList) :
        filteredObjectAsDict = {}
        for key, value in objectAsDictionary.items() :
            if key not in ignoreKeyList :
                if isDictionary(value) :
                    filteredObjectAsDict[key] = filterIgnoreKeyList(value,ignoreKeyList)
                else :
                    filteredObjectAsDict[key] = objectAsDictionary[key]
        return filteredObjectAsDict
    return objectAsDictionary

def isEmpty(thing) :
    return StringHelper.isBlank(thing) if isinstance(thing, str) else isNone(thing) or isEmptyCollection(thing)

def isNotEmpty(thing) :
    return not isEmpty(thing)

def isEmptyCollection(thing) :
    return isCollection(thing) and 0 == len(thing)

def isNotEmptyCollection(thing) :
    return isCollection(thing) and 0 < len(thing)

def isList(thing) :
    return isinstance(thing, list)

def isNotList(thing) :
    return not isList(thing)

def isSet(thing) :
    return isinstance(thing, set)

def isNotSet(thing) :
    return not isSet(thing)

def isTuple(thing) :
    return isinstance(thing, tuple)

def isNotTuple(thing) :
    return not isTuple(thing)

def isDictionary(thing) :
    return isinstance(thing, dict)

def isNotDictionary(thing) :
    return not isDictionary(thing)

def isDictionaryClass(thingClass) :
    return dict == thingClass

def isNotDictionaryClass(thingClass) :
    return not isDictionaryClass(thingClass)

def isNone(instance) :
    return instance is None

def isNotNone(instance) :
    return not isNone(instance)

def isNativeClass(instanceClass) :
    return isNotNone(instanceClass) and instanceClass in NATIVE_CLASS_LIST

def isNotNativeClass(instanceClass) :
    return not isNativeClass(instanceClass)

def isNativeClassIsntance(instance) :
    return isNotNone(instance) and isNativeClass(instance.__class__)

def isNotNativeClassIsntance(instance) :
    return not isNativeClassIsntance(instance)

def isCollection(instance) :
    return isNotNone(instance) and instance.__class__ in COLLECTION_CLASS_LIST

def isNotCollection(instance) :
    return not isCollection(instance)
