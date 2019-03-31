import sys

from PyQt5.QtCore import QObject
from antlr4.error.ErrorListener import ErrorListener

from OrodaelTurrim.Presenter.Connector import Connector


class CustomErrorListener(ErrorListener, QObject):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = 'Error: Problem with parsing rules: {} at line {} column {}. Rules not parsed!\n'.format(msg, line,
                                                                                                             column)

        sys.stderr.write(error_msg)

        UI_error = 'Problem with parsing rules:\n\n{} at line {} column {}.\n\nRules not parsed!\n'.format(msg,
                                                                                                                line,
                                                                                                                column)
        Connector().emit('error_message', 'Rule parser', UI_error)


    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        sys.stderr.write('Problem with parsing rules!')
