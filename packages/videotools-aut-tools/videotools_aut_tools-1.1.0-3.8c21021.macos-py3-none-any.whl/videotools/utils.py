"""
    Module with different helper utilities
"""
import logging
from datetime import datetime, timedelta
from subprocess import CalledProcessError

import pytz

from videotools import DEFAULT_TIMEZONE


def natural_order_key(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    int_text = lambda text: int(text) if text.isdigit() else text

    return [int_text(c) for c in re.split('(\d+)', text)]


def check_output(sentence):
    """
    This is a convenience method to execute any sentence and check if an error occurred, and get output
    from sentence command
    :param sentence: whatever needs to be executed
    :return: The output from command. A CalledProcessError is thrown if an error occurs
    """
    try:
        output = check_output(sentence, shell=True)
    except CalledProcessError as ex:
        raise Exception('\t\t check_call ERROR executing [%s], return code:= [%s]' % (sentence, ex.returncode))
    return output


class DateTimeHelper:
    """
    Helper class to be use with date and time manipulations
    """
    _LOGGER = logging.getLogger('DateTimeHelper')

    ISO_FORMAT_DATE = '%Y-%m-%d'
    ISO_FORMAT_TIME = '%H:%M'

    @staticmethod
    def is_short_format(short_date_as_string):
        """
        Verifies if supplied date matches short date regex
        :param short_date_as_string: The string to verify in short format yyyy-mm-dd
        :return: True if matches format, False otherwise
        """
        try:
            datetime.strptime(short_date_as_string, DateTimeHelper.ISO_FORMAT_DATE)
            return True
        except (TypeError, ValueError, Exception):
            return False

    @staticmethod
    def yesterday(as_string=True):
        """
        Provides yesterday date
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: Yesterday date as s string or a datetime object
        """
        return DateTimeHelper.days_ago(1, as_string)

    @staticmethod
    def sixty_days_ago(as_string=True):
        """
        Provides the date of sixty days ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: Two months ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(60, as_string)

    @staticmethod
    def thirty_days_ago(as_string=True):
        """
        Provides the date of a thirty days ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: A month ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(30, as_string)

    @staticmethod
    def two_weeks_ago(as_string=True):
        """
        Provides the date of a week ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: Two weeks ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(14, as_string)

    @staticmethod
    def a_week_ago(as_string=True):
        """
        Provides the date of a week ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: A week ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(7, as_string)

    @staticmethod
    def days_ago(number_of_days, as_string=True):
        """
        Provides the date value of number of days in short format yyyy-mm-dd
        :param number_of_days: Number of days ago from current date
        :param as_string: If true, provide the date as a string. Return the datetime object otherwise
        :return: Yesterday date as yyyy-mm-dd
        """
        days_ago = datetime.now() - timedelta(days=number_of_days)
        if as_string:
            return DateTimeHelper.datetime_to_iso8601(days_ago, DateTimeHelper.ISO_FORMAT_DATE)
        else:
            return days_ago

    @staticmethod
    def days_between(date1, date2):
        """
        Provides the number of dates between supplied two dates. If supplied dates are a string, they are
        converted to a datetime object, and the format must be as yyyy-mm-dd
        :param date1: A date as a string or a datetime
        :param date2: A date as a string or a datetime
        :return: The difference in days between supplied dates as an integer. An exception is thrown
                 if a problem occurs
        """
        if isinstance(date1, str):
            date1 = datetime.strptime(date1, DateTimeHelper.ISO_FORMAT_DATE)
        if isinstance(date2, str):
            date2 = datetime.strptime(date2, DateTimeHelper.ISO_FORMAT_DATE)
        return abs((date2 - date1).days)

    @staticmethod
    def short_date(_datetime=datetime.now()):
        """
        Provides current date in short format yyyy-mm-dd
        :return: The date as  yyyy-mm-dd
        """
        return DateTimeHelper.datetime_to_iso8601(_datetime, DateTimeHelper.ISO_FORMAT_DATE)

    @staticmethod
    def short_time():
        """
        Provides current date in short format hh:mm
        :return: The date as hh:mm
        """
        return DateTimeHelper.datetime_to_iso8601(datetime.now(), DateTimeHelper.ISO_FORMAT_TIME)

    @staticmethod
    def iso8601_to_datetime(time_as_iso8601, iso_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Given a date as a  ISO8601 string, i.e:  yyyy-MM-dd'T'HH:mm:ss.SSSZ, provides a datetime object.
        The string object is split at the <+> symbol.
        :param time_as_iso8601: String with a time representation in ISO8601 format as yyyy-MM-ddTHH:mm:ss.SSSZ
        :return: A datetime object with supplied date as string
        """
        # If string has the + symbol, split it:
        if '+' in time_as_iso8601:
            time_as_iso8601 = time_as_iso8601.split('+')[0]

        try:
            return datetime.strptime(time_as_iso8601, iso_format)
        except Exception as ex:
            raise Exception(f'\t\t Exception parsing strinng date in ISO8601 format {time_as_iso8601}')

    @staticmethod
    def datetime_to_iso8601(time_as_datetime, iso_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Given a datetime object provide a  ISO8601 string representation
        :param time_as_datetime: A datetime object
        :return: A string with ISO8601 representation of the supplied datetime object
        """

        try:
            return time_as_datetime.strftime(iso_format)
        except Exception:
            raise Exception('\t\t Exception converting datetime to ISO8601 format')

    @staticmethod
    def iso8601_to_anyformat(time_as_iso8601, format='%d-%m-%Y'):
        """
         Given a date as a  ISO8601 string, i.e:  yyyy-MM-dd'T'HH:mm:ss.SSSZ, provides a string with another format
         :param time_as_iso8601: String with a time representation in ISO8601 format as yyyy-MM-ddTHH:mm:ss.SSSZ
         :return: A string with date as dd-MM-yyyy
         """
        try:
            date_as_str = DateTimeHelper.iso8601_to_datetime(time_as_iso8601)
            date_as_str = DateTimeHelper.datetime_to_iso8601(date_as_str, iso_format=format)
        except Exception:
            date_as_str = 'Wrong Format'
        return date_as_str

    @staticmethod
    def compare_iso8601_dates(date1_as_iso8601, date2_as_iso8601):
        """
        Method that compares two dates, if the first one is bigger, the result is positive, if the second one is bigger
        the result is negative, if they are equal, a 0 is returned
        :param date1_as_iso8601: A string date representation as ISO8601
        :param date2_as_iso8601: A string date representation as ISO8601
        :return: An integer. Positive if date1>date2, negative if date2>date1 or 0 otherwise
        """
        try:
            date1 = DateTimeHelper.iso8601_to_datetime(date1_as_iso8601)
            date2 = DateTimeHelper.iso8601_to_datetime(date2_as_iso8601)

            if date1 > date2:
                return 1
            elif date2 > date1:
                return -1
            else:
                return 0
        except Exception as es:
            raise Exception(f'\t\t exception comparing iso8601 dates {date1_as_iso8601}{date2_as_iso8601}')

    @staticmethod
    def string_date_to_datetime(date_as_string, iso_format='%Y-%m-%d'):
        """
        Converts supplied date, to datetime object. Default format : %Y-%m-%d
        :param date_as_string: The date as a string, with format yyyy-mm-dds
        :return: A datetime object
        """
        try:
            return datetime.strptime(date_as_string, iso_format)
        except Exception as ex:
            DateTimeHelper._LOGGER.error(f'could not convert from date to datetime [{date_as_string}] using format '
                                         f'[{iso_format}]')
            raise ex

    @staticmethod
    def datetime_to_epoch(datetime_object):
        """
        Converts supplied datetime to epoch in milliseconds
        :param datetime_object: A datetime object
        :return: The number of milliseconds since epoch
        """
        epoch = int((datetime_object - datetime(1970, 1, 1)).total_seconds() * 1000)
        return f'{epoch}'

    @staticmethod
    def date_from_timezone(timezone=DEFAULT_TIMEZONE, iso_format=None, date=None):
        """
        Provides date as a string in a given timezone, using supplied format
        :param timezone:  A valid timezone
        :param iso_format: The format to use to express the datetime object
        :param date: The date to express in the former timezone
        :return: The date as a string
        """
        if date:
            date = pytz.timezone(timezone).localize(date)
        else:
            date = datetime.now(tz=pytz.timezone(timezone))
        if iso_format:
            date = date.strftime(iso_format)
        return date

    @staticmethod
    def to_hours_min_seconds(seconds):
        """
        Converts given seconds to hour, minutes and seconds
        :param seconds: The total number of seconds
        :return:  A tuple as (hour, min, sec)
        """
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return (hour, min, sec)
