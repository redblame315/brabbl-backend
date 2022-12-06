from functools import partial
import inspect
import logging
import sys
from django.conf import settings


class Logger(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # pass logging calls through to `log()` function
        for level in ('info', 'warn', 'warning', 'error', 'exception'):
            setattr(self, level, partial(self.log, level))

    def log(self, level, message, *args, **kwargs):
        '''
        Log the specified message with log level "level".

        Level can be one of 'debug', 'info', 'notice', 'warning', 'error'.
        Messages can contain placeholders "%s" with the actual content in *args.
        Sentry will group messages with the same message and only different args.

        If there's a keyword argument "request" with a Django request object, details
        about the request will be logged as well.
        If there's a keyword argument "exception" which evaluates as True, all
        details about the last exception will be captured as well
        '''
        kw = {}
        if 'request' in kwargs:
            kw['extra'] = {'request': kwargs['request']}

            if kwargs['request'].user.is_authenticated:
                kw['extra']['data'] = {
                    'data': {'username': kwargs['request'].user.username},
                }

        if 'exception' in kwargs or level == 'exception':
            exc = sys.exc_info()
            if exc[0] is not None:
                kw['exc_info'] = exc

        stack = inspect.stack()
        if 'execute_from_command_line' in stack[-1][4][0]:
            # it's called from a management command, use a custom logger
            caller = 'management_commands'
        else:
            # walk up the call stack and get the callers __name__
            caller = inspect.getmodule(inspect.stack()[2][0])
            if caller:
                caller = caller.__name__
            else:
                caller = settings.PROJECT_NAME
        logging.getLogger(caller).log(getattr(logging, level.upper()), message,
                                      *args, **kw)

logger = Logger()
