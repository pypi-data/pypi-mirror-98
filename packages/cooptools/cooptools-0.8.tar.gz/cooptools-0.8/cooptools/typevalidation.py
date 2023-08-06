import dateutil
import datetime

def float_as_currency(val: float):
    return "${:,.2f}".format(round(val, 2))


def int_tryParse(value):
    try:
        return int(value)
    except:
        return None


def datestamp_tryParse(value, include_time: bool = True, include_ms: bool = True):
    try:
        if type(value) == str:
            date_stamp = dateutil.parser.parse(value)
        elif type(value) in [datetime.datetime, datetime.date]:
            date_stamp = value
        else:
            raise NotImplementedError(f"Unhandled type [{type(value)}] for datestamp parsing")


        if not include_time:
            date_stamp = datetime.datetime.combine(date_stamp, datetime.datetime.min.time())

        if not include_ms:
            date_stamp = date_stamp.replace(microsecond=0)

        return date_stamp
    except:
        return None
