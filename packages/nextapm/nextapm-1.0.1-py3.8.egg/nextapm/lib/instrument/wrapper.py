import nextapm.lib.logger as logger
from .modules import modulesInfo
from importlib import import_module
from ..util import isCallable
from ..constants import postHookKey, preHookKey, methodNameKey, classNameKey

def callHook(methodInfo, key, args, kwargs):
    try:
        hook = methodInfo.get(key, '')
        if not hook:
            return
            
        hook(args, kwargs)
    except Exception as err:
        logger.error('[callHook]', err)


def wrap(original, methodInfo):
    def wrapper(*args, **kwargs):
        callHook(methodInfo, preHookKey, args, kwargs)
        try:
            res = original(*args, **kwargs)
            return res
        except Exception as exc:
            raise exc
        finally:
            callHook(methodInfo, postHookKey, args, kwargs)

    wrapper.__name__ = original.__name__
    return wrapper


def instrumentModule(modName, actModule):
    if not modName:
        return

    if hasattr(actModule, 'nextapm_instrumented'):
        return 

    if modName in modulesInfo.keys():
        methodsInfo = modulesInfo.get(modName)
        for eachMethodInfo in methodsInfo:
            instrumentMethod(modName, actModule, eachMethodInfo)

        setattr(actModule, 'nextapm_instrumented', True)
        logger.info(modName+' instrumented')


def instrumentMethod(modName, actModule, methodInfo):
    parent = actModule

    if classNameKey in methodInfo:
        className = methodInfo.get(classNameKey)
        if hasattr(actModule, className):
            parent = getattr(actModule, className)


    methodName = methodInfo.get(methodNameKey, '')
    if hasattr(parent, methodName):
        original = getattr(parent, methodName)
        if not isCallable(original):
            return
        
        wrapper = wrap(original, methodInfo)
        setattr(parent,  methodName, wrapper)


def start():
    logger.info('starting instrumentation')
    for eachModule in modulesInfo:
        try:
            actModule = import_module(eachModule)
            instrumentModule(eachModule, actModule)
        except Exception as e:
            logger.error('unable to instument '+ eachModule, e)

