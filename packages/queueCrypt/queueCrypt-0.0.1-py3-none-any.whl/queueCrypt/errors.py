__all__ = ["ErrorRequestedHigherThanExpected", "ErrorQueueSizeNotValid"]


class ErrorRequestedHigherThanExpected(Exception):
    """This Error occurs when given to put a bigger amount to the queue than what was set as default"""


class ErrorQueueSizeNotValid(Exception):
    """This Error occurs when given a number that is not valid amount (invalid size: length < 0)"""
