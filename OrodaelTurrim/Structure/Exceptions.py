class OrodaelTurrimException(Exception):
    pass


class IllegalArgumentException(OrodaelTurrimException):
    pass


class IllegalActionException(OrodaelTurrimException):
    pass


class IllegalHistoryOperation(OrodaelTurrimException):
    pass


class IllegalLogMessage(OrodaelTurrimException):
    pass
