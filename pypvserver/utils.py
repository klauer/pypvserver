from .alarms import MinorAlarmError, get_alarm_class

__all__ = ['split_record_field',
           'strip_field',
           'record_field',
           'check_alarm',
           ]


def split_record_field(pv):
    '''Splits a pv into (record, field)

    Parameters
    ----------
    pv : str
        the pv to split

    Returns
    -------
    record : str
    field : str
    '''
    if '.' in pv:
        record, field = pv.rsplit('.', 1)
    else:
        record, field = pv, ''

    return record, field


def strip_field(pv):
    '''Strip off the field from a record'''
    return split_record_field(pv)[0]


def record_field(record, field):
    '''Given a record and a field, combine them into a pv of the form:
    record.FIELD
    '''
    record = strip_field(record)
    return '{}.{}'.format(record, field.upper())


def check_alarm(base_pv, stat_field='STAT', severity_field='SEVR',
                reason_field=None, reason_pv=None,
                min_severity=MinorAlarmError.severity):
    """Raise an exception if an alarm is set

    Raises
    ------
    AlarmError (MinorAlarmError, MajorAlarmError)
    """
    stat_pv = '%s.%s' % (base_pv, stat_field)
    severity_pv = '%s.%s' % (base_pv, severity_field)
    if reason_field is not None:
        reason_pv = '%s.%s' % (base_pv, reason_field)
    reason = None

    import epics
    severity = epics.caget(severity_pv)

    if severity >= min_severity:
        try:
            error_class = get_alarm_class(severity)
        except KeyError:
            pass
        else:
            severity = epics.caget(severity_pv, as_string=True)
            alarm = epics.caget(stat_pv, as_string=True)
            if reason_pv is not None:
                reason = epics.caget(reason_pv, as_string=True)

            message = 'Alarm status %s [severity %s]' % (alarm, severity)
            if reason is not None:
                message = '%s: %s' % (message, reason)

            raise error_class(message)

    return True
