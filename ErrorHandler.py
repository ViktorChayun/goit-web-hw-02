from functools import wraps


# обробник помилок спільний для всіх команд
def input_error(func):
    @wraps(func)
    def inner_func(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError as err:
            return f"Invalid command: {err}"
        except ValueError as err:
            return f"Invalid command: {err}"
        except IndexError as err:
            return f"Invalid command: {err}"
        except Exception as err:
            return f"Unexpected error: {err}"
    return inner_func
