#!/usr/bin/env python2.7
'''An example of using :class:`PypvMotor`, which allows Ophyd
:class:`Positioner`s to be accessed by EPICS, via the built-in channel access
server.
'''
from __future__ import print_function
import epics
import logging

import config

from pypvserver import PypvMotor
from ophyd.controls import (EpicsMotor, PVPositioner)


logger = logging.getLogger(__name__)


def test():
    config.setup_logging([__name__, 'pypvserver.motor'])
    server = config.get_server()

    motor_record = config.motor_recs[0]
    mrec = EpicsMotor(motor_record)

    logger.info('--> PV Positioner, using put completion and a DONE pv')
    # PV positioner, put completion, done pv
    pos = PVPositioner(mrec.field_pv('VAL'),
                       readback=mrec.field_pv('RBV'),
                       done=mrec.field_pv('MOVN'), done_val=0,
                       stop=mrec.field_pv('STOP'), stop_val=1,
                       put_complete=True,
                       limits=(-2, 2),
                       egu='unknown',
                       )

    def updated(value=None, **kwargs):
        print('Updated to: %s' % value)

    ppv_motor = PypvMotor('m1', pos, server=server)
    print(ppv_motor.severity)
    record_name = ppv_motor.full_pvname
    for i in range(2):
        epics.caput(record_name, i, wait=True)
        print(pos.position)
    return ppv_motor


if __name__ == '__main__':
    ppv_motor = test()
