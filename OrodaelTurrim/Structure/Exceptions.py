class OrodaelTurrimException(Exception):
    """ Base framework exception. All framework exception inherit from this exception """
    pass


class IllegalArgumentException(OrodaelTurrimException):
    """ Illegal argument passed to object initialization """
    pass


class IllegalActionException(OrodaelTurrimException):
    """ You try to use illegal action on the game engine """
    pass


class IllegalHistoryOperation(OrodaelTurrimException):
    """ Trying to do illegal operation when in Browsing mode """
    pass


class IllegalLogMessage(OrodaelTurrimException):
    """ You are trying to log message which is not correct type """
    pass
