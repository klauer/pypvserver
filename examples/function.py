#!/usr/bin/env python2.7
'''An example of using :class:`PypvFunction`, a decorator that makes a Python
function accessible over channel access (using ophyd's built-in EPICS channel
access server)
'''
from __future__ import print_function
import time
import logging

import epics
import numpy as np

from pypvserver import PypvFunction
import config

logger = logging.getLogger(__name__)


@PypvFunction()
def async_func(a=0, b=0.0, **kwargs):
    '''A PypvFunction, a Python function that has all input parameters
    represented as process variables. Execution is done asynchronously, using
    put completion on the client side (on the server/Python side, it is run in
    a separate thread from the channel access context)

    Note: Keyword arguments only allowed, since default values must be
          specified.
    Note: Prefix defaults to 'function_name:' when not specified

    Note: Since 0 is an integer, `a` will be an integer in EPICS
    Note: Since 0.0 is a float, `b` will be a float in EPICS
    '''
    logger.info('async_func called: a=%s b=%s, kw=%s', a, b, kwargs)

    # Function is called asynchronously, so it's OK to block:
    time.sleep(0.5)

    ret = a + b
    logger.info('async_func returning: %s' % ret)
    return ret


@PypvFunction(async=False, prefix='test:sync:')
def sync_func(a=0, b=0.0, **kwargs):
    '''Synchronously executed PypvFunction.
    Do not block in these functions.
    '''

    # TODO: should we even give access to synchronous functions to users?
    logger.info('sync_func called: a=%s b=%s, kw=%s', a, b, kwargs)
    # Not an asynchronous PV, don't block
    return a * b


@PypvFunction(return_value='test')
def string_func(value='test'):
    '''Functions work on strings as well. This function takes a string and
    returns a string

    Note: EPICS string limitations apply here
    '''

    logger.info('string_func called: value=%s' % value)
    # Not a asynchronous PV, don't block
    return value.upper()


@PypvFunction(type_=np.int32, count=10)
def array_func(value=0.0):
    '''Keyword arguments get passed on to PyPV for the return value, so you
    can specify more about the return type in the PypvFunction decorator
    '''

    logger.info('array_func called: value=%s', value)
    return np.arange(10) * value


@PypvFunction(type_=np.int32, count=10,
              async=False)
def no_arg_func():
    '''No arguments taken in the function, returns an int array of 10
    elements'''

    logger.info('no_arg_func called')
    return np.arange(10)


@PypvFunction()
def array_input_func(value=np.array([1., 2., 3.], dtype=np.float)):
    '''Keyword arguments get passed on to PyPV for the return value, so you
    can specify more about the return type
    '''

    logger.info('array_input_func called: value=%s', value)
    return np.average(value)


@PypvFunction()
def failure_func():
    '''If exceptions are raised, the status PV gets updated to reflect that'''
    logger.info('failure_func called')
    raise ValueError('failed, somehow')


@PypvFunction(return_value=True)
def bool_func(bool_one=False, bool_two=True):
    '''Boolean values turn into EPICS enums, with values: ['False', 'True']'''
    logger.info('bool_func called: bool_one=%r bool_two=%r', bool_one,
                bool_two)

    return bool(bool_one or bool_two)


# Can't use positional arguments:
try:
    @PypvFunction(prefix='test:')
    def test1(a, b=1):
        pass
except ValueError:
    logger.debug('(Failed as expected)')


# Can't use variable arguments:
try:
    @PypvFunction(prefix='test:')
    def test2(a=1, *b):
        pass
except ValueError:
    logger.debug('(Failed as expected)')


# The individual tests below call the PypvFunctions through both channel access
# and through standard Python function calls

