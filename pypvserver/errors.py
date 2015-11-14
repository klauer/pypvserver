# vi: ts=4 sw=4
'''
:mod:`pypvserver.errors` - CAS errors
=============================================

.. module:: pypvserver.errors
   :synopsis: Errors/return value information shared by the channel access
              server
'''
from pcaspy import cas

__all__ = ['casError',
           'casSuccess',
           'casPVNotFoundError',
           'casUndefinedValueError',
           'casAsyncCompletion',
           'casAsyncRunning',
           ]


class casError(Exception):
    ret = cas.S_casApp_success


class casSuccess(casError):
    ret = cas.S_casApp_success


class casPVNotFoundError(casError):
    ret = cas.S_casApp_pvNotFound


class casUndefinedValueError(casError):
    ret = cas.S_casApp_undefined


class casAsyncCompletion(casError):
    ret = cas.S_casApp_asyncCompletion


class casAsyncRunning(casError):
    ret = cas.S_casApp_postponeAsyncIO
