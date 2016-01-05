from functools import wraps, partial

from seamus.exceptions import SeamusException
from seamus.seamus import Seamus

REFACTORED_FUNC = 'refactored_func'
FACTORY = 'factory'


def seamus(func=None, **dkwargs):
    if func is None:
        return partial(seamus, **dkwargs)

    @wraps(func)
    def wrapper(*args, **kwargs):
        refactored_function = dkwargs.get(REFACTORED_FUNC, None)
        if refactored_function:
            factory = dkwargs.get(FACTORY, None)
            if factory:
                runner = factory()
            else:
                runner = Seamus()
            runner.use(func, *args, **kwargs)
            runner.test(refactored_function, *args, **kwargs)
            return runner.run()
        else:
            raise SeamusException(
                    'Refactored function can\'t be None. Are you missing the \'{}\' argument?'.format(
                        REFACTORED_FUNC))

    return wrapper
