# vi: ts=4 sw=4
'''
:mod:`pypvserver.errors` - CAS errors
=============================================

.. module:: pypvserver.errors
   :synopsis: Errors/return value information shared by the channel access
              server
'''
from pcaspy import cas

__all__ = ['PypvError',
           'PypvSuccess',
           'PVNotFoundError',
           'UndefinedValueError',
           'AsyncCompletion',
           'AsyncRunning',
           ]


class PypvError(Exception):
    ret = cas.S_casApp_success


class PypvSuccess(PypvError):
    ret = cas.S_casApp_success


class PVNotFoundError(PypvError):
    ret = cas.S_casApp_pvNotFound


class UndefinedValueError(PypvError):
    ret = cas.S_casApp_undefined


class AsyncCompletion(PypvError):
    ret = cas.S_casApp_asyncCompletion


class AsyncRunning(PypvError):
    ret = cas.S_casApp_postponeAsyncIO