def test_async():
    logger.info('asynchronous function')
    pvnames = async_func.get_pvnames()

    sig_a = epics.PV(pvnames['a'])
    sig_b = epics.PV(pvnames['b'])
    sig_proc = epics.PV(pvnames['process'])
    sig_ret = epics.PV(pvnames['retval'])

    a, b = 3.0, 4.0

    sig_a.put(a)
    sig_b.put(b)
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r' % sig_ret.get())

    logger.info('called normally: %r' % async_func(a=a, b=b))


def test_sync():
    logger.info('synchronous function')
    pvnames = sync_func.get_pvnames()

    sig_a = epics.PV(pvnames['a'])
    sig_b = epics.PV(pvnames['b'])
    sig_proc = epics.PV(pvnames['process'])
    sig_ret = epics.PV(pvnames['retval'])

    a, b = 3.0, 4.0
    sig_a.put(a)
    sig_b.put(b)
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r' % sig_ret.get())

    logger.info('called normally: %r' % sync_func(a=a, b=b))


def test_string():
    logger.info('string function')
    pvnames = string_func.get_pvnames()

    sig_value = epics.PV(pvnames['value'])
    sig_proc = epics.PV(pvnames['process'])
    sig_ret = epics.PV(pvnames['retval'])

    sig_value.put('hello')
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r' % sig_ret.get())

    logger.info('called normally: %r' % string_func(value='hello'))


def test_array():
    logger.info('array function')
    pvnames = array_func.get_pvnames()

    sig_value = epics.PV(pvnames['value'])
    sig_proc = epics.PV(pvnames['process'])
    sig_ret = epics.PV(pvnames['retval'])

    sig_value.put(2.0)
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r' % sig_ret.get())

    logger.info('called normally: %r' % array_func(value=2.0))


def test_array_input():
    logger.info('array input function')
    pvnames = array_input_func.get_pvnames()

    sig_value = epics.PV(pvnames['value'])
    sig_proc = epics.PV(pvnames['process'])
    sig_ret = epics.PV(pvnames['retval'])

    input_ = np.array([5, 10, 15])
    sig_value.put(input_)
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r' % sig_ret.get())

    logger.info('called normally: %r' % array_input_func(value=input_))


def test_no_arg():
    logger.info('no argument function')
    pvnames = no_arg_func.get_pvnames()

    sig_proc = epics.PV(pvnames['process'])
    sig_ret = epics.PV(pvnames['retval'])

    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r' % sig_ret.get())

    logger.info('called normally: %r' % no_arg_func())


def test_failure():
    logger.info('function that fails with an exception')
    pvnames = failure_func.get_pvnames()

    sig_proc = epics.PV(pvnames['process'])
    sig_status = epics.PV(pvnames['status'])

    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('status pv shows: %r' % sig_status.get())


def test_bool():
    logger.info('logical or of two boolean values')
    pvnames = bool_func.get_pvnames()

    sig_bool1 = epics.PV(pvnames['bool_one'])
    sig_bool2 = epics.PV(pvnames['bool_two'])
    sig_proc = epics.PV(pvnames['process'])
    sig_status = epics.PV(pvnames['status'])
    sig_ret = epics.PV(pvnames['retval'])

    one, two = True, False
    sig_bool1.put(one)
    sig_bool2.put(two)
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r (string is %r)' %
                (sig_ret.get(), sig_ret.get(as_string=True)))

    logger.info('called normally: %r' % bool_func(bool_one=one, bool_two=two))

    one, two = False, False
    sig_bool1.put(one)
    sig_bool2.put(two)
    sig_proc.put(1)

    time.sleep(0.1)
    logger.info('result through channel access: %r (string is %r)' %
                (sig_ret.get(), sig_ret.get(as_string=True)))

    logger.info('called normally: %r' % bool_func(bool_one=one, bool_two=two))


def test():
    config.setup_logging([__name__, 'pypvserver.function'])
    server = config.get_server()

    test_async()
    test_sync()
    test_string()
    test_array()
    test_array_input()
    test_no_arg()
    test_failure()
    test_bool()


if __name__ == '__main__':
    test()
