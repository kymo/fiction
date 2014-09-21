import sys
import time
import datetime

def datetime_timedelta(dtA, dtB):
    if sys.version_info[1] < 7:
        t = lambda x: time.mktime(x.timetuple())
        delta = int(t(dtB)-t(dtA))
    else:
        delta = dtB - dtA
        delta = int(delta.total_seconds())
    if delta < 60:
        return '%s s' % delta
    elif delta < 60 * 60:
        return '%s min' % (delta/60)
    elif delta < 60 * 60 * 24:
        return '%s h' % (delta/(60 * 60))
    else:
        return '%s day' % (delta/(60 * 60 * 24))

TIME_TMPL = '%(m)s-%(d)s %(H)s:%(M)s %(dm)s.'
def readable_time(dt):
    c = dict(
        m = dt.month,
        d = dt.day,
        H = ((dt.hour-12)>0 and [dt.hour-12] or [dt.hour])[0],
        M = dt.strftime('%M'),
        dm = ((dt.hour-12)>0 and ['pm'] or ['am'])[0]
    )
    return TIME_TMPL % c
