#!/usr/bin/env python2.7
'''An example of using :class:`caServer`, an EPICS channel access server
implementation based on pcaspy
'''
from __future__ import print_function
import time
import logging

import epics

from pypvserver import PyPV
import config


logger = logging.getLogger(__name__)


def updated(value=None, **kwargs):
    logger.info('pyepics client sees new value: %s', value)


def test():
    config.setup_logging([__name__, 'pypvserver.pv'])
    server = config.get_server()
    logger.info('Creating PV "pv1", a floating-point type')
    python_pv = PyPV('pv1', 123.0, server=server)

    # full_pvname includes the server prefix
    pvname = python_pv.full_pvname
    logger.info('... which is %s including the server prefix', pvname)

    signal = epics.PV(pvname)
    signal.add_callback(updated)

    time.sleep(0.1)

    for value in range(10):
        logger.info('Updating the value on the server-side to: %s', value)
        python_pv.value = value
        time.sleep(0.05)

    logger.info('Done')


if __name__ == '__main__':
    test()
