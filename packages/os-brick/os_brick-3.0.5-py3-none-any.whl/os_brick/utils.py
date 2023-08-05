#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
"""Utilities and helper functions."""

import functools
import inspect
import logging as py_logging
import retrying
import six
import time

from oslo_log import log as logging
from oslo_utils import encodeutils
from oslo_utils import strutils

from os_brick.i18n import _


LOG = logging.getLogger(__name__)


def retry(exceptions, interval=1, retries=3, backoff_rate=2):

    def _retry_on_exception(e):
        return isinstance(e, exceptions)

    def _backoff_sleep(previous_attempt_number, delay_since_first_attempt_ms):
        exp = backoff_rate ** previous_attempt_number
        wait_for = max(0, interval * exp)
        LOG.debug("Sleeping for %s seconds", wait_for)
        return wait_for * 1000.0

    def _print_stop(previous_attempt_number, delay_since_first_attempt_ms):
        delay_since_first_attempt = delay_since_first_attempt_ms / 1000.0
        LOG.debug("Failed attempt %s", previous_attempt_number)
        LOG.debug("Have been at this for %s seconds",
                  delay_since_first_attempt)
        return previous_attempt_number == retries

    if retries < 1:
        raise ValueError(_('Retries must be greater than or '
                         'equal to 1 (received: %s). ') % retries)

    def _decorator(f):

        @six.wraps(f)
        def _wrapper(*args, **kwargs):
            r = retrying.Retrying(retry_on_exception=_retry_on_exception,
                                  wait_func=_backoff_sleep,
                                  stop_func=_print_stop)
            return r.call(f, *args, **kwargs)

        return _wrapper

    return _decorator


def platform_matches(current_platform, connector_platform):
    curr_p = current_platform.upper()
    conn_p = connector_platform.upper()
    if conn_p == 'ALL':
        return True

    # Add tests against families of platforms
    if curr_p == conn_p:
        return True

    return False


def os_matches(current_os, connector_os):
    curr_os = current_os.upper()
    conn_os = connector_os.upper()
    if conn_os == 'ALL':
        return True

    # add tests against OSs
    if (conn_os == curr_os or
       conn_os in curr_os):
        return True

    return False


def merge_dict(dict1, dict2):
    """Try to safely merge 2 dictionaries."""
    if type(dict1) is not dict:
        raise Exception("dict1 is not a dictionary")
    if type(dict2) is not dict:
        raise Exception("dict2 is not a dictionary")

    dict3 = dict1.copy()
    dict3.update(dict2)
    return dict3


def trace(f):
    """Trace calls to the decorated function.

    This decorator should always be defined as the outermost decorator so it
    is defined last. This is important so it does not interfere
    with other decorators.

    Using this decorator on a function will cause its execution to be logged at
    `DEBUG` level with arguments, return values, and exceptions.

    :returns: a function decorator
    """

    func_name = f.__name__

    @functools.wraps(f)
    def trace_logging_wrapper(*args, **kwargs):
        if len(args) > 0:
            maybe_self = args[0]
        else:
            maybe_self = kwargs.get('self', None)

        if maybe_self and hasattr(maybe_self, '__module__'):
            logger = logging.getLogger(maybe_self.__module__)
        else:
            logger = LOG

        # NOTE(ameade): Don't bother going any further if DEBUG log level
        # is not enabled for the logger.
        if not logger.isEnabledFor(py_logging.DEBUG):
            return f(*args, **kwargs)

        all_args = inspect.getcallargs(f, *args, **kwargs)
        logger.debug('==> %(func)s: call %(all_args)r',
                     {'func': func_name,
                      # NOTE(mriedem): We have to stringify the dict first
                      # and don't use mask_dict_password because it results in
                      # an infinite recursion failure.
                      'all_args': strutils.mask_password(
                          six.text_type(all_args))})

        start_time = time.time() * 1000
        try:
            result = f(*args, **kwargs)
        except Exception as exc:
            total_time = int(round(time.time() * 1000)) - start_time
            logger.debug('<== %(func)s: exception (%(time)dms) %(exc)r',
                         {'func': func_name,
                          'time': total_time,
                          'exc': exc})
            raise
        total_time = int(round(time.time() * 1000)) - start_time

        if isinstance(result, dict):
            mask_result = strutils.mask_dict_password(result)
        elif isinstance(result, six.string_types):
            mask_result = strutils.mask_password(result)
        else:
            mask_result = result

        logger.debug('<== %(func)s: return (%(time)dms) %(result)r',
                     {'func': func_name,
                      'time': total_time,
                      'result': mask_result})
        return result
    return trace_logging_wrapper


def convert_str(text):
    """Convert to native string.

    Convert bytes and Unicode strings to native strings:

    * convert to bytes on Python 2:
      encode Unicode using encodeutils.safe_encode()
    * convert to Unicode on Python 3: decode bytes from UTF-8
    """
    if six.PY2:
        return encodeutils.to_utf8(text)
    else:
        if isinstance(text, bytes):
            return text.decode('utf-8')
        else:
            return text
