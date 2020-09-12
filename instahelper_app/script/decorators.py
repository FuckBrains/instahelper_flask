
def run_again(xtimes):

    def decorator(func):
        
        def inner(*args, **kwargs):
            if callable(xtimes):
                x = 2
            else:
                x = xtimes
            while x >= 0:
                x -= 1
                result = func(*args, **kwargs)
                if result: break

            return result

        return inner
    if callable(xtimes):   #   arg is variable if exists
        return decorator(xtimes)
    else:
        return decorator

