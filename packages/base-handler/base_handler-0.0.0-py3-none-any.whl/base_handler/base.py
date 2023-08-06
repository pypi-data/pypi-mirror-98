from abc import ABC, abstractmethod
from functools import wraps
import logging


def entry_and_exit_logging(function):
    """
    Credit for this decorator goes to:
    https://medium.com/swlh/10-recommendations-for-writing-pragmatic-aws-lambdas-in-python-5f4b038caafe
    """
    @wraps(function)
    def wrapper(event, context):
        logging.info(f"'{context.function_name}' - entry.\nIncoming event: '{event}'")
        result = function(event, context)
        logging.info(f"'{context.function_name}' - exit.\nResult: '{result}'")
        return result

    return wrapper


class HandlerBase(ABC):
    @entry_and_exit_logging
    @abstractmethod
    def handle(self, event, context):
        pass

# TODO: add transform, fit and predict subclasses?
